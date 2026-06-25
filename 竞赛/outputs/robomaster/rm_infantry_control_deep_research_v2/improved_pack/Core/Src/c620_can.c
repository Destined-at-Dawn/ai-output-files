#include "c620_can.h"

int16_t C620_LimitCurrent(int32_t current)
{
    if (current > C620_CURRENT_MAX) {
        return C620_CURRENT_MAX;
    }
    if (current < C620_CURRENT_MIN) {
        return C620_CURRENT_MIN;
    }
    return (int16_t)current;
}

void C620_PackCurrentFrame(uint16_t tx_id, const int16_t current[4], can_frame_t *frame)
{
    uint32_t i;

    if (current == 0 || frame == 0) {
        return;
    }

    frame->std_id = tx_id;
    frame->dlc = 8U;

    for (i = 0U; i < 4U; i++) {
        int16_t limited = C620_LimitCurrent(current[i]);
        frame->data[i * 2U] = (uint8_t)(((uint16_t)limited >> 8) & 0xFFU);
        frame->data[i * 2U + 1U] = (uint8_t)((uint16_t)limited & 0xFFU);
    }
}

uint8_t C620_ParseFeedback(uint16_t std_id, const uint8_t data[8], c620_feedback_t *feedback)
{
    uint8_t esc_id;

    if (data == 0 || feedback == 0) {
        return 0U;
    }

    if (std_id < 0x201U || std_id > 0x208U) {
        return 0U;
    }

    esc_id = (uint8_t)(std_id - C620_CAN_FEEDBACK_ID_BASE);

    feedback->esc_id = esc_id;
    feedback->angle_raw = (uint16_t)(((uint16_t)data[0] << 8) | data[1]);
    feedback->speed_rpm = (int16_t)(((uint16_t)data[2] << 8) | data[3]);
    feedback->torque_current = (int16_t)(((uint16_t)data[4] << 8) | data[5]);
    feedback->temperature_c = data[6];
    feedback->updated = 1U;

    return 1U;
}

float C620_AngleRawToDeg(uint16_t angle_raw)
{
    return ((float)angle_raw * 360.0f) / (float)(C620_ANGLE_RAW_MAX + 1U);
}
