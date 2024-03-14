import time
import sys
#this needs to run with py1311-32 if it needs to work with dlls
#subprocess will call this script in a virtual environment
import ctypes

#mode = sys.argv[1]
#seed = sys.argv[2]

my_dll = ctypes.WinDLL("C:/SVN/LaForge/Tools/ESL_Token_Generation/Token_DLL/bin_dll_msvc/token_dll.dll")
# Function name according to your DLL's export table
my_function = my_dll.KWP2000_ComputeKeyFromSeed

my_function()

key = "LOOOOOOOOOOOOOOOOONGGGGG_KEEEEEEEEEEY"

print(key) #this will be sent back to sr_can