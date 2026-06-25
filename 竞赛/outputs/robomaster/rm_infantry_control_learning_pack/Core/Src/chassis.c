#include "chassis.h"
#include "bsp_port.h"

static chassis_t g_chassis;

static motor_id_t WheelIndexToMotor(uint32_t index)
{
    static const motor_id_t table[CHASSIS_WHEEL_COUNT] = {
        MOTOR_CHASSIS_FL,
        MOTOR_CHASSIS_FR,
        MOTOR_CHASSIS_BL,
        MOTOR_CHASSIS_BR
    };
    return table[index];
}

static void Chassis_CalcWheelTarget(const chassis_speed_t *speed, float wheel[CHASSIS_WHEEL_COUNT])
{
    float vx = Robot_LimitFloat(speed->vx, -CHASSIS_MAX_VX, CHASSIS_MAX_VX);
    float vy = Robot_LimitFloat(speed->vy, -CHASSIS_MAX_VY, CHASSIS_MAX_VY);
    float wz = Robot_LimitFloat(speed->wz, -CHASSIS_MAX_WZ, CHASSIS_MAX_WZ);
    float k = CHASSIS_GEOMETRY_K;

    wheel[0] = +vx - vy - wz * k;
    wheel[1] = +vx + vy + wz * k;
    wheel[2] = -vx + vy - wz * k;
    wheel[3] = -vx - vy + wz * k;
}

void Chassis_Init(void)
{
    uint32_t i;

    g_chassis.mode = CHASSIS_INDEPENDENT;
    g_chassis.target_speed.vx = 0.0f;
    g_chassis.target_speed.vy = 0.0f;
    g_chassis.target_speed.wz = 0.0f;

    for (i = 0U; i < CHASSIS_WHEEL_COUNT; i++) {
        g_chassis.wheel_target[i] = 0.0f;
        g_chassis.wheel_feedback[i] = 0.0f;
        g_chassis.wheel_output[i] = 0.0f;
        PID_Init(&g_chassis.speed_pid[i],
                 0.6f,
                 0.05f,
                 0.0f,
                 -MOTOR_OUTPUT_LIMIT,
                 MOTOR_OUTPUT_LIMIT,
                 -3000.0f,
                 3000.0f);
    }
}

void Chassis_Stop(void)
{
    uint32_t i;

    g_chassis.target_speed.vx = 0.0f;
    g_chassis.target_speed.vy = 0.0f;
    g_chassis.target_speed.wz = 0.0f;

    for (i = 0U; i < CHASSIS_WHEEL_COUNT; i++) {
        g_chassis.wheel_target[i] = 0.0f;
        g_chassis.wheel_output[i] = 0.0f;
        PID_Reset(&g_chassis.speed_pid[i]);
        BSP_SetMotorOutput(WheelIndexToMotor(i), 0.0f);
    }
}

void Chassis_Control(const remote_cmd_t *cmd, float yaw_angle_deg, float dt_s)
{
    uint32_t i;
    chassis_speed_t speed;

    if (cmd == 0 || cmd->robot_mode == ROBOT_STOP || cmd->valid == 0U) {
        Chassis_Stop();
        return;
    }

    g_chassis.mode = cmd->chassis_mode;
    speed = cmd->chassis_speed;

    if (g_chassis.mode == CHASSIS_SPIN) {
        speed.wz = CHASSIS_SPIN_WZ;
    } else if (g_chassis.mode == CHASSIS_FOLLOW_GIMBAL) {
        float yaw_error = Robot_WrapAngleDeg(0.0f - yaw_angle_deg);
        speed.wz = Robot_LimitFloat(yaw_error * CHASSIS_FOLLOW_KP, -CHASSIS_MAX_WZ, CHASSIS_MAX_WZ);
    }

    g_chassis.target_speed = speed;
    Chassis_CalcWheelTarget(&g_chassis.target_speed, g_chassis.wheel_target);

    for (i = 0U; i < CHASSIS_WHEEL_COUNT; i++) {
        g_chassis.wheel_feedback[i] = BSP_GetMotorSpeed(WheelIndexToMotor(i));
        g_chassis.wheel_output[i] = PID_Calc(&g_chassis.speed_pid[i],
                                             g_chassis.wheel_target[i],
                                             g_chassis.wheel_feedback[i],
                                             dt_s);
        g_chassis.wheel_output[i] = Robot_LimitFloat(g_chassis.wheel_output[i],
                                                     -MOTOR_OUTPUT_LIMIT,
                                                     MOTOR_OUTPUT_LIMIT);
        BSP_SetMotorOutput(WheelIndexToMotor(i), g_chassis.wheel_output[i]);
    }
}

const chassis_t *Chassis_GetState(void)
{
    return &g_chassis;
}
