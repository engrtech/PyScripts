from canlib import canlib, Frame
import can_def
import threading
import time
import pandas as pd
import glob
import os

did = 0x18da5ff9
tid = 0x18daf95f

# The path to the Python interpreter you want to use token_dll may require 32-bit Python
py32bit = 'C:/SVN/LaForge/Tools/Hydra_UDS/Scripts/venv/Scripts/python.exe'
# The path to your 32
script_path = 'ComputeKeyFromSeed.py'

def tx_uds(framedata, mf):
#called by quick_tx()
    if mf == 0:
        tx_sf_uds(framedata)
    else:
        tx_mf_uds(framedata)

def tx_sf_uds(framedata):
    global did
    frame = Frame(id_=did, data=framedata, flags=canlib.MessageFlag.FDF | canlib.MessageFlag.BRS | canlib.MessageFlag.EXT)
    ch_a.write(frame)
    sent_msg = can_def.disp_uds(frame)
    global df
    dflog = 'Tx : ' + sent_msg
    df.loc[len(df.index)] = dflog

def tx_mf_uds(framedata): #framedata here comes as a list...
    global did
    # send first frame
    print("sending out large frame")
    frame = Frame(id_=did, data=framedata[0], flags=canlib.MessageFlag.FDF | canlib.MessageFlag.BRS | canlib.MessageFlag.EXT)
    ch_a.write(frame)
    sent_msg = can_def.disp_uds(frame)
    global df
    dflog = 'Tx : ' + sent_msg
    df.loc[len(df.index)] = dflog
    time.sleep(.002)
    # now check the response
    conf, st = can_def.chk_resp(last_recd)
    #print(last_recd.data)
    #print("send signal confirmed: ", conf, st)
    if conf: #Was the first byte 30?
        for x in range(len(framedata) - 1):
            time.sleep(st)  # separation time
            frame = Frame(id_=did, data=framedata[x + 1], flags=canlib.MessageFlag.FDF | canlib.MessageFlag.BRS | canlib.MessageFlag.EXT)
            sent_msg = can_def.disp_uds(frame)
            dflog = 'Tx : ' + sent_msg
            df.loc[len(df.index)] = dflog
            time.sleep(.002)
            ch_a.write(frame)
    time.sleep(.002)

def tx_rec_cf(st):
#flow control with separation time...
    send = bytearray(8)
    send[0] = 48
    send[1] = st
    frame = Frame(id_=did, data=send, flags=canlib.MessageFlag.FDF | canlib.MessageFlag.BRS | canlib.MessageFlag.EXT)
    sent_msg = can_def.disp_uds(frame)
    global df
    dflog = 'Tx : ' + sent_msg
    df.loc[len(df.index)] = dflog
    ch_a.write(frame)

def rx_uds():
#runs on separated thread dedicated to listening.
    while not end_rx.is_set():
        try:
            recd = ch_a.read(timeout=60000)
            global last_recd
            if recd.id == 0x18daf95f:
                proc_uds_recd(recd) #if flow control needs to be implemented
                last_recd = recd
                recd_msg = can_def.disp_uds(recd)
                global df
                dflog = 'Rx : ' + recd_msg
                df.loc[len(df.index)] = dflog
        except:
            print("no longer reading messages")
    print("rx_uds thread is stopped")

def proc_uds_recd(recd):
#takes in a received dataframe and processes it
    if len(recd.data) == 8:  # to avoid error bytes
        can_def.disp_uds(recd)
        global last_rec
        #print("here is the global last_recd in proc_uds: ", last_rec.data)
        last_rec = recd  # this would always be reserved as single frame or first frame
        if (recd.data[0] >> 4 == 1):  # this means consecutive frames will be sent
            #print("first frame")
            byte_length = (0 + recd.data[1])
            set_pl_count(byte_length)
            full_cf = int((byte_length - 6) / 7)  # number of full consecutive frames
            if (byte_length - 6) % 7 == 0:  # will there be a partially filled frame at the end?
                cf = full_cf
            else:
                cf = full_cf + 1
            set_multi_frame(cf)
            set_cf_count_proc(cf)
            append_large_frame(last_rec)
            tx_rec_cf(0)
        if (recd.data[0] >> 4 == 2) & (cf_count > 0):
            #print("consecutive frame")
            dec_cf_count()
            append_large_frame(last_rec)

def quick_tx(msg):
# will process the string and convert it to the data frame and
    framedata, mf = can_def.strhex2uds(msg)
    tx_uds(framedata, mf)
    time.sleep(.01)

#Creating a class for Tester Present repetitive ping so instances of thread may be created.
class TP_send(threading.Thread):
    def __init__(self, arg):
        super().__init__()
        self.arg = arg
        self._stop_event = threading.Event()

    def run(self):
        # a message announcing that the thread has started.
        #print(f"Task started with argument: {self.arg}")
        while not self._stop_event.is_set():
            # the actual task goes in here.
            tping, mf = can_def.strhex2uds('3e')
            tx_uds(tping, mf)
            time.sleep(.95)  # Task work simulation

    def stop(self):
        self._stop_event.set()

