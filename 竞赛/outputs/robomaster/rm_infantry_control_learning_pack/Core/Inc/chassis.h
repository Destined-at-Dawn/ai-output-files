#ifndef CHASSIS_H
#define CHASSIS_H

#include "pid.h"
#include "remote.h"

#ifdef __cplusplus
extern "C" {
#endif

typedef struct {
    chassis_mode_t mode;
    chassis_speed_t target_speed;
    float wheel_target[CHASSIS_WHEEL_COUNT];
    float wheel_feedback[CHASSIS_WHEEL_COUNT];
    float wheel_output[CHASSIS_WHEEL_COUNT];
    pid_t speed_pid[CHASSIS_WHEEL_COUNT];
} chassis_t;

void Chassis_Init(void);
void Chassis_Control(const remote_cmd_t *cmd, float yaw_angle_deg, float dt_s);
void Chassis_Stop(void);
const chassis_t *Chassis_GetState(void);

#ifdef __cplusplus
}
#endif

#endif
