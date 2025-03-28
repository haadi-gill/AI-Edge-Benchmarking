from pathlib import Path
import socket 
import time
import math
import pandas
import logging
from datetime import datetime
import matplotlib.pyplot as plt
import os
import statistics
import csv

"""

    This script is used to configure the MSO2302A oscilloscope in order to obtain readings of the power consumption of differnet boards.
    
    Power will be obtained by measuring current fluctuations across a constant voltage source.
    
    Procedure:
    [INSERT DETAILS ABOUT HOW WE ARE SETTING UP, GATHERING DATA, AND STORING IT]
    Export format: 
        raw data - CSV
        plots - pngs of graphs, power over time
        

"""


config_df = pandas.read_excel("Scripts/config.xlsx")
config_df.drop(columns=["Description", "Flag", "Unnamed: 4", "Flag Values"], inplace=True)


def config_value(label):
    
    return config_df[config_df['Name'] == label].reset_index()["Value"][0]


# Dictionary of information for the oscilloscope
OS_Data = {
    'ip_addr': ('10.245.26.87', 5555),
    'chan1_vpp':':MEAS:VPP? CHAN1\n',
    'chan2_vpp':':MEAS:VPP? CHAN2\n',
    'chan1_freq':':MEAS:FREQ? CHAN1\n',
    'chan2_freq':':MEAS:FREQ? CHAN2\n',
    'rphase': ':MEAS:RPH? CHAN1,CHAN2\n'
}

#Data for Multimeter
MM_Data = {
    'ip_addr' : ('10.245.26.24', 5555),
    'curr_dc' : ':MEAS:CURR:DC?\n'
}


# Set up logging file for error reporting
# Referenced from: https://stackoverflow.com/questions/3383865/how-to-log-error-to-file-and-not-fail-on-exception
logging.basicConfig(filename=config_value('logging_filepath'), level=logging.ERROR,
                    format='%(asctime)s - %(levelname)s - %(name)s - %(message)s')

logger = logging.getLogger(__name__)


"""
    These values define the number of iterations to measure, for the total repetitions and the frequency (Hz) per repetition.
    For best results, these values should be consistent for all sets of measurements between boards.
"""
repetitions = config_value('repetitions')
iterations = config_value('iterations')
delay = config_value('delay')



print("Before beginning the measurements, enter data to label the current trial.")

new_ip = config_value('multimeter_ip')

o_scope = config_value('use_oscilloscope')
new_ip2 = config_value('oscilloscope_ip')
    

board_name = config_value('board_name')
test_label = config_value('test_label')
filepath = config_value('data_filepath')
voltage = config_value('voltage')


#Multimeter Connection    
if new_ip.strip() != "DEFAULT":
    MM_Data['ip_addr'] = (new_ip, 5555)

print("Attempting to connect to IP address: ", MM_Data['ip_addr'])

try:
    # SCOPE_SOCKET = socket.create_connection(MSO2302A_DATA['ip_addr'])
    MM_SOCKET = socket.create_connection(MM_Data['ip_addr'])
except Exception as err:
    logger.error(err)
    print("Connection failed. See log for more details.")
    exit() 
    
MM_SOCKET.settimeout(2.0)
RECV_MAX_BYTES = 1024

#Oscilloscope Connection
if (o_scope) :
    if new_ip2 != "DEFAULT":
        OS_Data['ip_addr'] = (new_ip2, 5555)

    print("Attempting to connect to IP address: ", OS_Data['ip_addr'])

    try:
        # SCOPE_SOCKET = socket.create_connection(MSO2302A_DATA['ip_addr'])
        OS_SOCKET = socket.create_connection(OS_Data['ip_addr'])
    except Exception as err:
        logger.error(err)
        print("Connection failed. See log for more details.")
        exit()
    
    OS_SOCKET.settimeout(2.0)

    
# voltage = float(voltage.strip())

input("\nPress enter to begin idle current draw...\n")

idle_current = 0;
idle_iterations = config_value('idle_iterations')

for j in range(idle_iterations):
    # Query the Multimeter
    MM_SOCKET.send(bytes(MM_Data['curr_dc'], 'utf_8'))
    # Read and store the value 
    data_in = (bytes.decode(MM_SOCKET.recv(1024), 'utf_8'))
    idle_current += float(data_in.strip()) * (1/idle_iterations)

df = pandas.DataFrame()

print("Idle current draw: ", idle_current)

print("\nBeginning measurements...\n")

