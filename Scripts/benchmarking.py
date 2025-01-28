from pathlib import Path
import socket 
import time
import math
import pandas
import logging
import matplotlib.pyplot as plt

"""

    This script is used to configure the MSO2302A oscilloscope in order to obtain readings of the power consumption of differnet boards.
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
frequency = 500

raw_data = []
decibles = []



for i in range(repitions):
    
    SCOPE_SOCKET.send(bytes(MSO2302A_DATA['chan1_vpp'], 'utf_8'))
    data_in = (bytes.decode(SCOPE_SOCKET.recv(RECV_MAX_BYTES), 'utf_8'))
    raw_data.append(data_in.strip())
    # print(f"receiving frequency: {float(data_in):.2f}\n")
    # decibles.append(20.0*math.log(float(data_in)/5.0, 10))
    # print(f"decibel: {float(decibles[-1]):.2f}\n")
    time.sleep(1.0/frequency)

SCOPE_SOCKET.close()

# Voltage will be constant, current will fluctuate. Final measurements will represent Power over Time. 



# df = pandas.DataFrame(data = [frequencies, raw_data, decibles]).T
# df.columns = ['frequencies', 'raw_data', 'decibles']
# df.index = df['frequencies']
# df.drop(columns='frequencies', inplace=True)
# df.to_csv('Equipment Demonstration/data.csv')

# plt.plot(frequencies, decibles)
# plt.axvline(1591, color = 'purple', label = 'Experimental Cutoff')
# plt.axvline(1082, color = 'red', label = 'Calculated Cutoff')
# plt.xlabel('Frequencies (Hz)')
# plt.ylabel('Decibels (dB)')
# plt.xscale('log')
# plt.title("Bode Plot for Cutoff Frequency")
# plt.legend()
# plt.savefig('Equipment Demonstration/graph.png')
