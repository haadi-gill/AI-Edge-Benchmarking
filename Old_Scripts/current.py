from pathlib import Path
import socket
import time
import math
import matplotlib.pyplot as plt

#Data for Multimeter
MM_Data = {
    'ip_addr' : ('10.245.26.169', 5555),
    'curr_dc' : ':MEAS:CURR:DC?\n'
}

#Try to create socket connections
try: 
    MM_SOCKET = socket.create_connection(MM_Data['ip_addr'])
except:
    exit("Error")
MM_SOCKET.settimeout(2.0)

RECV_MAX_BYTES = 1024

Times = []
Measurements = []

time.sleep(0.1)
totalTime = 0
for x in range(60):
    # start timer
    start = time.perf_counter()
    #Query the MM
    MM_SOCKET.send(bytes(MM_Data['curr_dc'], "utf-8"))
    #Store that value
    current = float((MM_SOCKET.recv(RECV_MAX_BYTES)).decode("utf-8"))
    # stop timer
    end = time.perf_counter()
    # keeo track of total time
    totalTime += end - start
    # y axis
    Measurements.append(current * 3.3)
    # x axis
    Times.append(totalTime)

#Plot data and labels
plt.plot(Times, Measurements)
plt.xlabel("Time(s)")
plt.ylabel("Power(W)")
plt.title("Measured Power Over 25 Seconds")
plt.show()