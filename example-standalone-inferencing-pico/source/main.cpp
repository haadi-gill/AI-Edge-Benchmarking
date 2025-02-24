#include "edge-impulse-sdk/classifier/ei_run_classifier.h"

#include <hardware/gpio.h>
#include <hardware/uart.h>
#include <pico/stdio_usb.h>
#include <stdio.h>

const uint LED_PIN = 25;
const uint 

static const float features[] = {
   196.1322, 114.3185, 34.2049, 71.7544, 179.6990, 188.4987, 72.8411, 15.3378, 119.9058, 227.0558, 168.1914, 41.8864, 46.4647, 176.6049, 275.7649, 286.7008, 276.7284, 283.6972, 288.1567, 286.5602, 287.1323, 286.3434, 288.4919, 293.8264, 291.0033, 286.9362, 288.5351, 285.9875, 288.8928, 291.6985, 280.7527, 293.1976, 309.0624, 245.3163, 146.5826, 91.9295, 44.4669, 42.0717, 168.9111, 261.8951, 138.2092, -9.7200, 68.3341, 217.2789, 186.1182, 77.4306, 61.7230, 62.4011, 48.6334, 140.8058, 278.1482, 272.7060, 156.8023, 92.5273, 91.2991, 81.9894, 72.4931, 71.2180, 56.6165, 78.7682, 163.7718, 214.6154
};

int raw_feature_get_data(size_t offset, size_t length, float *out_ptr) {
  memcpy(out_ptr, features + offset, length * sizeof(float));
  return 0;
}

void print_inference_result(ei_impulse_result_t result) {

    // Print how long it took to perform inference
    ei_printf("Timing: DSP %d ms, inference %d ms, anomaly %d ms\r\n",
            result.timing.dsp,
            result.timing.classification,
            result.timing.anomaly);

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
#if EI_CLASSIFIER_HAS_ANOMALY == 1
    ei_printf("Anomaly prediction: %.3f\r\n", result.anomaly);
#endif

}

int main() {
    stdio_usb_init();

    gpio_init(LED_PIN);
    gpio_set_dir(LED_PIN, GPIO_OUT);

    ei_impulse_result_t result = {nullptr};

    ei_printf("Edge Impulse standalone inferencing (Raspberry Pi Pico)\n");

    if (sizeof(features) / sizeof(float) != EI_CLASSIFIER_DSP_INPUT_FRAME_SIZE) {
        ei_printf("The size of your 'features' array is not correct. Expected %d items, but had %u\n",
        EI_CLASSIFIER_DSP_INPUT_FRAME_SIZE, sizeof(features) / sizeof(float));
        return 1;
    }

    while (true) {
        // blink LED
        gpio_put(LED_PIN, !gpio_get(LED_PIN));

        // the features are stored into flash, and we don't want to load everything into RAM
        signal_t features_signal;
        features_signal.total_length = sizeof(features) / sizeof(features[0]);
        features_signal.get_data = &raw_feature_get_data;

        // invoke the impulse
        EI_IMPULSE_ERROR res = run_classifier(&features_signal, &result, false /* debug */);
        if (res != EI_IMPULSE_OK) {
            ei_printf("ERR: Failed to run classifier (%d)\n", res);
            return res;
        }

        print_inference_result(result);
        ei_sleep(2000);
    }
}