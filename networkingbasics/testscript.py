#!/usr/bin/python

#This is tcp_server.py script

import socket			                #line 1: Import socket module

s = socket.socket()		                #line 2: create a socket object
host = socket.gethostname()	            #line 3: Get current machine name
port = 9999			                    #line 4: Get port number for connection

s.bind((host,port))		                #line 5: bind with the address

print("Waiting for connection...")
s.listen(5)			                    #line 6: listen for connections

print("done listening")

while True:
	conn,addr = s.accept()            #line 7: connect and accept from client
	print('Got Connection from', addr)
	conn.send('Server Saying Hi')
	conn.close()		                #line 8: Close the connection