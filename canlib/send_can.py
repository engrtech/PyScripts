#send_msg
# The CANlib library is initialized when the canlib module is imported. To be
# able to send a message, Frame also needs to be installed.
from canlib import canlib, Frame
import binascii


ch_a = canlib.openChannel(channel=0)

# After opening the channel, we need to set the bus parameters. Some
# interfaces keep their params from previous programs. This can cause problems
# if the params are different between the interfaces/channels. For now we will
# use setBusParams() to set the canBitrate to 250K.
#AT DANA WE USE 500K
ch_a.setBusParams(canlib.canBITRATE_500K)

# The next step is to Activate the CAN chip for each channel
ch_a.busOn()

frame = Frame(id_=0x7E0, data=[0x02,0x3e,0x00,0x00,0x00,0x00,0x00,0x00], flags=canlib.MessageFlag.STD)

print("Written to A:")
print((binascii.hexlify(frame.data)))
ch_a.write(frame)

# To make sure the message was sent we will attempt to read the message. Using
# timeout, only 500 ms will be spent waiting to receive the CANFrame. If it takes
# longer the program will encounter a timeout error. read the CANFrame by calling
# .read() on the channel that receives the message, ch_b in this example. To
# then read the message we will use print() and send msg as the input.

msg = ch_a.read(timeout=5)
print("Read from A:")
print((binascii.hexlify(msg.data)))

# After the message has been sent, received and read it is time to inactivate
# the CAN chip. To do this call .busOff() on both channels that went .busOn()
ch_a.busOff()

# Lastly, close all channels with close() to finish up.
ch_a.close()

# Depending on the situation it is not always necessary or preferable to go of
# the bus with the channels and, instead only use close(). But this will be
# talked more about later.