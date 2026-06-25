#ifndef SAFETY_H
#define SAFETY_H

#include "remote.h"

#ifdef __cplusplus
extern "C" {
#endif

typedef struct {
    uint8_t robot_stop;
    uint8_t remote_lost;
    uint8_t pitch_out_of_range;
    uint8_t motor_output_limited;
    uint32_t last_check_ms;
} safety_state_t;

void Safety_Init(void);
void Safety_Update(const remote_cmd_t *cmd, float pitch_target_deg, uint32_t now_ms);
uint8_t Safety_ShouldStop(void);
void Safety_ReportMotorLimited(uint8_t limited);
const safety_state_t *Safety_GetState(void);

#ifdef __cplusplus
}
#endif

#endif
