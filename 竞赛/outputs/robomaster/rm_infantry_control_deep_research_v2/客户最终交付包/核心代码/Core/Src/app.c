#include "app.h"
#include "bsp_port.h"
#include "chassis.h"
#include "gimbal.h"
#include "remote.h"
#include "safety.h"

static uint32_t g_last_control_ms;

static void App_UpdateLed(uint32_t now_ms, const remote_cmd_t *cmd)
{
    uint32_t breath_period = 1000U;
    uint32_t t = now_ms % breath_period;
    float duty;
    uint32_t mode_period;
    uint8_t l2_on;

    if (t < (breath_period / 2U)) {
        duty = (float)t / (float)(breath_period / 2U);
    } else {
        duty = (float)(breath_period - t) / (float)(breath_period / 2U);
    }
    BSP_SetLedL1(duty);

    if (cmd != 0 && cmd->chassis_mode == CHASSIS_SPIN) {
        mode_period = 250U;
    } else if (cmd != 0 && cmd->chassis_mode == CHASSIS_FOLLOW_GIMBAL) {
        mode_period = 167U;
    } else {
        mode_period = 500U;
    }

    l2_on = ((now_ms / mode_period) % 2U) == 0U ? 1U : 0U;
    BSP_SetLedL2(l2_on);
}

void App_Init(void)
{
    Remote_Init();
    Chassis_Init();
    Gimbal_Init();
    Safety_Init();
    g_last_control_ms = BSP_GetTickMs();
}

void App_Loop(void)
{
    uint32_t now_ms = BSP_GetTickMs();

    App_UpdateLed(now_ms, Remote_GetCommand());

    if ((now_ms - g_last_control_ms) >= ROBOT_CONTROL_PERIOD_MS) {
        g_last_control_ms = now_ms;
        App_ControlTask();
    }
}

void App_ControlTask(void)
{
    uint32_t now_ms = BSP_GetTickMs();
    float dt_s = (float)ROBOT_CONTROL_PERIOD_MS / 1000.0f;
    const remote_cmd_t *cmd;
    const chassis_t *chassis;
    const gimbal_t *gimbal;

    Remote_Update(now_ms);
    cmd = Remote_GetCommand();
    gimbal = Gimbal_GetState();
    Safety_Update(cmd, gimbal->pitch_target_deg, now_ms);

    if (Safety_ShouldStop() != 0U) {
        Chassis_Stop();
        Gimbal_Stop();
        return;
    }

    Gimbal_Control(cmd, dt_s);
    gimbal = Gimbal_GetState();
    Chassis_Control(cmd, gimbal->yaw_feedback_deg, dt_s);

    chassis = Chassis_GetState();
    BSP_DebugOnControlTick(cmd,
                           chassis->wheel_target,
                           chassis->wheel_output,
                           gimbal->yaw_target_deg,
                           gimbal->pitch_target_deg);
}
