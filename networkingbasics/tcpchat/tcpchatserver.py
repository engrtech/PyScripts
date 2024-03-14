'Chat Room Connection - Client-To-Client'

# thread is a sequence of instructions in a program

import threading
import socket

host = '127.0.0.1' #local host
port = 59000 # make sure this isn't an open port. run netstate in cmd
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM) #create server object...
server.bind((host, port)) #it accepts a TUPLE!!!
server.listen()
clients = []
aliases = []

def broadcast(message): #to send a message to all clients
    for client in clients:
        client.send(message)

# Function to handle clients'connections
def handle_client(client):
    while True:
        try:
            message = client.recv(1024)#maximum about of bytes that the server can receive.
            print("client sent a message...")
            broadcast(message)
        except:
            index = clients.index(client)
            clients.remove(client) #if there is an error then remove that client...
            client.close()
            alias = aliases[index] #also need to remove the alias...
            broadcast(f'{alias} has left the chat room!'.encode('utf-8'))
            aliases.remove(alias)
            break

# Main function to receive the clients connection
def receive():
    while True:
        print('Server is running and listening ...')
        client, address = server.accept() #returns socket, ip, and port
        print(f'connection is established with {str(address)}')
        client.send('alias?'.encode('utf-8'))
        alias = client.recv(1024) #max byte size
        print(f'adding {str(alias)}')
        aliases.append(alias)
        clients.append(client)
        print(f'The alias of this client is {alias}'.encode('utf-8'))
        broadcast(f'{alias} has connected to the chat room'.encode('utf-8'))
        client.send('you are now connected!'.encode('utf-8'))
        #multi-threading by creating thread object...
        thread = threading.Thread(target=handle_client, args=(client,))
        thread.start()

if __name__ == "__main__":
    receive()