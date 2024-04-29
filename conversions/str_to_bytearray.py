#import canlib
#for dev in canlib.connected_devices():
#    print(dev.probe_info())

#there is the string
udsmsg = '3e00'

udsmsg = [udsmsg[i:i+2].encode('utf-8') for i in range(0, len(udsmsg), 2)]
print(udsmsg)