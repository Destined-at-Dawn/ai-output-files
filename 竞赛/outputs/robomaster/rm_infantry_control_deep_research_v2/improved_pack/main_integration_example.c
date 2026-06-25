/*
 * Do not copy this file over CubeMX generated main.c blindly.
 * Use it as an integration example.
 */

#include "main.h"
#include "app.h"

int main(void)
{
    HAL_Init();
    SystemClock_Config();

    MX_GPIO_Init();
    MX_TIM1_Init();
    MX_TIM2_Init();
    MX_USART1_UART_Init();

    App_Init();

    while (1) {
        App_Loop();
    }
}
