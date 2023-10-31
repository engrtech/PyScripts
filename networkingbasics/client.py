#!/usr/bin/python

#This is tcp_client.py script

import socket

s = socket.socket()
host = socket.gethostname()	        # Get current machine name
port = 9999			                # Client wants to connect to server's
				                    # port number 9999
s.connect((host,port))
print(s.recv(1024))	                # 1024 is bufsize or max amount
				                    # of data to be received at once
s.close()