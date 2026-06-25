#ifndef APP_H
#define APP_H

#include "robot_def.h"

#ifdef __cplusplus
extern "C" {
#endif

void App_Init(void);
void App_Loop(void);
void App_ControlTask(void);

#ifdef __cplusplus
}
#endif

#endif