multi_frame = 0
def set_multi_frame(int):
    global multi_frame    # Needed to modify global copy of globvar
    multi_frame = int
    set_cf_count(int)

cf_count = 0
def set_cf_count(int):
    global cf_count    # Needed to modify global copy of globvar
    cf_count = int

cf_count_proc = 0
def set_cf_count_proc(int):
    global cf_count_proc
    cf_count_proc = int
def dec_cf_count():
    global cf_count    # Needed to modify global copy of globvar
    cf_count = cf_count-1

pl_count = 0
def set_pl_count(int):
    global pl_count
    pl_count = int

large_frame = []
def append_large_frame(frame):
    global large_frame
    large_frame.append(frame)
    #for x in range(len(large_frame)):
        #print("frame#", x, ": ", (binascii.hexlify(large_frame[x].data)).decode())

def unlock_using_token_dll():
    global large_frame, last_rec, df
    print("requesting seed")
    quick_tx('2761')
    # a large frame tupple should have been created...
    time.sleep(.010)  # need this to process the frame
    seed = can_def.proc_seed(large_frame, cf_count_proc, pl_count)
    challenge = [str(i) for i in seed]  # it needs to be sent as a string...
    # compute_key_from_seed is defined in can_def
    key = can_def.compute_key_from_seed(py32bit, script_path, challenge)
    seed, mf = can_def.strhex2uds(key)
    tx_uds(seed, mf)
    time.sleep(.5)
    # reset everything incase this is looped:
    set_multi_frame(0)
    set_pl_count(0)
    del large_frame[:]

def pw_req():
    global large_frame, last_rec, df
    print("requesting pw")
    quick_tx('22f13d')
    # a large frame tupple should have been created...
    time.sleep(.050)  # need this to process the frame
    pw = can_def.proc_pw(large_frame, cf_count_proc, pl_count)
    print(pw[0])
    len_of_df = df.shape[0]
    df.iat[len_of_df-1, 0] = df.iat[len_of_df-1, 0] + ' ' + pw[0]
    time.sleep(.5)
    # reset everything incase this is looped:
    set_multi_frame(0)
    set_pl_count(0)
    del large_frame[:]

#SCRIPT STARTS HERE

column_names = ['Messages']
df = pd.DataFrame(columns = column_names)

last_rec = Frame(id_=did, data=bytearray((0).to_bytes(8, 'big')), flags=canlib.MessageFlag.FDF | canlib.MessageFlag.BRS | canlib.MessageFlag.EXT)

# open channel (only 1 channel on the kvaser)
ch_a = canlib.openChannel(
    channel=0,
    flags=canlib.Open.CAN_FD,
    bitrate=canlib.BitrateFD.BITRATE_500K_80P,
    data_bitrate=canlib.BitrateFD.BITRATE_2M_80P,
)
# activate CAN chip
ch_a.busOn()

end_rx = threading.Event()  #recd
rx = threading.Thread(target=rx_uds) #thread for receiving messages only
rx.start()

tp1 = TP_send(1)
tp1.start()

############################################################################
#####################FIRST SEQUENCE STARTS HERE ############################
############################################################################
time.sleep(.5)
quick_tx('1003')
time.sleep(.5)

#unlock unit
print("pause tester present signal")
tp1.stop()
tp1.join()
unlock_using_token_dll()

time.sleep(.5)

print("\nresume tester present signal")
tp2 = TP_send(1)
tp2.start()

############################################################################
################### SECOND SEQUENCE STARTS HERE ############################
############################################################################
time.sleep(.1)
quick_tx('1002')
time.sleep(1)
print("pause tester present signal")
tp2.stop()
tp2.join()

unlock_using_token_dll()

time.sleep(.5)

pw_req()

ch_a.busOff()
# close channel
ch_a.close()

end_rx.set()
rx.join()

############################################################################
####################### PROCESS DATA FRAME HERE ############################
############################################################################
projdirectory = os.path.dirname(os.path.realpath(__file__))
#process the df and get ready to write to file:
tocsvdf = df['Messages'].str.split(" ", n=4, expand=True)
col_names = {0: 'Rx/Tx', 1: ':', 2: 'ID', 3: 'Hex', 4: 'Desc'}
print(tocsvdf)
tocsvdf.rename(columns=col_names, inplace=True)

#get serial number from log file that you will add to
currentdir = projdirectory + '/Current'
file = glob.glob(os.path.join(currentdir, "*.csv"))[0]
filename = file.split("\\")[-1]
sn = filename.split(".")[0]
fromcsvdf = pd.read_csv(file, dtype={'ID': 'str'})
fromcsvdf = fromcsvdf.drop(fromcsvdf.columns[[0]], axis=1)

#now concatenate and overwrite
newdf = pd.concat([fromcsvdf, tocsvdf])
newdf.reset_index(drop=True, inplace=True)
newdf.to_csv(f'{currentdir}/{sn}.csv')

exit()