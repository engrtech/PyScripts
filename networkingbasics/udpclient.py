#!usr/bin/python

import socket

sock = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)      # For UDP

udp_host = socket.gethostname()		# Host IP. This is what it will aim for.
udp_port = 12345			        # specified port to connect. This is what it will aim for.

msg = "Hello Python2!"
print("UDP target IP:", udp_host)
print("UDP target Port:", udp_port)

sock.sendto(msg.encode(),(udp_host,udp_port))		# Sending message to UDP server