#!/user/bin/env python3

import socket
import os

host = 'localhost'
portSender = 3333
portReceiver = 4444

# Connect to server
sender = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sender.connect((host, portSender))
print("Sender connected to port ", portSender)

# Read file
filename = "Queue.java"
file = open(filename, 'rb')
file_data = file.read()
print("File named ", filename, " has opened")

# Send file
sentData = sender.send(file_data)
if sentData == os.stat(filename).st_size:
    print("Successfully sent all data")
else:
    print(os.stat(filename).st_size - sentData, " bytes could not sent")

receiver = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
receiver.connect((host, portReceiver))
print("Receiver connected to port ", portReceiver)

# Receive and write file
# Different version to check new file
filename = "Queue2.java"
file = open(filename, 'wb+')

# Receive file
receivedData = receiver.recv(2048)
file = file.write(receivedData)
print("Successfully created received data")

sender.close()
receiver.close()

