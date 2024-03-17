import binascii

#send/receive functions
#only converts frame to a readable format takes in entire frame (id and data)
def disp_uds(frame):
    id = frame.id
    id = (hex(id)[2:]).upper()
    data = (binascii.hexlify(frame.data)).decode()
    if (data[2:4] == '3e')|(data[2:4] == '7e'):
        msg = id + " " + data
    else:
        msg = id + " " + data
        print(msg)
    return msg

#send functions
#create functions to convert a string to the data component in a Frame
def strhex2uds(input):
    output_ba = bytearray.fromhex(input)
    lop = len(output_ba)
    if lop <= 7:
        return strhex2uds_sf(bytes(output_ba))
    else:
        return strhex2uds_mf(bytes(output_ba), lop)

def strhex2uds_sf(bytes):
    blen = bytearray(len(bytes).to_bytes(1, 'big'))
    seven_byte = pad_bytearray(bytes, 7)
    single_frame = blen + seven_byte
    return single_frame, 0

def strhex2uds_mf(bytes, lop):
    f2b = bytearray((4096+lop).to_bytes(2, 'big')) #first two bytes that contain ff nibble and lop
    ff = f2b + bytes[:6] #first frame bytes 0-5
    if (lop-6)%7>0:
        rf_count = int((lop-6)/7)+1
    else:
        rf_count = int((lop-6)/7)
    #start mf tuple:
    mf = [ff]
    for i in range(rf_count):
        cf_count = i+1
        cf = bytes[(6+i*7):(13+i*7)]
        fb = (cf_count + 32) #this is an int
        if cf_count == rf_count:
            cf = pad_bytearray(cf, 7)
        cf_id = bytearray(fb.to_bytes(1, 'big'))
        mf.append(cf_id+cf)
    return mf, 1
def pad_bytearray(b_array, block_size, padding_byte=0):
    padding_needed = (block_size - len(b_array)) % block_size
    if padding_needed == 0:
        return b_array  # No padding needed
    padding = bytearray([padding_byte] * padding_needed)
    return b_array + padding

def chk_resp(frame):
    if frame.data[0] & 0x30 == 48:
        print("separation time :", frame.data[2])
        return True, frame.data[2]/1000 #YES, ST in seconds
    return False, 0

def proc_seed(large_frame_list, frame_count, pl_count):
    pl_count = pl_count - 2 #we dont need the 67 61
    frames_remaining = frame_count
    pl_remaining = pl_count
    payload = []
    for frame in large_frame_list:
        if frames_remaining == frame_count:
            for x in range(4):
                if pl_remaining != 0:
                    payload.append(frame.data[4+x])
                    pl_remaining = pl_remaining-1
            frames_remaining = frames_remaining - 1
        else:
            for x in range(7):
                if pl_remaining != 0:
                    payload.append(frame.data[1+x])
                    pl_remaining = pl_remaining - 1
            frames_remaining = frames_remaining-1
    print(payload)
    return payload
