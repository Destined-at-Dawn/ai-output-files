#ifndef C620_CAN_H
#define C620_CAN_H

#include <stdint.h>

#ifdef __cplusplus
extern "C" {
#endif

#define C620_CAN_TX_ID_GROUP_1        0x200U
#define C620_CAN_TX_ID_GROUP_2        0x1FFU
#define C620_CAN_FEEDBACK_ID_BASE     0x200U
#define C620_CURRENT_MIN              (-16384)
#define C620_CURRENT_MAX              16384
#define C620_ANGLE_RAW_MAX            8191U

typedef struct {
    uint16_t std_id;
    uint8_t dlc;
    uint8_t data[8];
} can_frame_t;

typedef struct {
    uint8_t esc_id;
    uint16_t angle_raw;
    int16_t speed_rpm;
    int16_t torque_current;
    uint8_t temperature_c;
    uint8_t updated;
} c620_feedback_t;

int16_t C620_LimitCurrent(int32_t current);
void C620_PackCurrentFrame(uint16_t tx_id, const int16_t current[4], can_frame_t *frame);
uint8_t C620_ParseFeedback(uint16_t std_id, const uint8_t data[8], c620_feedback_t *feedback);
float C620_AngleRawToDeg(uint16_t angle_raw);

#ifdef __cplusplus
}
#endif

#endif
