# vyasan valavil 10/25/2023
# code for reading digital input from USB-6008

import nidaqmx
from nidaqmx.constants import LineGrouping

def getDIsamp(line, samplecount):
    with nidaqmx.Task() as task:
        diline = "Dev1/port1/" + line
        task.di_channels.add_di_chan(diline, line_grouping=LineGrouping.CHAN_PER_LINE)
        data = task.read(number_of_samples_per_channel=samplecount)
        return most_frequent(data)

def most_frequent(List):
    return max(set(List), key = List.count)

print(getDIsamp("line0", 4))