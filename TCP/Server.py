#!/usr/bin/env python3

import socket
import os

host = "localhost"
portA = 3333
portB = 4444

socket_for_a = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# Try to bind socket_for_a
try:
    socket_for_a.bind((host, portA))
except socket.error as message:
    print("Bind failed with error ", message[1])

# Set maximum client for this socket
socket_for_a.listen(1)

# Wait for data
connectionA, addressA = socket_for_a.accept()
print("Connected with ", portA)

# Receive data from A
data = connectionA.recv(2048)

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

# Send data to B
data_sent = connectionB.send(data)
if len(data) == data_sent:
    print("All data sent successfully")
else:
    print(os.stat(data).st_size - os.stat(data_sent).st_size, " bytes are failed to sent")
