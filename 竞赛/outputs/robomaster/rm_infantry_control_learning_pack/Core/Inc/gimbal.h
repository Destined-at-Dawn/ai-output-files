#ifndef GIMBAL_H
#define GIMBAL_H

#include "pid.h"
#include "remote.h"

#ifdef __cplusplus
extern "C" {
#endif

typedef struct {
    float yaw_target_deg;
    float pitch_target_deg;
    float yaw_feedback_deg;
    float pitch_feedback_deg;
    float yaw_output;
    float pitch_output;
    pid_t yaw_pid;
    pid_t pitch_pid;
} gimbal_t;

void Gimbal_Init(void);
void Gimbal_Control(const remote_cmd_t *cmd, float dt_s);
void Gimbal_Stop(void);
const gimbal_t *Gimbal_GetState(void);

#ifdef __cplusplus
}
#endif

#endif
