#!usr/bin/python

# block_server.py

import socket

s = socket.socket()

host = socket.gethostname()
port = 12345

s.bind((host, port))
s.listen(5)

while True:
    conn, addr = s.accept()  # accept the connection

    data = conn.recv(1024).decode()
    while data:  # till data is coming
        print(data)
        data = conn.recv(1024)
    print("All Data Received")  # Will execute when all data is received
    conn.close()
    break