from pathlib import Path
import socket
import time
import math
import matplotlib.pyplot as plt

#Data for Multimeter
MM_Data = {
    'ip_addr' : ('10.245.26.218', 5555),
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
for x in range(300):
    Times.append(0.1 + (x * 0.1))

Measurements = []
time.sleep(0.1)
for x in range(300):
    #Query the MM
    MM_SOCKET.send(bytes(MM_Data['curr_dc'], "utf-8"))
    #Store that value
    current = float((MM_SOCKET.recv(RECV_MAX_BYTES)).decode("utf-8"))
    Measurements.append(current)
    time.sleep(0.1)

#Plot data and labels
plt.plot(Times, Measurements)
plt.xlabel("Time(s)")
plt.ylabel("Current(A)")
plt.title("Measured Current Over 30 Seconds")
plt.show()