#!/user/bin/env python3

import socket
# For package size
import os
# For package count
import math

host = 'localhost'
portSender = 3333
portReceiver = 4444
# Send 2KB each time
package_size = 2048

# Connect to server
sender = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sender.connect((host, portSender))
print("Sender connected to port ", portSender)

# Read file
filename = "Chapter_6_V6.0.ppt"
file = open(filename, 'rb')
print("File named ", filename, " has opened")

# Send file

package_count = math.ceil(os.stat(filename).st_size / package_size)
print("Package count ",package_count)

count_sent = 0
total_sent = 0

while count_sent < package_count:
    file_data = file.read(package_size)
    sent_data = sender.send(file_data)
    # sent_data is the size of the data sent
    total_sent += sent_data
    print("total_sent ",total_sent)
    count_sent += 1
    
if total_sent == os.stat(filename).st_size:
    print("Successfully sent all data")
else:
    print(os.stat(filename).st_size - sentData, " bytes could not sent")

receiver = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
receiver.connect((host, portReceiver))
print("Receiver connected to port ", portReceiver)

# Receive and write file
# Different version to check new file
filename = "Chapter_6_V6.1.ppt"
file = open(filename, 'wb+')

# Receive file

count_received = 0
total_received = 0
while count_received < count_sent:
    received_data = receiver.recv(2048)
    total_received += received_data
    
file = file.write(receivedData)
print("Successfully created received data")

sender.close()
receiver.close()

