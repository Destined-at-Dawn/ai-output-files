#ifndef BSP_PORT_H
#define BSP_PORT_H

#include "robot_def.h"

#ifdef __cplusplus
extern "C" {
#endif

uint32_t BSP_GetTickMs(void);
uint8_t BSP_ReadKey(key_id_t key);

void BSP_SetMotorOutput(motor_id_t motor, float output);
float BSP_GetMotorSpeed(motor_id_t motor);

float BSP_GetYawAngleDeg(void);
float BSP_GetPitchAngleDeg(void);

void BSP_SetLedL1(float duty_0_to_1);
void BSP_SetLedL2(uint8_t on);

void BSP_DebugOnControlTick(const remote_cmd_t *cmd,
                            const float wheel_target[CHASSIS_WHEEL_COUNT],
                            const float wheel_output[CHASSIS_WHEEL_COUNT],
                            float yaw_target,
                            float pitch_target);

#ifdef __cplusplus
}
#endif

#endif