total_inference = []
avg_inf_power = []
energy = []

for i in range(repetitions):
    
    a = input("Press enter to start next repetition...")
    
    raw_data = []
    offset_data = []
    o_scope_data = []
    time_stamps = []
    
    try: 
        
        for j in range(iterations):
            
            # Query the Multimeter
            MM_SOCKET.send(bytes(MM_Data['curr_dc'], 'utf_8'))
            #Query the o_scope
            if (o_scope == "Y") :
                OS_SOCKET.send(bytes(OS_Data['chan1_vpp'], 'utf_8'))
            # Read and store the value 
            data_in = (bytes.decode(MM_SOCKET.recv(RECV_MAX_BYTES), 'utf_8'))
            raw_data.append(float(data_in.strip()))
            offset_data.append(float(data_in.strip())-idle_current)
            time_stamps.append(datetime.now())
            #Recieve from the o_scope
            if (o_scope == "Y") :
                data_in = (bytes.decode(OS_SOCKET.recv(RECV_MAX_BYTES), 'utf_8'))
                o_scope_data.append(float(data_in.strip()))
            time.sleep(delay)
    
    except Exception as err:
        logger.error(err)
    
    print("\nCurrent repetition complete. Perform any necessary resets now.\n")
    
    raw_power = [voltage * float(i) for i in raw_data]
    offset_power = [voltage * float(i) for i in offset_data]

    if (o_scope) :
        #count total inference time and find average power while inferencing
        total = 0
        power = 0
        idx = 0
        for point in o_scope_data :
            if (point >= 1) : #if inferencing at this time
                total += 1
                power += offset_power[idx]
        idx += 1

        total_inference.append(total * 0.1) #add 100ms * total high points to the total time
        if (total == 0) :
            avg_inf_power.append(0)
        else :
            avg_inf_power.append(power / total) #find the average offset power draw WHILE INFERENCING
        energy.append(total_inference[-1] * avg_inf_power[-1]) #energy = power * time (in Joules)

    temp = pandas.DataFrame(data = [[pandas.to_datetime(i) for i in time_stamps], raw_data, raw_power, offset_data, offset_power, o_scope_data])
    temp = temp.T
    temp.columns = [f'timestamp_{i+1}', f'raw_current_{i+1}', f'raw_power_{i+1}', f'offset_current_{i+1}', f'offset_power_{i+1}', f'o_scope_data_{i+1}']
    temp.index = list(range(iterations))
    
    print("\n\n\n")
    print(temp)
    
    df = pandas.concat([df, temp], axis=1)
    
    print("\n\n\n")
    print(df)
    
MM_SOCKET.close()

try:
    # Voltage will be constant, current will fluctuate. Final measurements will represent Power over Time. 

    # if filepath == "":
    #     filepath = f'./{board_name}/{test_label}'
    # else:
    #     filepath = filepath;
    
    if not os.path.exists(filepath):
        os.makedirs(filepath, exist_ok=True)
    
    df.to_csv(f'{filepath}/data.csv')
    
    powers = [f'raw_power_{a+1}' for a in range(repetitions)]
    
    df.plot(y = powers, kind='line', legend=True, title = f'Raw Power over Time for {board_name} - {test_label}')
        

    """ 
        Maybe take average timestamp change estimate for x axis?
    """

    # plt.plot(df)
    # plt.xlabel('Time')
    # plt.ylabel('Power')
    # plt.title(f'Power and Current over Time for {board_name} - {test_label}')
    plt.savefig(f'{filepath}/raw_graph.png')
    
    offsets = [f'offset_power_{a+1}' for a in range(repetitions)]
    
    df.plot(y = offsets, kind='line', legend=True, title = f'Offset Power over Time for {board_name} - {test_label}')
    plt.savefig(f'{filepath}/offset_graph.png')

    if (o_scope) :
        toggles = [f'o_scope_data_{a+1}' for a in range(repetitions)]

        df.plot(y = toggles, kind='line', legend=True, title = f'Pin Toggle over Time for {board_name} - {test_label}')
        plt.savefig(f'{filepath}/pin_toggle_graph.png')

        inference_time = statistics.mean(total_inference)
        average_power = statistics.mean(avg_inf_power)
        avg_energy = statistics.mean(energy)
        score = 1 / avg_energy

        data = [board_name, test_label, inference_time, average_power, avg_energy, score]

        with open(f'{filepath}/out.csv', 'w', newline='') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(data)
    
except Exception as err:
    logger.error(err)