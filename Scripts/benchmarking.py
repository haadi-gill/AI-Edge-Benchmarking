from pathlib import Path
import socket 
import time
import math
import pandas
import logging
import matplotlib.pyplot as plt

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

# Set up logging file for error reporting
# Referenced from: https://stackoverflow.com/questions/3383865/how-to-log-error-to-file-and-not-fail-on-exception
logging.basicConfig(filename='ErrorLogs\\benchmarking.log', level=logging.ERROR,
                    format='%(asctime)s - %(levelname)s - %(name)s - %(message)s')

logger = logging.getLogger(__name__)


try:
    SCOPE_SOCKET = socket.create_connection(MSO2302A_DATA['ip_addr'])
except Exception as err:
    logger.error(err)
    exit()
    
    
SCOPE_SOCKET.settimeout(2.0)
RECV_MAX_BYTES = 1024

"""
    These values define the number of iterations to measure, for the total repitions and the frequency (Hz) per repition.
    For best results, these values should be consistent for all sets of measurements between boards.
"""
repitions = 20
iterations = 500
delay = 0.5

raw_data = []
time_stamps = []
decibles = []


print("Before beginning the measurements, enter data to label the current trial.")

board_name = input("Enter the name of the board: ")
test_label = input("Enter the label for the current trial: ")
filepath = input("Enter the filepath to save the current trial data (default relative path - /[board_name]/[test_label]): ")
voltage = input("Enter the voltage for the current trial: ")

while not voltage.strip().isnumeric():
    voltage = input("Please enter a numerical value: ")
    
voltage = float(voltage.strip())

print("\nBeginning measurements...\n")

for i in range(repitions):
    
    a = input("Press any enter to start next repition...")
    
    try: 
        
        for j in range(iterations):
            SCOPE_SOCKET.send(bytes(MSO2302A_DATA['chan1_vpp'], 'utf_8'))
            data_in = (bytes.decode(SCOPE_SOCKET.recv(RECV_MAX_BYTES), 'utf_8'))
            raw_data.append(data_in.strip())
            time_stamps.append(time.time())
            time.sleep(delay)
    
    except Exception as err:
        logger.error(err)
    
    print("\nCurrent repition complete. Perform any necessary resets now.\n")
    

SCOPE_SOCKET.close()

# Voltage will be constant, current will fluctuate. Final measurements will represent Power over Time. 
power = [voltage * float(i) for i in raw_data]
datetimes = [pandas.to_datetime(i) for i in time_stamps]

df = pandas.DataFrame(data = [datetimes, raw_data, power]).T
df.columns = ['timestamp', 'raw_data', 'power']
df.index = df['timestamp']

if filepath == "":
    filepath = Path(f'./{board_name}/{test_label}')
else:
    filepath = Path(filepath)

filepath.parent.mkdir(parents = True, exist_ok = True)
df.to_csv(f'{filepath}/data.csv')

plt.plot(datetimes, power)
plt.xlabel('Time')
plt.ylabel('Power')
plt.title(f'Power over Time for {board_name} - {test_label}')
plt.savefig(f'{filepath}/graph.png')