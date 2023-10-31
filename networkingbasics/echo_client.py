#!usr/bin/python

import socket
host = socket.gethostname()
port = 12345
s = socket.socket()		# TCP socket object

s.connect((host,port))

sendmsg = 'This will be sent to server'
s.sendall(sendmsg.encode())    # Send This message to server

data = s.recv(1024)	    # Now, receive the echoed
					    # data from server

print("this is what was sent :")
print(data)             # Print received(echoed) data
s.close()				# close the connection