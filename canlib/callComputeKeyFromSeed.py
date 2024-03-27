import can_def
import sys

print("The python interpreter being used is:")
print(sys.executable)

# The path to the Python interpreter you want to use token_dll may require 32-bit Python
py32bit = 'C:/Users/vyasan.valavil/py32bit/Scripts/python.exe'
# The path to your 32
script_path = 'ComputeKeyFromSeed.py'

challenge = [0xd1, 0xb2, 0xb0, 0xc6, 0xcd, 0x0, 0x3b, 0x1d, 0x4b, 0xea, 0xeb, 0x77, 0x86, 0x09, 0x75, 0x93]
#challenge = [209, 178, 176, 198, 205, 0, 59, 29, 75, 234, 235, 119, 134, 9, 117, 147]
challenge = [str(i) for i in challenge]
#compute_key_from_seed is defined in can_def
key = can_def.compute_key_from_seed(py32bit, script_path, challenge)