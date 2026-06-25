#include "gimbal.h"
#include "bsp_port.h"

static gimbal_t g_gimbal;

void Gimbal_Init(void)
{
    g_gimbal.yaw_target_deg = 0.0f;
    g_gimbal.pitch_target_deg = 0.0f;
    g_gimbal.yaw_feedback_deg = 0.0f;
    g_gimbal.pitch_feedback_deg = 0.0f;
    g_gimbal.yaw_output = 0.0f;
    g_gimbal.pitch_output = 0.0f;

    PID_Init(&g_gimbal.yaw_pid,
             18.0f,
             0.0f,
             0.8f,
             -GIMBAL_OUTPUT_LIMIT,
             GIMBAL_OUTPUT_LIMIT,
             -100.0f,
             100.0f);

    PID_Init(&g_gimbal.pitch_pid,
             20.0f,
             0.0f,
             0.8f,
             -GIMBAL_OUTPUT_LIMIT,
             GIMBAL_OUTPUT_LIMIT,
             -100.0f,
             100.0f);
}

void Gimbal_Stop(void)
{
    PID_Reset(&g_gimbal.yaw_pid);
    PID_Reset(&g_gimbal.pitch_pid);
    g_gimbal.yaw_output = 0.0f;
    g_gimbal.pitch_output = 0.0f;
    BSP_SetMotorOutput(MOTOR_GIMBAL_YAW, 0.0f);
    BSP_SetMotorOutput(MOTOR_GIMBAL_PITCH, 0.0f);
}

void Gimbal_Control(const remote_cmd_t *cmd, float dt_s)
{
    float yaw_error;
    float pitch_error;

    if (cmd == 0 || cmd->robot_mode == ROBOT_STOP || cmd->valid == 0U) {
        Gimbal_Stop();
        return;
    }

    if (cmd->yaw_step_positive != 0U) {
        g_gimbal.yaw_target_deg = Robot_WrapAngleDeg(g_gimbal.yaw_target_deg + GIMBAL_YAW_STEP_DEG);
    }

    if (cmd->pitch_step_positive != 0U) {
        g_gimbal.pitch_target_deg += GIMBAL_PITCH_STEP_DEG;
        g_gimbal.pitch_target_deg = Robot_LimitFloat(g_gimbal.pitch_target_deg,
                                                     GIMBAL_PITCH_MIN_DEG,
                                                     GIMBAL_PITCH_MAX_DEG);
    }

    g_gimbal.yaw_feedback_deg = BSP_GetYawAngleDeg();
    g_gimbal.pitch_feedback_deg = BSP_GetPitchAngleDeg();

    yaw_error = Robot_WrapAngleDeg(g_gimbal.yaw_target_deg - g_gimbal.yaw_feedback_deg);
    pitch_error = g_gimbal.pitch_target_deg - g_gimbal.pitch_feedback_deg;

    g_gimbal.yaw_output = PID_Calc(&g_gimbal.yaw_pid, yaw_error, 0.0f, dt_s);
    g_gimbal.pitch_output = PID_Calc(&g_gimbal.pitch_pid, pitch_error, 0.0f, dt_s);

    g_gimbal.yaw_output = Robot_LimitFloat(g_gimbal.yaw_output,
                                           -GIMBAL_OUTPUT_LIMIT,
                                           GIMBAL_OUTPUT_LIMIT);
    g_gimbal.pitch_output = Robot_LimitFloat(g_gimbal.pitch_output,
                                             -GIMBAL_OUTPUT_LIMIT,
                                             GIMBAL_OUTPUT_LIMIT);

    BSP_SetMotorOutput(MOTOR_GIMBAL_YAW, g_gimbal.yaw_output);
    BSP_SetMotorOutput(MOTOR_GIMBAL_PITCH, g_gimbal.pitch_output);
}

const gimbal_t *Gimbal_GetState(void)
{
    return &g_gimbal;
}
