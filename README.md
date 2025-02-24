# AI Edge Benchmarking

## Introduction
Welcome to the repository for the AI Edge Benchmarking team!

Our goal is to create a standardized benchmarking process for Edge AI Applications, measuring metrics like inference time, power draw, and energy in order to see how different hardware compares in running AI.

## Current Features
Using the "EdgeImpulse" framework, we are able to have a standardized set of models that can target a variety of boards. These models can be compiled into simple c++ programs that record a precise measurement of inferencing time.

Using the `benchmarking.py` script, we are able to record:
- Current
- Power
- Energy

Raw values are stored in addition to offset values, which come from isolating spikes from idle power consumption. This is more impactful for larger boards such as those in the single board computer class. A pin toggle feature is also used to ensure that power measurements 

## Current State
### List of Current Boards
- Raspberry Pi Pico
- Raspberry Pi Zero
- MAX78000FTHR
### List of In-Progress/Future Boards
- BeagleBone AI-64

## Current Issues
- Due to multimeter polling rate and network latency, it is not recommended to use the script for models with an inference time of 100ms or below. Smaller models can be repeated many times in succession to fix this problem and provide more precise measurements.

## Procedures
### Measuring Inference Time: Using EdgeImpulse
With Edge Impulse models, measuring inference time is a fully standardized process. Before and after invoking the model, a timer is captured. The elapsed time is stored and transported using serial communication or viewed in a terminal in the case of single-board computers.  

### Measuring Power and Energy: Using `benchmarking.py`
The `benchmarking.py` script provides a standardized process for measuring inferencing power draw and energy consumption. It can be used with any board that has an external power source option and a GPIO pin that can be toggled on and off.
The procedure for using this script is described below:
1. Set up the hardware as shown in the image below. The power supply positive terminal is connected to the board Vin. The multimeter positive terminal is connected to board GND. The oscilloscope positive terminal is connected to the board pin toggle. All of the negative terminals are connected together. 

![screenshot](Images/setup.png)

2. Set the power supply to provide the correct voltage to your board. This voltage should remain constant during testing.
3. Run the script and provide all information when prompted (such as device IP addresses and operating voltage). 
4. Answer "Y" when asked to use the pin toggle feature if you would like to ensure synchronization of inferencing and measuring.
5. The script should successfully connect to the devices.
6. Ensure that the board is not inferencing, and when prompted, allow the script to take a measurement of the board's idle current.
7. For three trials, begin the board's inferencing and then start the trial on the script. Reset the board after each trial for best results.
8. Graphs will be printed for each of the three trials showing raw power, offset power (with idle power removed), and pin toggle data.
9. When using the pin toggle feature, additional statistics will be printed to the terminal showing measured inference time, average power while inferencing, and energy consumed by inferencing.