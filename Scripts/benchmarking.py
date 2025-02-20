from pathlib import Path
import socket 
import time
import math
import pandas
import logging
from datetime import datetime
import matplotlib.pyplot as plt
import os

"""

    This script is used to configure the MSO2302A oscilloscope in order to obtain readings of the power consumption of differnet boards.
    
    Power will be obtained by measuring current fluctuations across a constant voltage source.
    
    Procedure:
    [INSERT DETAILS ABOUT HOW WE ARE SETTING UP, GATHERING DATA, AND STORING IT]
    Export format: 
        raw data - CSV
        plots - pngs of graphs, power over time
        

"""

# Dictionary of information for the oscilloscope
MSO2302A_DATA = {
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
logging.basicConfig(filename='ErrorLogs\\benchmarking.log', level=logging.ERROR,
                    format='%(asctime)s - %(levelname)s - %(name)s - %(message)s')

logger = logging.getLogger(__name__)


"""
    These values define the number of iterations to measure, for the total repetitions and the frequency (Hz) per repetition.
    For best results, these values should be consistent for all sets of measurements between boards.
"""
repetitions = 3
iterations = 50
delay = 0.1



print("Before beginning the measurements, enter data to label the current trial.")

new_ip = input(f"Enter the IP address of the multimeter ([d]efault - {MM_Data['ip_addr'][0]}): ")
board_name = input("Enter the name of the board: ")
test_label = input("Enter the label for the current trial: ")
filepath = input("Enter the filepath to save the current trial data (default relative path - /[board_name]/[test_label]): ")
voltage = input("Enter the voltage for the current trial: ")

while not voltage.strip().isdecimal() and not voltage.strip().isnumeric():
    voltage = input("\tPlease enter a numerical value: ")
    
if new_ip != "d" and new_ip != "":
    print(new_ip)
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
    
voltage = float(voltage.strip())

input("\nPress enter to begin idle current draw...\n")

idle_current = 0;
idle_iterations = 20

for j in range(idle_iterations):
    # Query the Multimeter
    MM_SOCKET.send(bytes(MM_Data['curr_dc'], 'utf_8'))
    # Read and store the value 
    data_in = (bytes.decode(MM_SOCKET.recv(RECV_MAX_BYTES), 'utf_8'))
    idle_current += float(data_in.strip()) * (1/idle_iterations)

df = pandas.DataFrame()

print("Idle current draw: ", idle_current)

print("\nBeginning measurements...\n")

for i in range(repetitions):
    
    a = input("Press enter to start next repetition...")
    
    raw_data = []
    offset_data = []
    time_stamps = []
    
    try: 
        
        for j in range(iterations):
            
            
            # Query the Multimeter
            MM_SOCKET.send(bytes(MM_Data['curr_dc'], 'utf_8'))
            # Read and store the value 
            data_in = (bytes.decode(MM_SOCKET.recv(RECV_MAX_BYTES), 'utf_8'))
            raw_data.append(float(data_in.strip()))
            offset_data.append(float(data_in.strip())-idle_current)
            time_stamps.append(datetime.now())
            time.sleep(delay)
    
    except Exception as err:
        logger.error(err)
    
    print("\nCurrent repetition complete. Perform any necessary resets now.\n")
    
    raw_power = [voltage * float(i) for i in raw_data]
    offset_power = [voltage * float(i) for i in offset_data]
    
    temp = pandas.DataFrame(data = [[pandas.to_datetime(i) for i in time_stamps], raw_data, raw_power, offset_data, offset_power])
    temp = temp.T
    temp.columns = [f'timestamp_{i+1}', f'raw_current_{i+1}', f'raw_power_{i+1}', f'offset_current_{i+1}', f'offset_power_{i+1}']
    temp.index = list(range(iterations))
    
    print("\n\n\n")
    print(temp)
    
    df = pandas.concat([df, temp], axis=1)
    
    print("\n\n\n")
    print(df)
    
MM_SOCKET.close()

try:
    # Voltage will be constant, current will fluctuate. Final measurements will represent Power over Time. 

    if filepath == "":
        filepath = f'./{board_name}/{test_label}'
    else:
        filepath = filepath;
    
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
    
except Exception as err:
    logger.error(err)