#ifndef REMOTE_H
#define REMOTE_H

#include "robot_def.h"

#ifdef __cplusplus
extern "C" {
#endif

typedef struct {
    uint8_t stable_pressed;
    uint8_t last_raw;
    uint8_t short_event;
    uint8_t long_event;
    uint8_t repeat_event;
    uint32_t raw_changed_ms;
    uint32_t press_start_ms;
    uint32_t last_repeat_ms;
} remote_button_t;

void Remote_Init(void);
void Remote_Update(uint32_t now_ms);
const remote_cmd_t *Remote_GetCommand(void);
uint8_t Remote_ParseUartFrame(const uint8_t *data, uint16_t len, remote_cmd_t *out_cmd);

#ifdef __cplusplus
}
#endif

#endif
