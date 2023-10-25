# vyasan valavil 10/25/2023
# code for generating analog output to USB-6008
# Analog Output will stay on unless stopAO is used at the end.

import nidaqmx
from nidaqmx.constants import LineGrouping

def giveAO(line, voltage):
    with nidaqmx.Task() as task:
        dev1a0 = "Dev1/" + line
        task.ao_channels.add_ao_voltage_chan(dev1a0, 'AOchannel', 0, 5)
        task.write(voltage)

def stopAO(line):
    with nidaqmx.Task() as task:
        dev1a0 = "Dev1/" + line
        task.ao_channels.add_ao_voltage_chan(dev1a0, 'AOchannel', 0, 5)
        task.write(0)

giveAO("ao0", 1.6)