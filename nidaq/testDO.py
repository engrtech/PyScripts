# vyasan valavil 10/25/2023
# code for sending digital out to USB-6008
# max is 1 mA. if additional amerage is needed, use external pullups (8.5 mA max i.e. 370 Ohms)
# USI Q56 tester is used in this example

import nidaqmx
from nidaqmx.constants import LineGrouping

def giveDO(case):
    with nidaqmx.Task() as task:
        task.do_channels.add_do_chan("Dev1/port0/line0:7", line_grouping=LineGrouping.CHAN_FOR_ALL_LINES)
        match case:
            case 0b00000000:
                print("LED all off")
                status = "All off"
            case 0b00000001:
                print("LED Red for Error")
                status = "Error"
            case 0b00000010:
                print("LED Green for Success")
                status = "Success"
            case 0b00000011:
                print("LED all ON")
                status = "All ON"
            case 0b00000100:
                print("LED alternate ON")
                status = "Alternate ON"
        task.write(case)
        return status

giveDO(0b00000100)