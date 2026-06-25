#ifndef ROBOT_DEF_H
#define ROBOT_DEF_H

#include <stdint.h>

#ifdef __cplusplus
extern "C" {
#endif

#define ROBOT_CONTROL_PERIOD_MS       5U
#define ROBOT_REMOTE_TIMEOUT_MS       300U

#define CHASSIS_WHEEL_COUNT           4U
#define CHASSIS_MAX_VX                3000.0f
#define CHASSIS_MAX_VY                3000.0f
#define CHASSIS_MAX_WZ                180.0f
#define CHASSIS_SPIN_WZ               90.0f
#define CHASSIS_FOLLOW_KP             2.0f
#define CHASSIS_GEOMETRY_K            1.0f
#define MOTOR_OUTPUT_LIMIT            1000.0f

#define GIMBAL_YAW_STEP_DEG           5.0f
#define GIMBAL_PITCH_STEP_DEG         3.0f
#define GIMBAL_PITCH_MIN_DEG          (-20.0f)
#define GIMBAL_PITCH_MAX_DEG          30.0f
#define GIMBAL_OUTPUT_LIMIT           1000.0f

#define REMOTE_DEBOUNCE_MS            20U
#define REMOTE_LONG_PRESS_MS          500U
#define REMOTE_REPEAT_MS              100U

typedef enum {
    ROBOT_STOP = 0,
    ROBOT_NORMAL = 1
} robot_mode_t;

typedef enum {
    CHASSIS_INDEPENDENT = 0,
    CHASSIS_SPIN = 1,
    CHASSIS_FOLLOW_GIMBAL = 2
} chassis_mode_t;

typedef enum {
    KEY_ID_1 = 0,
    KEY_ID_2,
    KEY_ID_3,
    KEY_ID_STOP,
    KEY_ID_COUNT
} key_id_t;

typedef enum {
    MOTOR_CHASSIS_FL = 0,
    MOTOR_CHASSIS_FR,
    MOTOR_CHASSIS_BL,
    MOTOR_CHASSIS_BR,
    MOTOR_GIMBAL_YAW,
    MOTOR_GIMBAL_PITCH,
    MOTOR_COUNT
} motor_id_t;

typedef struct {
    float vx;
    float vy;
    float wz;
} chassis_speed_t;

typedef struct {
    robot_mode_t robot_mode;
    chassis_mode_t chassis_mode;
    chassis_speed_t chassis_speed;
    uint8_t yaw_step_positive;
    uint8_t pitch_step_positive;
    uint8_t emergency_toggle;
    uint8_t valid;
    uint32_t last_update_ms;
} remote_cmd_t;

static inline float Robot_LimitFloat(float value, float min_value, float max_value)
{
    if (value > max_value) {
        return max_value;
    }
    if (value < min_value) {
        return min_value;
    }
    return value;
}

static inline float Robot_AbsFloat(float value)
{
    return (value >= 0.0f) ? value : -value;
}

static inline float Robot_WrapAngleDeg(float angle)
{
    while (angle > 180.0f) {
        angle -= 360.0f;
    }
    while (angle < -180.0f) {
        angle += 360.0f;
    }
    return angle;
}

#ifdef __cplusplus
}
#endif

#endif
