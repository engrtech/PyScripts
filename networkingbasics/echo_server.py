#!usr/bin/python

import socket
host = socket.gethostname()
port = 12345
s = socket.socket()		# TCP socket object
s.bind((host,port))
s.listen(5)

print("Waiting for client...")
conn,addr = s.accept()	        # Accept connection when client connects
print("Connected by ", addr)

while True:
	data = conn.recv(1024)	    # Receive client data
	if not data: break	        # exit from loop if no data
	conn.sendall(data)	        # Send the received data back to client
	print("some data was received and sent back")
conn.close()