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
    Currently using just to get the input from the excel sheet
"""


file = open("Scripts/analysis_filepaths.txt", 'r')
columns = ["Board Name", "Trial Name", "Average Inference Time", "Average Offset Power", "Energy Consumed", "Energy Score"]

df = pandas.DataFrame(columns=columns)

for line in file:
    if line == "\n":
        break
    
    line = line.strip()
    
    temp_file = open(line, 'r')
    
    data = []
    
    for val in temp_file.readlines():
        
        temp_data = val.strip().split(",")
        temp_data = [temp_data[0], temp_data[1], float(temp_data[2]), float(temp_data[3]), float(temp_data[4]), float(temp_data[5])]
        data.append(temp_data)
    
    temp_file.close()
    
    for i in range(len(data)):
        df.loc[len(df)] = data[i]

file.close()

print(df)

# Average any results across same board, different trials

new_df = pandas.DataFrame(columns=columns)

print('\n\n\n')
for board in df['Board Name'].unique():
    temp_df = df[df['Board Name'] == board].copy()
    temp_df.reset_index(inplace=True)
    
    average_inference_time = temp_df['Average Inference Time (s)'].mean(axis=0)
    average_offset_power = temp_df['Average Power Difference During Inferencing (W)'].mean(axis=0)
    energy_consumed = temp_df['Energy Consumed Per Inference (J)'].mean(axis=0)
    energy_score = temp_df['Energy Score'].mean(axis=0)
    
    new_df.loc[len(new_df)] = [board, "Average", average_inference_time, average_offset_power, energy_consumed, energy_score]

print(new_df)

# Generate bar graphs showing each category of results across all board averages

for column in new_df.columns:
    if column == "Board Name" or column == "Trial Name":
        continue
    
    plt.bar(new_df['Board Name'], new_df[column])
    plt.title(column)
    plt.xlabel("Board")
    plt.ylabel("Measurement")
    plt.savefig('Results/' + column + '.png')
    plt.close()