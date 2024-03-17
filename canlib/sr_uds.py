from canlib import canlib, Frame
import can_def
import threading
import time
import subprocess


def tx_uds(framedata, mf):
    if mf == 0:
        tx_sf_uds(framedata)
    else:
        tx_mf_uds(framedata)


def tx_sf_uds(framedata):
    frame = Frame(id_=0x7E0, data=framedata, flags=canlib.MessageFlag.STD)
    ch_a.write(frame)
    can_def.disp_uds(frame)


def tx_mf_uds(framedata):
    # send first frame
    frame = Frame(id_=0x7E0, data=framedata[0], flags=canlib.MessageFlag.STD)
    ch_a.write(frame)
    can_def.disp_uds(frame)
    time.sleep(.005)
    # now check the response
    conf, st = can_def.chk_resp(last_rec)
    if conf:
        for x in range(len(framedata) - 1):
            time.sleep(st)  # separation time
            frame = Frame(id_=0x7E0, data=framedata[x + 1], flags=canlib.MessageFlag.STD)
            ch_a.write(frame)
    time.sleep(.010)


def rx_uds():
    while (1):
        recd = ch_a.read(timeout=60000)
        proc_uds(recd)


def proc_uds(recd):
    if len(recd.data) == 8:  # to avoid error bytes
        can_def.disp_uds(recd)
        last_rec = recd  # this would always be reserved as single frame or first frame
        if (recd.data[0] >> 4 == 1):  # this means consecutive frames will be sent
            print("first frame")
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
        if (recd.data[0] >> 4 == 2) & (cf_count > 0):
            print("consecutive frame")
            dec_cf_count()
            append_large_frame(last_rec)

def quick_tx(msg):
    while hold_tx:
        time.sleep(1)
    framedata, mf = can_def.strhex2uds(msg)
    tx_uds(framedata, mf)
    time.sleep(.01)


def tp_send():
    while (1):
        while hold_tx:
            time.sleep(1)
        framedata, mf = can_def.strhex2uds('3e')
        tx_uds(framedata, mf)
        time.sleep(1)


multi_frame = 0
def set_multi_frame(int):
    global multi_frame    # Needed to modify global copy of globvar
    multi_frame = int
    set_cf_count(int)

hold_tx = False

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
    print("frame is now : ", len(large_frame))

last_rec = Frame(id_=0x7E0, data=bytearray((0).to_bytes(8, 'big')), flags=canlib.MessageFlag.STD)

# open channel (only 1 channel on the kvaser)
ch_a = canlib.openChannel(channel=0)
# set bus parameters
ch_a.setBusParams(canlib.canBITRATE_500K)
# activate CAN chip
ch_a.busOn()

tp2 = threading.Thread(target=rx_uds)
tp2.start()

tp3 = threading.Thread(target=tp_send)
tp3.start()

# The path to the Python interpreter you want to use
py32bit = 'C:/PyScripts/canlib/venv/Scripts/python.exe'
# The path to your script
script_path = 'load_dll.py'


quick_tx('1001')
time.sleep(.95)
quick_tx('1003')
time.sleep(.95)
quick_tx('1002')
time.sleep(.95)
print("requesting seed")
quick_tx('2761')
time.sleep(.050)
can_def.proc_seed(large_frame, cf_count_proc, pl_count)
#seed = can_def.proc_seed(large_frame, cf_count_proc, pl_count)
# Running the script
key = (subprocess.run([py32bit, script_path, str('test')], capture_output=True, text=True))
print(key.stdout)

time.sleep(1)

#reset everything:
set_multi_frame(0)
set_pl_count(0)
del large_frame[:]

while (1):
    time.sleep(1)

# while (1):
## create frame and transmit
# msg = '23247001ad080004'
# framedata, mf = can_def.strhex2uds(msg)
# tx_uds(framedata, mf)
# time.sleep(5)

ch_a.busOff()
# close channel
ch_a.close()


exit()