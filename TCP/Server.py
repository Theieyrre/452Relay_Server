#!/usr/bin/env python3

import socket
import os

host = "localhost"
portA = 3333
portB = 4444
# Total size of the file in bytes
total_size = 12177920

socket_for_a = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# Try to bind socket_for_a
try:
    socket_for_a.bind((host, portA))
except socket.error as message:
    print("Bind failed with error ", message[1])

# Set maximum client for this socket
socket_for_a.listen(1)

# Bind to socket_for_b
socket_for_b = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
try:
    socket_for_b.bind((host, portB))
except socket.error as message:
    print("Bind faile with error ", message[1]) 

# Set maximum client for this socket wait for data
socket_for_b.listen(1)
connectionB, addressB = socket_for_b.accept()
print("Connected with ", portB)
connectionA, addressA = socket_for_a.accept()
print("Connected with ", portA)

# Receive data from A and send data to B
total_sent = 0
total_received = 0
while True:
    data = connectionA.recv(2048)
    total_sent += data
    data_sent = connectionB.send(data)
    # Basic control to change later
    if len(data) == data_sent:
        print("Data sent successfully")
        total_received += data_sent
    else:
        print("Couldn't send data")
    if total_sent == total_size:     
        print("All data sent")
        break
    
if total_sent == total_received:
    print("All data sent successfully")
else:
    print(total_sent - total_received , " bytes are failed to sent")
