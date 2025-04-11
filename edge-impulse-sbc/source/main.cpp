#include <stdio.h>

#include "edge-impulse-sdk/classifier/ei_run_classifier.h"

// Callback function declaration
static int get_signal_data(size_t offset, size_t length, float *out_ptr);

// Raw features copied from test sample
static const float features[] = {
   196.1322, 114.3185, 34.2049, 71.7544, 179.6990, 188.4987, 72.8411, 15.3378, 119.9058, 227.0558, 168.1914, 41.8864, 46.4647, 176.6049, 275.7649, 286.7008, 276.7284, 283.6972, 288.1567, 286.5602, 287.1323, 286.3434, 288.4919, 293.8264, 291.0033, 286.9362, 288.5351, 285.9875, 288.8928, 291.6985, 280.7527, 293.1976, 309.0624, 245.3163, 146.5826, 91.9295, 44.4669, 42.0717, 168.9111, 261.8951, 138.2092, -9.7200, 68.3341, 217.2789, 186.1182, 77.4306, 61.7230, 62.4011, 48.6334, 140.8058, 278.1482, 272.7060, 156.8023, 92.5273, 91.2991, 81.9894, 72.4931, 71.2180, 56.6165, 78.7682, 163.7718, 214.6154 // Copy raw features here (e.g. from the 'Model testing' page)
};

int main(int argc, char **argv) {

    signal_t signal;            // Wrapper for raw input buffer
    ei_impulse_result_t result; // Used to store inference output
    EI_IMPULSE_ERROR res;       // Return code from inference

    // Calculate the length of the buffer
    size_t buf_len = sizeof(features) / sizeof(features[0]);

    // Make sure that the length of the buffer matches expected input length
    if (buf_len != EI_CLASSIFIER_DSP_INPUT_FRAME_SIZE) {
        ei_printf("ERROR: The size of the input buffer is not correct.\r\n");
        ei_printf("Expected %d items, but got %d\r\n",
                EI_CLASSIFIER_DSP_INPUT_FRAME_SIZE,
                (int)buf_len);
        return 1;
    }

    // Assign callback function to fill buffer used for preprocessing/inference
    signal.total_length = EI_CLASSIFIER_DSP_INPUT_FRAME_SIZE;
    signal.get_data = &get_signal_data;

    // Perform DSP pre-processing and inference
    int time;
    for(int i = 0; i < 100 ; i ++){
        res = run_classifier(&signal, &result, false);

           ei_printf("run_classifier returned: %d\r\n", res);
            ei_printf("Timing: DSP %d us, inference %d us, anomaly %d us\r\n",
            result.timing.dsp_us,
            result.timing.classification_us,
            result.timing.anomaly_us);
            time += result.timing.classification_us;
            ei_sleep(100);
    }
    time = time / 100;
    ei_printf("Average inf time = %d\r\n", res);





    // Print return code and how long it took to perform inferenc

    // Print the prediction results (object detection)
#if EI_CLASSIFIER_OBJECT_DETECTION == 1
    ei_printf("Object detection bounding boxes:\r\n");
    for (uint32_t i = 0; i < result.bounding_boxes_count; i++) {
        ei_impulse_result_bounding_box_t bb = result.bounding_boxes[i];
        if (bb.value == 0) {
            continue;
        }
        ei_printf("  %s (%f) [ x: %u, y: %u, width: %u, height: %u ]\r\n",
                bb.label,
                bb.value,
                bb.x,
                bb.y,
                bb.width,
                bb.height);
    }

    // Print the prediction results (classification)
#else
    ei_printf("Predictions:\r\n");
    for (uint16_t i = 0; i < EI_CLASSIFIER_LABEL_COUNT; i++) {
        ei_printf("  %s: ", ei_classifier_inferencing_categories[i]);
        ei_printf("%.5f\r\n", result.classification[i].value);
    }
#endif

    // Print anomaly result (if it exists)
#if EI_CLASSIFIER_HAS_ANOMALY
    ei_printf("Anomaly prediction: %.3f\r\n", result.anomaly);
#endif

#if EI_CLASSIFIER_HAS_VISUAL_ANOMALY
    ei_printf("Visual anomalies:\r\n");
    for (uint32_t i = 0; i < result.visual_ad_count; i++) {
        ei_impulse_result_bounding_box_t bb = result.visual_ad_grid_cells[i];
        if (bb.value == 0) {
            continue;
        }
        ei_printf("  %s (%f) [ x: %u, y: %u, width: %u, height: %u ]\r\n",
                bb.label,
                bb.value,
                bb.x,
                bb.y,
                bb.width,
                bb.height);
    }
    ei_printf("Visual anomaly values: Mean : %.3f Max : %.3f\r\n",
    result.visual_ad_result.mean_value, result.visual_ad_result.max_value);
#endif

    return 0;
}

// Callback: fill a section of the out_ptr buffer when requested
static int get_signal_data(size_t offset, size_t length, float *out_ptr) {
    for (size_t i = 0; i < length; i++) {
        out_ptr[i] = (features + offset)[i];
    }

    return EIDSP_OK;
}
