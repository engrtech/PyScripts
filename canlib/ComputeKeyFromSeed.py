#PYTHON 11-32 REQUIRED for this script and token_dll.dll!!!
#subprocess will be calling this script in a virtual environment
import ctypes
from ctypes import *
import sys

#print("The python interpreter being used is:")
#print(sys.executable)

#gather the arguments as a atring and
seed = [int(arg) for arg in sys.argv[1:]]

#location of dll
token_dll = ctypes.CDLL("C:/SVN/LaForge/Tools/ESL_Token_Generation/Token_DLL/bin_dll_msvc/token_dll.dll")
create_key_func = token_dll.KWP2000_ComputeKeyFromSeed

#Shorter ctype variables for convenience.
BYTE = ctypes.c_ubyte
USHORT = ctypes.c_ushort

#1 mode
Mode = 0x61

#2 seed
seed_byte_array = (c_ubyte * 16)(*seed)                  #byte*

#3 sizeSeed
sizeSeed = 0x10
sizeSeed = USHORT(sizeSeed)                               #short

#4 key
key = [1]
key_byte_array = (c_ubyte * 256)()

#5 maxSizeKey
maxSizeKey = 256
maxSizeKey = USHORT(maxSizeKey)

#6 sizeKey
sizeKey = USHORT()

# Define argument types to match KWP2000_ComputeKeyFromSeed
create_key_func.argtypes = [
    BYTE,                           # Mode CHAR
    ctypes.POINTER(BYTE),           # seed (pointer to BYTE)
    USHORT,                         # sizeSeed USHORT
    ctypes.POINTER(BYTE),           # key (pointer to BYTE)
    USHORT,                         # maxSizeKey USHORT
    ctypes.POINTER(USHORT)          # sizeKey (pointer to USHORT)
]
# Defining the only return type from KWP2000_ComputeKeyFromSeed
create_key_func.restype = ctypes.c_bool

success = create_key_func(
    ctypes.c_ubyte(Mode),
    seed_byte_array,
    sizeSeed,
    key_byte_array,
    maxSizeKey,
    ctypes.byref(sizeKey)
)

print(*key_byte_array) #this will be captured by the calling program

exit()