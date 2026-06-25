#include "pid.h"

void PID_Init(pid_t *pid,
              float kp,
              float ki,
              float kd,
              float out_min,
              float out_max,
              float integral_min,
              float integral_max)
{
    if (pid == 0) {
        return;
    }

    pid->kp = kp;
    pid->ki = ki;
    pid->kd = kd;
    pid->integral = 0.0f;
    pid->prev_error = 0.0f;
    pid->out_min = out_min;
    pid->out_max = out_max;
    pid->integral_min = integral_min;
    pid->integral_max = integral_max;
}

void PID_Reset(pid_t *pid)
{
    if (pid == 0) {
        return;
    }

    pid->integral = 0.0f;
    pid->prev_error = 0.0f;
}

float PID_Calc(pid_t *pid, float target, float feedback, float dt_s)
{
    float error;
    float derivative;
    float output;

    if (pid == 0 || dt_s <= 0.0f) {
        return 0.0f;
    }

    error = target - feedback;
    pid->integral += error * dt_s;
    pid->integral = Robot_LimitFloat(pid->integral, pid->integral_min, pid->integral_max);

    derivative = (error - pid->prev_error) / dt_s;
    pid->prev_error = error;

    output = pid->kp * error + pid->ki * pid->integral + pid->kd * derivative;
    return Robot_LimitFloat(output, pid->out_min, pid->out_max);
}
