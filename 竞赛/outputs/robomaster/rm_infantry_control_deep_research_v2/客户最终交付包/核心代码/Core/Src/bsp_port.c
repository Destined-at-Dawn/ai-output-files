#include "bsp_port.h"

/*
 * Hardware adapter layer.
 * Replace these stubs with real STM32 HAL code in your CubeMX project.
 */

uint32_t BSP_GetTickMs(void)
{
    /*
     * STM32 HAL project:
     * return HAL_GetTick();
     */
    return 0U;
}

uint8_t BSP_ReadKey(key_id_t key)
{
    (void)key;
    /*
     * Return 1 when pressed, 0 when released.
     * Example:
     * return HAL_GPIO_ReadPin(KEY1_GPIO_Port, KEY1_Pin) == GPIO_PIN_RESET;
     */
    return 0U;
}

void BSP_SetMotorOutput(motor_id_t motor, float output)
{
    (void)motor;
    (void)output;
    /*
     * PWM motor:
     * 1. limit direction
     * 2. set GPIO direction pin
     * 3. set TIM compare value
     *
     * CAN motor:
     * 1. pack current command
     * 2. send CAN frame
     */
}

float BSP_GetMotorSpeed(motor_id_t motor)
{
    (void)motor;
    /*
     * Return encoder speed in your own unit.
     * Keep target speed and feedback speed in the same unit.
     */
    return 0.0f;
}

float BSP_GetYawAngleDeg(void)
{
    /*
     * Return IMU yaw angle in degree.
     */
    return 0.0f;
}

float BSP_GetPitchAngleDeg(void)
{
    /*
     * Return IMU pitch angle in degree.
     */
    return 0.0f;
}

void BSP_SetLedL1(float duty_0_to_1)
{
    (void)duty_0_to_1;
    /*
     * Use PWM or software PWM for breathing LED.
     */
}

void BSP_SetLedL2(uint8_t on)
{
    (void)on;
    /*
     * HAL_GPIO_WritePin(L2_GPIO_Port, L2_Pin, on ? GPIO_PIN_SET : GPIO_PIN_RESET);
     */
}

void BSP_DebugOnControlTick(const remote_cmd_t *cmd,
                            const float wheel_target[CHASSIS_WHEEL_COUNT],
                            const float wheel_output[CHASSIS_WHEEL_COUNT],
                            float yaw_target,
                            float pitch_target)
{
    (void)cmd;
    (void)wheel_target;
    (void)wheel_output;
    (void)yaw_target;
    (void)pitch_target;
    /*
     * Optional: print variables through UART, SWO, or watch them in debugger.
     */
}
