
# even numbered string to bytearray
# number of bytes is always half the number of charactesr
output_ba = bytearray.fromhex('1003')
print(output_ba)

# converting byte array to bytes
print(bytes(output_ba))

# selecting a SINGLE element in a bytearray will always give an integer
print(bytes(output_ba)[0])
print(type(bytes(output_ba)[0]))

# byte arrays can be added
long_ba = bytearray.fromhex('6761') + bytearray.fromhex('3e168c0934a4ae73fbd50a50c8f638e2')
print(long_ba)

print(long_ba[3])
if long_ba[3] >> 4 == 1:
    print(bytearray(long_ba[2]))
