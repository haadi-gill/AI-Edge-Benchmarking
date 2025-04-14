# MAX78000_FTHR

These models are used with the Maxim SDK software to test the features of the max78000 and its hardware accelerator.

## Requirements

### Hardware

MAX78000FTHR

### Software
Keyword Sensing
One example model is “KWS20”, a voice-sensing model that uses a CNN to classify audio signals into 20 different “keywords” (“up”, “one”, “two”, etc.). It makes use of the hardware accelerator and runs independently, inferencing any time a voice is detected.

Rock Paper Scissors
Another example model is “rps”, an image detection model that uses a CNN to classify images into either a rock, paper, or scissors. It makes use of the hardware accelerator and onboard camera, requiring the user to press a button to perform an inference.

## Building the application

### Compile

For third party models, use the "izer" tool to compile a trained model to make use of the hardware accelerator. A detailed description of this tool can be found at https://github.com/analogdevicesinc/MaximAI_Documentation.

### Flash

Use the tools in the Maxim SDK to build and flash to the device.