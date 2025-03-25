from pathlib import Path
import socket 
import time
import math
import pandas
import logging
from datetime import datetime
import matplotlib.pyplot as plt
import os

MM_Data = {
    'ip_addr' : ('10.245.26.233', 5555),
    'curr_dc' : ':MEAS:CURR:DC?\n'
}

print("Attempting to connect to IP address: ", MM_Data['ip_addr'])

try:
    # SCOPE_SOCKET = socket.create_connection(MSO2302A_DATA['ip_addr'])
    MM_SOCKET = socket.create_connection(MM_Data['ip_addr'])
except Exception as err:
    print("Connection failed. See log for more details.")
    exit() 
    
MM_SOCKET.settimeout(10.0)
RECV_MAX_BYTES = 1024

#Set trigger to auto for idle current 
MM_SOCKET.send(bytes(":TRIG:SOUR AUTO\n", "utf_8"))
time.sleep(0.5)

input("\nPress enter to begin idle current draw...\n")

idle_current = 0
idle_iterations = 20
inferences_measured = 10

for j in range(idle_iterations):
    # Query the Multimeter
    MM_SOCKET.send(bytes(MM_Data['curr_dc'], 'utf_8'))
    # Read and store the value 
    data_in = (bytes.decode(MM_SOCKET.recv(1024), 'utf_8'))
    idle_current += float(data_in.strip()) * (1/idle_iterations)

print("Idle current draw: ", idle_current)

#Set trigger to external (rising edge) for inferencing current 
MM_SOCKET.send(bytes(":TRIG:SOUR EXT\n", "utf_8"))
time.sleep(0.5)
MM_SOCKET.send(bytes(":TRIG:EXT RISE\n", "utf_8"))
time.sleep(0.5)

print("\nBeginning precise power measurements for %d inferences\n" % inferences_measured)

inferences = 0
readings = []

while (inferences < inferences_measured) :
    # Query the Multimeter
    MM_SOCKET.send(bytes(":MEAS:CURR:DC?\n", 'utf_8'))
    # Read and store the value 
    data_in = (bytes.decode(MM_SOCKET.recv(1024), 'utf_8'))
    readings.append(data_in.strip())
    inferences += 1
    print("Inference %d recorded." % inferences)

print(readings)