import subprocess
import sys

respreqtx = ['1002', '1003', '3e00', '2761', '2762']
respreqrx = ['5002', '5003', '7e00', '6761', '6762']

def str2udstupple(msg_string):
    if len(msg_string) % 2 != 0:
        sys.exit(1)  # do not accept odd length messages
    dl = int(len(msg_string) / 2)
    if len(msg_string) <= 14:
        for i in range(7 - dl): msg_string = msg_string + '00'  # individual dataframes MUST be 8 bytes
        framedata = [int(hv, 16) for hv in [msg_string[i:i + 2] for i in range(0, len(msg_string), 2)]]
        framedata.insert(0, dl) #add the data length to the start of the frame
        framestring = f'0{dl}{msg_string}'
        #print(f'framedata: {framedata}') #type = list of int
        #print(f'framestring: {framestring}') #type = string
    else:
        print("message needs flow control")
        framestring = []
        framedata = []
        for i in range(6 - (dl + 1) % 7): msg_string = msg_string + '00'  # individual dataframes MUST be 8 bytes with fc.
        for i in range(int(((len(msg_string) / 2) + 1) / 7)):
            if i == 0: #The first frame
                udsstring = f'1{format(dl, "03x")}{msg_string[0:12]}'
                framestring.append(udsstring)
                udsdata = [int(hv, 16) for hv in [udsstring[k:k + 2] for k in range(0, len(udsstring), 2)]]
                framedata.append(udsdata)
            if i > 0: #All the Consecutive Frames
                udsstring = f'2{format(i % 16, "01x")}{msg_string[(12 + (i - 1) * 14):(12 + (i - 1) * 14 + 14)]}'
                framestring.append(udsstring)
                udsdata = [int(hv, 16) for hv in [udsstring[k:k + 2] for k in range(0, len(udsstring), 2)]]
                framedata.append(udsdata)
        #print(f'framedata: {framedata}') #type = list of list of int
        #print(f'framestring: {framestring}') #type = list of strings
    return framedata, framestring #returns different type of data depending on length of message...

def compute_key_from_seed(arguments):
    global script_path
    command = ['py', '-3.11-32', 'ComputeKeyFromSeed.py'] + arguments
    try:
        result = subprocess.run(
            command,  # Command to execute
            stdout=subprocess.PIPE,  # Capture standard output
            stderr=subprocess.PIPE,  # Capture standard errors
            text=True  # Output will be treated as text (Python 3.7+); use 'universal_newlines=True' for Python <3.7
        )
        #print("result", result)
        #print('stdout:', result.stdout)
        #print('stderr:', result.stderr)
        # Check if the command was successful
        if result.returncode == 0:
            print("The ComputeKeyFromSeed script ran successfully")
            key_ba_as_string = result.stdout
        else:
            print(f"The command to run ComputeKeyFromSeed resulted in an error {result.returncode}")
        key = ''.join(format(int(x), '02x') for x in key_ba_as_string.split())
        return key
    except subprocess.CalledProcessError as e:
        print(f"An error occurred while trying to run the key-generation script: {e}")