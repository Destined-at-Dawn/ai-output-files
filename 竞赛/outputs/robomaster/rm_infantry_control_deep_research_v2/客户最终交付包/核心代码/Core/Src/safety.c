#include "safety.h"

static safety_state_t g_safety;

void Safety_Init(void)
{
    g_safety.robot_stop = 1U;
    g_safety.remote_lost = 0U;
    g_safety.pitch_out_of_range = 0U;
    g_safety.motor_output_limited = 0U;
    g_safety.last_check_ms = 0U;
}

void Safety_Update(const remote_cmd_t *cmd, float pitch_target_deg, uint32_t now_ms)
{
    g_safety.last_check_ms = now_ms;

    if (cmd == 0 || cmd->valid == 0U) {
        g_safety.remote_lost = 1U;
        g_safety.robot_stop = 1U;
        return;
    }

    g_safety.remote_lost = ((now_ms - cmd->last_update_ms) > ROBOT_REMOTE_TIMEOUT_MS) ? 1U : 0U;
    g_safety.robot_stop = (cmd->robot_mode == ROBOT_STOP || g_safety.remote_lost != 0U) ? 1U : 0U;

    g_safety.pitch_out_of_range =
        (pitch_target_deg < GIMBAL_PITCH_MIN_DEG || pitch_target_deg > GIMBAL_PITCH_MAX_DEG) ? 1U : 0U;
}

uint8_t Safety_ShouldStop(void)
{
    return (g_safety.robot_stop != 0U || g_safety.remote_lost != 0U) ? 1U : 0U;
}

void Safety_ReportMotorLimited(uint8_t limited)
{
    g_safety.motor_output_limited = limited;
}

const safety_state_t *Safety_GetState(void)
{
    return &g_safety;
}
