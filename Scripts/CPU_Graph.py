import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_csv("CPU&Temp_log_Raspi3_AudDetect.csv")
df['Timestamp'] = pd.to_datetime(df['Timestamp'])

plt.figure()
plt.plot(df['Timestamp'], df['CPU Usage (%)'], label='CPU Usage')
plt.plot(df['Timestamp'], df['CPU Temp (°C)'], label='CPU Temp')
plt.xlabel("Time")
plt.ylabel("Value")
plt.legend()
plt.show()
