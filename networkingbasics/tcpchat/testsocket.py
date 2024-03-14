'''Socket Programming in Python'''
import socket
import sys

try:
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # AF_INET internet protocol version 4
    # SOCK_STREAM a connection oriented tcp (connection has to be established before any data is transferred)
    print('socket succesfully created!')
except socket.error as err:
    print(f'socket creation failed with error {err}')

#default port for the server
port = 80

try:
    # get the ip address of the website
    host_ip = socket.gethostbyname('www.github.com')
except socket.gaierror:
    # means there is an error with DNS. the service that associates the name with the IP
    print('error resolving the host')
    sys.exit()
#now connect to the server...
s.connect((host_ip, port)) #this is a tupple
print(f'Socket has succesfully connected to Github on port == {host_ip}')