# vyasan valavil 10/25/2023
# code for reading analog input from USB-6008

import nidaqmx
from nidaqmx.constants import LineGrouping
import time

def getAIsamp(line, samplecount):
    with nidaqmx.Task() as task:
        ailine = "Dev1/" + line
        task.ai_channels.add_ai_voltage_chan(ailine)
        print(f'1 Channel {samplecount} Samples Read: ')
        data = task.read(number_of_samples_per_channel=samplecount)
        return most_frequent(data)

def most_frequent(List):
    return max(set(List), key = List.count)

while (1):
    print(getAIsamp("ai6", 8))
    time.sleep(1)