# All communication in this server is encoded to ascii
# !/usr/bin/python
# Import necessary Libraries
import threading as th
import socket as sc
import sys

# Localhost
host = '127.0.0.1'
# Input Port Number as command line argument
port = int(sys.argv[1])

# AF_INET - IPv4 networking socket
server = sc.socket(sc.AF_INET, sc.SOCK_STREAM)
# Bind host to port
server.bind((host, port))
server.listen()

# Maintain list of clients connected to server on same port
clients = []
names = []

# Function to broadcast message sent by one client to all clients
def broadcast_message(msg):
    for x in clients:
        x.send(msg)

# Function to receive message from a client
def receive_message(client):
    while True:
        try:
            # Receive message from client and broadcast using server
            msg = client.recv(1024)
            broadcast_message(msg)
        except:
            # In case of error client is removed / disconnected from server
            x = clients.index(client)
            clients.remove(client)
            client.close()
            name = names[x]
            broadcast_message(f'{name} left the chat.'.encode('ascii'))
            names.remove(name)
            break

# Function to connect clients to the server
def connect_clients():
    while True:
        # Establish connection with client
        client, address = server.accept()
        print(f'Connected with {str(address)}')

        client.send('NAME'.encode('ascii'))
        name = client.recv(1024).decode('ascii')
        # Get name of client and append to client list
        names.append(name)
        clients.append(client)
        print(f'Client name is {name}')

        broadcast_message(f'{name} joined the chat.'.encode('ascii'))
        client.send('Connected to server!'.encode('ascii'))

        # Create threads of receive message function as to simultaneously receive from multiple clients
        thread = th.Thread(target=receive_message, args=(client,))
        thread.start()


def boot_server():
    print('Server has been Booted!')
    connect_clients()


boot_server()