#Vyasan Valavil
#03-21-2024
#create a DLL using VS. #python doesn't have pointers.
#We are mostly working with STRINGS in this script

import ctypes

#load the dll
path = 'C:/CFiles/ctypes_tutorial/x64/Debug/ctypes_tutorial.dll'
clibrary = ctypes.CDLL(path)

#this is how a function from the dll is called:
clibrary.test() #this is just a "hello world" function.

#you can just rename a function like this for simplicity
add = clibrary.add

#use the function without defining function parameters
print(add(1,2))

#it works... but now let's define function parameters
#it takes two int and returns an int...
add.argtypes = [ctypes.c_ushort, ctypes.c_ushort]
add.restype = ctypes.c_int

#it works just as well in this case.
print(add(1,4))

#HOWEVER for strings its different.
#strings are immutable...

#sending just the string to a char * str will print out just 'J'
#display contains a printf statement.
clibrary.display("John")

#so you need to convert it with a b"   " for BINARY
#Now it will print "John"
clibrary.display(b"John")

#IMPORTANT: how about variables?
last_name = "Smith" #now it is no longer a raw string.
#this wont work: #It will again only print the first letter...
clibrary.display(last_name)
#it needs to be encoded!
clibrary.display(last_name.encode())

#send a string variable to increment each character and print it...
#NOTE : we are not using the display function,
#we are just printing it here after sending it through a function...
string = "Hello"
print("Before:", string)
clibrary.increment(string)
#you will see that it has not been incremented
print("After:", string)

#to make string 'C-ready' send the pointer!!! cstring...
cstring = ctypes.c_char_p(b"Hello")
#now they will work... beause we are sending char pointers...
print("Before:", cstring, cstring.value)
clibrary.increment(cstring)
print("After: ", cstring, cstring.value)

#now what if we change the above string completely?
print("\nUsing c_char_p(b\"Hello\") and changing variable content:")
cstring.value = b"World"
print("After: ", cstring, cstring.value)
print("c_char_p is not good for mutable memory.")
#The MEMORY LOCATION CHANGED!

#THEREFORE use STRING BUFFERS for MUTABLE MEMORY!!!:
print("\nUsing create_string_buffer(b\"Hello\")")
cstring = ctypes.create_string_buffer(b"Hello")
print("Before: ", cstring, cstring.value)
clibrary.increment(cstring)
cstring.value = b"World"
print("After: ", cstring, cstring.value)
#The MEMORY LOCATION STAYED THE SAME!!!

# Defining alloc function and it's return type
#print("\nFunctions to create/Allocate memory for a string in the C function...")
alloc_func = clibrary.alloc_memory
alloc_func.restype = ctypes.POINTER(ctypes.c_char) #RETURNS SOMETHING

# Defining free function and it's return type
#print("\nFunctions to delete memory for a string in the C function...")
free_func = clibrary.free_memory
free_func.argtypes = [ctypes.POINTER(ctypes.c_char)] #ONLY SEND NO RETURN

# Using the functions to return a string
print("\nWe create the string ptr in C++ and save it as c_string_pointer")
cstring_pointer = alloc_func()
print("We GRAB the string from the ptr using c_char_p.from_buffer(cstring_pointer)")
str = ctypes.c_char_p.from_buffer(cstring_pointer)

print("String Value : ", str.value)

# Freeing memory
free_func(cstring_pointer)

print("String Value after freeing memory : ", str.value)

print("\nCAPTURES : \n")