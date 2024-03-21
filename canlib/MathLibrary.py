#this needs to run with py1311-32 if it needs to work with dlls
#subprocess will call this script in a virtual environment
import ctypes

my_dll = ctypes.WinDLL("C:/CFiles/test_dll/MathLibrary/x64/Debug/MathLibrary.dll")
# Function name according to your DLL's export table
func1 = my_dll.fibonacci_init

func4 = my_dll.fibonacci_index

func1(1,1)

print(func4())

key = "LOOOOOOOOOOOOOOOOONGGGGG_KEEEEEEEEEEY"

print(key) #this will be sent back to sr_can