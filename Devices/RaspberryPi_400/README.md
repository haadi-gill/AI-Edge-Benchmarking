## Operating System
Raspberry Pi OS (Legacy 64-bit) Debian Bullseye with Desktop environment and all freatures to allow flexability.
## Connection
SSH Configuration: Hostname: raspberrypi400sd Username: seniordesign Password: design
Connect with: ssh seniordesign@raspberrypi400sd enter username and password
Connect with application such as RealVNC Viewer to access desktop environment

## Hardware
* [Raspberry Pi 400](https://www.raspberrypi.com/products/raspberry-pi-400/)

## ML Model
* [TensorFlow Examples](https://github.com/tensorflow/examples/)

### Object Detection Model
* [Object Detection](https://github.com/tensorflow/examples/tree/master/lite/examples/object_detection/raspberry_pi)
* CNN architecture model that detects objects in video frame and identifies them with a confidence value.
* Video feed from USB webcam
* This model is using a virtual environment for dependencies
* Access virtual environment named tf
```
source tf/bin/activate
```
* Build and run model:
 ```
 sh setup.sh
 python3 detect.py --model efficientdet_lite0.tflite
 ```

### Audio Classification Model
* [Audio Classification](https://github.com/tensorflow/examples/tree/master/lite/examples/audio_classification/raspberry_pi)
* CNN architecture model that turns audio into spectrograms then uses image classification to detect general sound patterns such as speech, and specific sounds such as finger snaps
* Audio feed from USB microphone
* This model is using a virtual environment for dependencies
* Access virtual environment named tf
```
source tf/bin/activate
```
* Build and run model:
 ```
 sh setup.sh
 python3 classify.py --model yamnet.tflite --maxResults (x)
 ```

 ### Edge Impulse Model
 * Standardized edge impulse Rock, Paper, Scissors computer vision model. 
 * cd into edge impulse folder
 * run the following commands to run the model
 ```
 make
 sudo ./build/app
 ```

 ## Board Testing
 ### Powering Board
 Power come from Raspi transformer plugged into 120V outlet. (+5V supply). USB C connector goes into a breakout to connect to the breadboard. The multimeter is put into series on the breadboard with second USB C breakout. The second breakout runs to the board powering it.
 Peripherals such as keyboard, mouse, and monitor are plugged in while not testing the model.

### Pin Toggle
 A pin toggles high and low directly before and after the model is called to make an inference. The pin should be connected to the external trigger of the multimeter. When the pin toggles high, the inference begins and the multimeter records the current at the moment of inference. This ensures power measurements are during times of the model running. The toggles pin is GPIO 27, physical pin 13 on the 40 pin output.

 ### Script
 The script is a standard in the project as all members run it. It interfaces with the Digital Multimeter to measure current, which is then transformed into power. 

 ## WIP
* CPU Usage
 ```
 top > output.txt
 ```
* temperature
 ```
 vcgencmd measure_temp
 ```

 inference_log.csv saved the CPU usage and temperatue during model runtime.



 ## Issues
 * No current issues
 
 ## References
* [Paul McWhorter](https://www.youtube.com/watch?v=yE7Ve3U5Slw)
    - Setting up Raspi for Tensorflow | Writing new script using Object Detection Model
* [Ben | Lazy Tech](https://www.youtube.com/watch?v=kX6zWqMP9U4)
    - Quick Reference for running Object Detection on Raspi