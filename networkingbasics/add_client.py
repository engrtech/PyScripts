#!usr/bin/python

import socket

host = socket.gethostname()
port = 12347

a = str(input('Enter first number: '))	# Enter the numbers
b = str(input('Enter second number: '))	# to be added
c = a+','+b					# Generate a string from numbers

print("Sending string {0} to server" .format(c))

s = socket.socket()
s.connect((host,port))

s.sendall(c.encode())				# Send string 'c' to server
data = s.recv(1024)			# receive server response
print(int(data)) 			# convert received dat to 'int'

s.close()					#Close the Connection