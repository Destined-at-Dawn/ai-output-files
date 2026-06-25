#include "remote.h"
#include "bsp_port.h"

static remote_cmd_t g_cmd;
static remote_button_t g_buttons[KEY_ID_COUNT];
static uint8_t g_stop_latched;
static chassis_mode_t g_chassis_mode;

static void Button_Update(remote_button_t *button, uint8_t raw_pressed, uint32_t now_ms)
{
    button->short_event = 0U;
    button->long_event = 0U;
    button->repeat_event = 0U;

    if (raw_pressed != button->last_raw) {
        button->last_raw = raw_pressed;
        button->raw_changed_ms = now_ms;
    }

    if ((now_ms - button->raw_changed_ms) < REMOTE_DEBOUNCE_MS) {
        return;
    }

    if (raw_pressed != button->stable_pressed) {
        button->stable_pressed = raw_pressed;

        if (button->stable_pressed) {
            button->press_start_ms = now_ms;
            button->last_repeat_ms = now_ms;
        } else {
            uint32_t pressed_ms = now_ms - button->press_start_ms;
            if (pressed_ms < REMOTE_LONG_PRESS_MS) {
                button->short_event = 1U;
            }
        }
    }

    if (button->stable_pressed) {
        uint32_t pressed_ms = now_ms - button->press_start_ms;
        if (pressed_ms >= REMOTE_LONG_PRESS_MS) {
            if ((now_ms - button->last_repeat_ms) >= REMOTE_REPEAT_MS) {
                button->long_event = 1U;
                button->repeat_event = 1U;
                button->last_repeat_ms = now_ms;
            }
        }
    }
}

void Remote_Init(void)
{
    uint32_t i;

    for (i = 0U; i < KEY_ID_COUNT; i++) {
        g_buttons[i].stable_pressed = 0U;
        g_buttons[i].last_raw = 0U;
        g_buttons[i].short_event = 0U;
        g_buttons[i].long_event = 0U;
        g_buttons[i].repeat_event = 0U;
        g_buttons[i].raw_changed_ms = 0U;
        g_buttons[i].press_start_ms = 0U;
        g_buttons[i].last_repeat_ms = 0U;
    }

    g_stop_latched = 1U;
    g_chassis_mode = CHASSIS_INDEPENDENT;

    g_cmd.robot_mode = ROBOT_STOP;
    g_cmd.chassis_mode = CHASSIS_INDEPENDENT;
    g_cmd.chassis_speed.vx = 0.0f;
    g_cmd.chassis_speed.vy = 0.0f;
    g_cmd.chassis_speed.wz = 0.0f;
    g_cmd.yaw_step_positive = 0U;
    g_cmd.pitch_step_positive = 0U;
    g_cmd.emergency_toggle = 0U;
    g_cmd.valid = 1U;
    g_cmd.last_update_ms = 0U;
}

void Remote_Update(uint32_t now_ms)
{
    uint32_t i;

    for (i = 0U; i < KEY_ID_COUNT; i++) {
        Button_Update(&g_buttons[i], BSP_ReadKey((key_id_t)i), now_ms);
    }

    g_cmd.yaw_step_positive = 0U;
    g_cmd.pitch_step_positive = 0U;
    g_cmd.emergency_toggle = 0U;

    if (g_buttons[KEY_ID_STOP].short_event != 0U) {
        g_stop_latched = (uint8_t)!g_stop_latched;
        g_cmd.emergency_toggle = 1U;
    }

    if (g_buttons[KEY_ID_1].short_event != 0U) {
        if (g_chassis_mode == CHASSIS_SPIN) {
            g_chassis_mode = CHASSIS_INDEPENDENT;
        } else {
            g_chassis_mode = CHASSIS_SPIN;
        }
    }

    if (g_buttons[KEY_ID_1].stable_pressed != 0U &&
        (now_ms - g_buttons[KEY_ID_1].press_start_ms) >= REMOTE_LONG_PRESS_MS) {
        g_chassis_mode = CHASSIS_FOLLOW_GIMBAL;
    } else if (g_chassis_mode == CHASSIS_FOLLOW_GIMBAL) {
        g_chassis_mode = CHASSIS_INDEPENDENT;
    }

    if (g_buttons[KEY_ID_2].short_event != 0U || g_buttons[KEY_ID_2].repeat_event != 0U) {
        g_cmd.yaw_step_positive = 1U;
    }

    if (g_buttons[KEY_ID_3].short_event != 0U || g_buttons[KEY_ID_3].repeat_event != 0U) {
        g_cmd.pitch_step_positive = 1U;
    }

    g_cmd.robot_mode = (g_stop_latched != 0U) ? ROBOT_STOP : ROBOT_NORMAL;
    g_cmd.chassis_mode = g_chassis_mode;

    /*
     * Keep translation speed zero until joystick, keyboard, or UART values
     * are explicitly connected. Never move forward automatically after boot.
     */
    g_cmd.chassis_speed.vx = 0.0f;
    g_cmd.chassis_speed.vy = 0.0f;
    g_cmd.chassis_speed.wz = 0.0f;

    g_cmd.valid = 1U;
    g_cmd.last_update_ms = now_ms;
}

const remote_cmd_t *Remote_GetCommand(void)
{
    return &g_cmd;
}

uint8_t Remote_ParseUartFrame(const uint8_t *data, uint16_t len, remote_cmd_t *out_cmd)
{
    if (data == 0 || out_cmd == 0 || len < 8U) {
        return 0U;
    }

    /*
     * Assignment protocol:
     * header: 0x0a 0x05
     * fields: Vx, Vy, gimbal speed, checksum
     * tail:   0x05 0x0a
     */
    if (data[0] != 0x0aU || data[1] != 0x05U) {
        return 0U;
    }
    if (data[len - 2U] != 0x05U || data[len - 1U] != 0x0aU) {
        return 0U;
    }

    if (data[5] != 0x06U) {
        return 0U;
    }

    out_cmd->chassis_speed.vx = (float)((int8_t)data[2]) * 20.0f;
    out_cmd->chassis_speed.vy = (float)((int8_t)data[3]) * 20.0f;
    out_cmd->chassis_speed.wz = (float)((int8_t)data[4]);
    out_cmd->valid = 1U;

    return 1U;
}
