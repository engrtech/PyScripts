#Vyasan Valavil
#03-21-2024
#We are still going to use the ctypes_tutorial.dll
#We will work with integers here

import ctypes

#load the dll
path = 'C:/CFiles/ctypes_tutorial/x64/Debug/ctypes_tutorial.dll'
clibrary = ctypes.CDLL(path)

#ctypes.POINTER() only accepts ctypes...
#There is a difference between ctypes.pointer() and ctypes.POINTER().
#ctypes.pointer() is a bit slower.

num1ptr = ctypes.pointer(ctypes.c_int(100))
print(num1ptr) #this will print the ctype object and its value
print(num1ptr.contents.value) #this will print the value that is points to

#working with ARRAYS:
array = (ctypes.c_int * 10)()
#the type of data times the number of elements.
#the () is a sort of constructor

#pass the array and its length...
x = clibrary.sum(array, len(array))
print(clibrary.sum(array, 10)) # it will default to 0

#now give it some values:
for i in range(10):
    array[i] = i

#passing it with new values will yield a new sum
x = clibrary.sum(array, len(array))
print(clibrary.sum(array, 10))

#Here is a quick example of creating and sending an array
values = [5, 7, 8, 3, 6, 8, 9, 6, 3, 2]
array = (ctypes.c_int * 10)(*values)
y = clibrary.sum(array, len(array))
print(y)
print(clibrary.sum(array, 10))