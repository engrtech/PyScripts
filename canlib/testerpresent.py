from canlib import canlib, Frame
import time
import binascii
import candef
import threading
import pandas as pd

kvaser_channel = 0

did = 0x7E0
tid = 0x7E8

#Also keep the receiving channel open...
def rx_uds():
#runs on separated thread dedicated to listening.
    print("Receiving channel ON.\n")
    global rx, df
    while not end_rx.is_set():
        try:
            recd = ch_a.read(timeout=5000)
            if recd.id == tid: #We only care about specific IDs
                recmsg = ((binascii.hexlify(recd.data)).decode())
                df.loc[len(df.index)] = f'Rx : 7E0 {recmsg}'
                proc_rx(recmsg)
        except:
            print("no longer reading messages")
    print("receive thread is stopped")

def proc_rx(recmsg):
    global st, bytes_remaining, dl, eor, recstr, conf
    if recmsg[0] == '0':
        recstr = recmsg
        eor = True
    if recmsg[0] == '1':
        recstr = '' ## initializing
        eor = False ## flow control is on.
        dl = int(recmsg[1:4], 16) ## initialized here
        bytes_remaining = dl-6 ## first UDS message has only 6 bytes
        framestr = recmsg[4:] ## this is what we select sections of the transmission
        recstr = recstr + framestr ## add it to the big string
        ch_a.write(Frame(id_=did, data=[48, 0, 7, 0, 0, 0, 0, 0], flags=canlib.MessageFlag.STD)) #YES to FC
        df.loc[len(df.index)] = f'Tx : 7E8 3000070000000000'
    if recmsg[0] == '3':
        conf = True
        st = int(recmsg[4:6], 16)
    if recmsg[0] == '2':
        if bytes_remaining > 7:
            framestr = recmsg[2:]
            bytes_remaining = bytes_remaining - 7
        else:
            framestr = recmsg[2:(2+bytes_remaining*2)] ## last byte will be incomplete
            eor = True
        recstr = recstr + framestr


def tx(msg, resp="std"):
    global df, did, fc, eor
    fc = False #clear the frame... it needs to be ready to either accept full data or confirmation....
    eor = False  # Actively listening for Rx...
    global recstr, serreq, prc, nrc
    recstr = '' #New transmission means forget about the old one...
    st = 0
    prc = int(msg[0:2], 16) + 64 #adding 0x40 to the service request
    nrc = int('7f', 16)
    print(f'Positive Response Code Expected: {prc}')
    if len(msg)>14: fc = True
    framedata, framestring = candef.str2udstupple(msg)
    if fc==False:
        ch_a.write(Frame(id_=did, data=framedata, flags=canlib.MessageFlag.STD))
        df.loc[len(df.index)] = f'Tx : 7E8 {framestring}'
    else:
        time.sleep(.1)
        ch_a.write(Frame(id_=did, data=framedata[0], flags=canlib.MessageFlag.STD))
        df.loc[len(df.index)] = f'Tx : 7E8 {framestring[0]}'
        #now here compare the rx message to see if it has a flow control separation time...
        while conf==False:
            pass
        for i in range(len(framedata)-1):
            ch_a.write(Frame(id_=did, data=framedata[i+1], flags=canlib.MessageFlag.STD))
            df.loc[len(df.index)] = f'Tx : 7E8 {framestring[i+1]}'

def response():
    global df, eor, recstr
    while eor==False:
         if eor:
            len_of_df = df.shape[0]
            df.iat[len_of_df - 1, 0] = df.iat[len_of_df - 1, 0] + ' ' + recstr
            return recstr

def unlock_using_token(dll):
    global msgstr, sn, df, recstr
    sn = 0
    tx('2761')
    seed = response()[4:]
    print(f'Seed from ECU: {seed}')
    challenge = []
    for s in range(int(len(seed)/2)):
        challenge.append(str(int(seed[(s*2):((s+1)*2)], 16)))
    challenge.insert(0, str(dll))  # which dev key does it use?
    challenge.insert(0, str(sn))  # string serial number will be passed as argument#1
    # compute_key_from_seed is defined in can_def
    key = candef.compute_key_from_seed(challenge)
    print(key)
    tx(f'2762{key}')

def check_comm():
    comm = False
    tries = 0
    while comm & tries==3:
        tx('3e00')
        if response() == '7e000000000000':
            print("Response Received")
        time.sleep()

#################################################################################################
##################################### SCRIPT BEGINS HERE ########################################
#################################################################################################

column_names = ['Messages']
df = pd.DataFrame(columns = column_names)

#initialize variables
eor = False #end of reception
conf = False #flow control confirmed

for i in range(3):
    try:
        # open channel (only 1 channel on the kvaser)
        ch_a = canlib.openChannel(channel=kvaser_channel)
        # set bus parameters
        ch_a.setBusParams(canlib.canBITRATE_500K)
        # activate CAN chip
        ch_a.busOn()
        print(f'Channel {kvaser_channel} is ON.')
        break
    except:
        print(f'Channel {1} did NOT turn ON after try {i + 1}.')
        channel_flag = False
        time.sleep(3)

end_rx = threading.Event()  #recd
can_rx = threading.Thread(target=rx_uds) #thread for receiving messages only
can_rx.start()
rx_frame = []

#Now make sure that the unit is communicating...
check_comm()
#################################################################################################
################################## TRANSMISSIONS BEGINS HERE ####################################
#################################################################################################

#First check if unit is communicating...
tx('1003')
print("Response", response())
time.sleep(1)
tx('3e00')
print("Response", response())
time.sleep(1)
tx('1002')
print("Response", response())
time.sleep(1)
unlock_using_token(1)

time.sleep(3) #you want a pause after the last confirmation...

end_rx.set()
can_rx.join()

#################################################################################################
############################################ PROCESS DATA #######################################
#################################################################################################

print(df)