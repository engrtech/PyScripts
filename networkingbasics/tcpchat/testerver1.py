# First, the server has a bind() method which binds to a specific ip and port so it can listen to incoming requests.

# Second, the server has a Listen() method which puts the server into a  listen mode which allows the server to listen to
# incoming connections.

# Last we have accept and close() methods.
# accept() : intiates a connection with the client.
# close()  :  closes the connection with the client.

import socket

s = socket.socket()
print('Socket succesfully created')
port = 56789
s.bind(('', port))
print(f'socket binded to port{port}')
s.listen(5) #five connections max!!!
print('Socket is listening')

while True: #a forever loop...
    c, addr = s.accept() #the accept happens whenever it receives a connection... and it stores the ip and port...
    #print(c) #c is the connection... has info on listening ip:port and sending ip:port
    print('Got connection from', addr)
    message = ('Thank you for connecting')
    c.send(message.encode()) #need to send in the form of bytes...
    c.close()

#you can use the telnet command in cmd in linux:
# telnet localhost 56789