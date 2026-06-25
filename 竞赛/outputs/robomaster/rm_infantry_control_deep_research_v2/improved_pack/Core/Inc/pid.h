#ifndef PID_H
#define PID_H

#include "robot_def.h"

#ifdef __cplusplus
extern "C" {
#endif

typedef struct {
    float kp;
    float ki;
    float kd;
    float integral;
    float prev_error;
    float out_min;
    float out_max;
    float integral_min;
    float integral_max;
} pid_t;

void PID_Init(pid_t *pid,
              float kp,
              float ki,
              float kd,
              float out_min,
              float out_max,
              float integral_min,
              float integral_max);
void PID_Reset(pid_t *pid);
float PID_Calc(pid_t *pid, float target, float feedback, float dt_s);

#ifdef __cplusplus
}
#endif

#endif
