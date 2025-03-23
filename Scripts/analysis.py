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


df = pandas.read_excel("Scripts/benchmark_template.xlsx")
df.drop(columns=["Description", "Flag", "Unnamed: 4", "Flag Values"], inplace=True)
print(df)
print(df[df['Name'] == 'logging_filepath']["Value"][0])


def config_value(label):
    
    return df[df['Name'] == label].reset_index()["Value"][0]
    
logging_filepath = config_value('logging_filepath')        
repetitions = config_value('repetitions')
iterations = config_value('iterations')
delay = config_value('delay')
use_oscilloscope = config_value('use_oscilloscope')

print(logging_filepath, type(logging_filepath))
print(repetitions, type(repetitions))
print(iterations, type(iterations))
print(delay, type(delay))
print(use_oscilloscope, type(use_oscilloscope))