from pathlib import Path
import socket 
import time
import math
import pandas
import logging
from datetime import datetime
import matplotlib.pyplot as plt
import os
import csv

#config_df = pandas.read_excel("Scripts/config.xlsx")
config_df = pandas.read_excel("Scripts/config_Raspi400.xlsx")
config_df.drop(columns=["Description", "Flag", "Unnamed: 4", "Flag Values"], inplace=True)


def config_value(label):
    
    return config_df[config_df['Name'] == label].reset_index()["Value"][0]

MM_Data = {
    #'ip_addr' : ('10.245.26.218', 5555),
    'ip_addr' : ('10.245.26.74', 5555),
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

idle_iterations = config_value('idle_iterations')
inferences_measured = config_value('inferences_measured')
inference_time = config_value('inference_time')
board_name = config_value('board_name')
test_label = config_value('test_label')
voltage = config_value('voltage')
filepath = config_value('data_filepath')

idle_current = 0

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

input("\nPress enter when ready to execute %d inferences\n" % inferences_measured)

inferences = 0
average_current = 0

while (inferences < inferences_measured) :
    # Query the Multimeter
    MM_SOCKET.send(bytes(":MEAS:CURR:DC?\n", 'utf_8'))
    # Read and store the value 
    data_in = (bytes.decode(MM_SOCKET.recv(1024), 'utf_8'))
    average_current += ((float(data_in.strip()) - idle_current) * (1/inferences_measured))
    inferences += 1
    print("Inference %d recorded." % inferences)

average_power = average_current * voltage
energy = average_power * inference_time
score = 1 / energy

data = [board_name, test_label, inference_time, average_power, energy, score]

if (filepath == 'DEFAULT') :
    filepath = f'./{board_name}/{test_label}'

print(filepath)
if not os.path.exists(filepath):
    os.makedirs(filepath, exist_ok=True)

with open(f'{filepath}/out.csv', 'w', newline='') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(data)
