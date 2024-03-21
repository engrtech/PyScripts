from ctypes import *

# Let's say you have a pointer to an integer with value 42
int_var = c_int(42)
pointer_to_int_var = pointer(int_var)

# If you print the pointer, you might get a description of the pointer
# e.g., <__main__.LP_c_int object at ...> or <cparam 'P' ...>
print(pointer_to_int_var)

# To print the address stored by the pointer, use ctypes.addressof()
print("Address:", addressof(int_var))

# If you want to print the value pointed to by the pointer
print("Value at address:", pointer_to_int_var.contents.value)