#We are still going to use the ctypes_tutorial.dll

import ctypes

#load the dll
path = 'C:/CFiles/ctypes_tutorial/x64/Debug/ctypes_tutorial.dll'
clibrary = ctypes.CDLL(path)

#ctypes.POINTER() only accepts ctypes...


