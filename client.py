# !/usr/bin/python
# import necessary libraries
import threading as th
import socket as sc
import sys

# localhost
host = '127.0.0.1'
# input port number as command line argument
port = int(sys.argv[1])
# input username as command line argument
name = str(sys.argv[2])

# AF_INET - IPv4 networking socket
client = sc.socket(sc.AF_INET, sc.SOCK_STREAM)
# Bind host to port
client.connect((host, port))

# Function to establish client connection to server
def connect_to_server():
    while True:
        try:
            msg = client.recv(1024).decode('ascii')
            if msg == 'NAME':
                client.send(name.encode('ascii'))
            else:
                print(msg)
        except:
            print('Error in connection!')
            client.close()
            break

# Function to send a message on server
def send_message():
    while True:
        msg = f'{name}: {input("")}'
        client.send(msg.encode('ascii'))


th1 = th.Thread(target=connect_to_server)
th1.start()

th2 = th.Thread(target=send_message)
th2.start()
