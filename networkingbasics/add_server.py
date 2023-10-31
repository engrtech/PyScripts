#!usr/bin/python

import socket

host = socket.gethostname()
port = 12345
s = socket.socket()  # TCP socket object
s.bind((host, port))

s.listen(5)

conn, addr = s.accept()
print("Connected by ", addr)
while True:
    data = conn.recv(1024).decode()
    print("data received after decoding : ")
    print(data)
    if not data:
        print("no more data sent")
        break
    # Split the received string using ','
    # as separator and store in list 'd'
    d = data.split(",")
    print("this is the data after being split:")
    print(d[0], d[1])

    # add the content after converting to 'int'
    data_add = int(d[0]) + int(d[1])

    print("sending data")
    conn.sendall(str(data_add).encode())  # Send added data as string
    print("data sent")
    # String conversion is MUST!
conn.close()