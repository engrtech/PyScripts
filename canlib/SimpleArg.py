#this needs to run with py1311-32 if it needs to work with dlls
#subprocess will call this script in a virtual environment
import ctypes
from ctypes import *
import ctypes.wintypes as w

my_dll = ctypes.CDLL("C:/CFiles/test_dll/SimpleArg/x64/Debug/SimpleArg.dll")
# Function name according to your DLL's export table

BYTE = ctypes.c_ubyte
USHORT = ctypes.c_ushort

##########################
#######    -1-   #########
func1 = my_dll.test_Mode
Mode = 0x61

func1.argtypes = [
    ctypes.c_ubyte                  # Mode CHAR
]
func1.restype = ctypes.c_bool

success1 = func1(
    ctypes.c_ubyte(Mode)
)
print("success1", success1)

##########################
#######    -2-   #########
func2 = my_dll.test_seed
seed = bytearray([0x3e, 0x16, 0x8c, 0x09, 0x34, 0xa4, 0xae, 0x73, 0xfb, 0xd5, 0x0a, 0x50, 0xc8, 0xf6, 0x38, 0xe2])
seed_byte_array = (c_ubyte * 16)(*seed)

func2.argtypes = [
    ctypes.POINTER(BYTE)
]
func2.restype = ctypes.c_bool

success2 = func2(
    seed_byte_array
)
print("success2", success2)

##########################
#######    -3-   #########
func3 = my_dll.test_sizeSeed
sizeSeed = 16
sizeSeed = USHORT(sizeSeed)

func3.argtypes = [
    ctypes.c_ushort                  # Mode USHORT
]
func3.restype = ctypes.c_bool

success3 = func3(
    sizeSeed
)
print("success3", success3)

##########################
#######    -4-   #########

print("\n")

func4 = my_dll.test_key
key = [97, 97, 97] #this is giving \n...
key = bytearray(key)
byte_array = (c_ubyte * 240)(*key)
print("seed address of first index BEFORE function", hex(id(byte_array[0])), "    contents : ", byte_array[0])
print(byte_array)#this would be an object at an address...

func4.argtypes = [
    ctypes.POINTER(BYTE)
]
func4.restype = ctypes.c_bool

success4 = func4(
    byte_array
)
print("seed address of first index AFTER function", hex(id(byte_array[0])), "    contents : ", byte_array[0])
print(*byte_array)
print(byte_array)
print("success4", success4)

print("\n")

##########################
#######    -5-   #########

func5 = my_dll.test_maxSizeKey
maxSizeKey = 240
maxSizeKey = USHORT(maxSizeKey)

func5.argtypes = [
    ctypes.c_ushort                  # Mode USHORT
]
func5.restype = ctypes.c_bool

success5 = func5(
    maxSizeKey
)
print("success5", success5)

##########################
#######    -6-   #########

func6 = my_dll.test_sizeKey
#sizeKey = USHORT()
#sizeKey = ctypes.byref(sizeKey)
sizeKey = ctypes.c_ushort()  # instance of C unsigned short

func6.argtypes = [ctypes.POINTER(ctypes.c_ushort)]               # sizeKey (pointer to USHORT)
func6.restype = ctypes.c_bool

success6 = func6(ctypes.byref(sizeKey))
#print(sizeKey)
print("success6", sizeKey.value)
#print(type(sizeKey.value))

print("\n")