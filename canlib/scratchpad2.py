from canlib import canlib

num_channels = canlib.getNumberOfChannels()

print(f"Found {num_channels} channels")