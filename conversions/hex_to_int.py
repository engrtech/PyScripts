#IMPORTANT: hex is stored as an integer...
hex_num = 0x2a
print(hex_num)
print(type(hex_num)) #this will output an integer

#if the hex is a string:
hex_string = "2a"  # Example hexadecimal string
integer_number = int(hex_string, 16)
print(integer_number)  # Output will be 42

hex_string_with_0x = "0x2a"  # Example hexadecimal string
integer_number = int(hex_string_with_0x, 16)
print(integer_number)  # Output will be 42