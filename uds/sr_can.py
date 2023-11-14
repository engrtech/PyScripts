#Vyasan Valavil
#2023-11-14

#Script takes user-input and transmits it through UDS while Tester Present ping is sent every second.
#There are 2 additional threads in this script

#send_msg
# The CANlib library is initialized when the canlib module is imported. To be
# able to send a message, Frame also needs to be installed.
from canlib import canlib, Frame
import binascii
import time
import threading

#function definitions
def processuds(input):
    input = str(input).replace(" ", "").lower()
    b_len = int(len(input)/2)
    if len(input) < 14:
        for x in range(14-len(input)):
            input = input + '0'
    inputhex = [b_len]
    for x in range(7):
        inputhex.append(int(input[2 * x:2 * x + 2], 16))
    if input[:1] != '0x':
        input = '0x' + input
    #print(input)
    #print(inputhex)
    return inputhex

def printiddata(frame):
    id = frame.id
    id = (hex(id)[2:]).upper()
    data = (binascii.hexlify(frame.data)).decode()
    temp = description(str(data)) #get rid of this line and its associated function after debugging.
    msg = id + " " + data + " " + temp
    return msg

def tx(hex):
    send = Frame(id_=danasend_id, data=hex[0], flags=canlib.MessageFlag.STD)
    ch_a.write(send)
    sentmsg = printiddata(send)
    print(f'Tx : {sentmsg}')

def rx():
    while (1):
        recd = ch_a.read(timeout=60000)
        recdmsg = printiddata(recd)
        if recdmsg != '7E8 027e000000000000 ':
            print(f'Rx : {recdmsg}')

def hiddentx(hex):
    send = Frame(id_=danasend_id, data=hex[0], flags=canlib.MessageFlag.STD)
    ch_a.write(send)
    #sentmsg = printiddata(send)
    #print(f'Tx : {sentmsg}')

def testerpresent(tpsend):
    while True:
        hiddentx(tpsend)
        time.sleep(1)

def processdesc(tupple):
    hexstring = []
    description = []
    for x in tupple:
        tempstr = ""
        for y in x[0]:
            twodigit = hex(y)[2:]
            if len(twodigit)<2:
                twodigit = '0' + twodigit
            tempstr = tempstr + twodigit
        hexstring.append(tempstr)
        description.append(x[1])
    return hexstring, description

def description(data):
    desc = ""
    for i in range(len(hexstrings)):
        if data == hexstrings[i]:
            desc = descriptions[i]
    return desc

#message id and data
danasend_id = 0x7E0
tpsend              = ([0x02, 0x3e, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00], "")
tprecd              = ([0x02, 0x7e, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00], "")
ddssend             = ([0x02, 0x10, 0x01, 0x00, 0x00, 0x00, 0x00, 0x00], "REQUESTED DDS")
ddsrecd_p           = ([0x06, 0x50, 0x01, 0x00, 0x32, 0x13, 0x88, 0x00], "POSITIVE DDS")
pgssend             = ([0x02, 0x10, 0x02, 0x00, 0x00, 0x00, 0x00, 0x00], "REQUESTED PGS")
pgsproc             = ([0x03, 0x7f, 0x10, 0x78, 0x00, 0x00, 0x00, 0x00], "PROCESSING REQUEST FOR PGS")
pgsrecd_p           = ([0x06, 0x50, 0x02, 0x00, 0x32, 0x13, 0x88, 0x00], "POSITIVE PGS")
edssend             = ([0x02, 0x10, 0x03, 0x00, 0x00, 0x00, 0x00, 0x00], "REQUESTED EDS")
edsrecd_p           = ([0x06, 0x50, 0x03, 0x00, 0x32, 0x13, 0x88, 0x00], "POSITIVE EDS")
ksu_uds_rc          = ([0x04, 0x31, 0x01, 0xf1, 0x3f, 0x00, 0x00, 0x00], "KSU UDS RC")
ksu_uds_rc_p        = ([0x04, 0x71, 0x01, 0xf1, 0x3f, 0x00, 0x00, 0x00], "KSU UDS RC CONFIRMED")
dpr_uds_rc          = ([0x04, 0x31, 0x01, 0xf1, 0x3f, 0x00, 0x00, 0x00], "DEBUG PW REQ RC")

#description tuples
desctupples = [ddssend, ddsrecd_p, edssend, edsrecd_p, pgssend, pgsproc, pgsrecd_p, ksu_uds_rc, ksu_uds_rc_p, dpr_uds_rc]
#let's process all these tupples into strings:
hexstrings, descriptions = processdesc(desctupples)


#open channel (only 1 channel on the kvaser)
ch_a = canlib.openChannel(channel=0)

#set bus parameters
ch_a.setBusParams(canlib.canBITRATE_500K)

#activate CAN chip
ch_a.busOn()

#seconds = 100

#initialize tester present send
tp1 = threading.Thread(target=testerpresent, args=(tpsend,))
tp1.start()

#initialize a receive that stays on all the time
tp2 = threading.Thread(target=rx)
tp2.start()

while (1):
    # create frame and transmit
    time.sleep(.5)
    useruds = input("Enter UDS code in hex : ")
    usermsg = (processuds(useruds), "USER INPUT")
    tx(usermsg)

#close bus
ch_a.busOff()

# close channel
ch_a.close()