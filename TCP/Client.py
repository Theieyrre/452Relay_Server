#!/user/bin/env python3

import socket
# For package count
import math
# For checksum
import hashlib
# For exception handling
import sys
# For file size
import os
# For elapsed time
import time

import tcppacket

host = 'localhost'
portSender = 3333
portReceiver = 4444
# Send 2KB each time
package_size = 2048
# Total size of the file in bytes
total_size = 12177920
checksum = hashlib.sha3_256()

# Connect to server
sender = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sender.connect((host, portSender))
print("Sender connected to port ", portSender)

receiver = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
receiver.connect((host, portReceiver))
print("Receiver connected to port ", portReceiver)

# Read file
filename = "Chapter_6_V6.0.ppt"
file = open(filename, 'rb')
print("File named ", filename, " has opened")

# Send file

package_count = math.ceil(total_size / package_size)
print("Package count ",package_count)

count_sent = 0
total_sent = 0
sequence = 0
expected = 0
start_time = time.time()
while count_sent < package_count:
    try:
        file_data = file.read(package_size)
        package = tcppacket.TCPPacket(3333,sequence,expected)
        packet = package.create_packet(file_data)
        sent_data = sender.send(packet)
        # Get response
        response = sender.recv(10)
        opened = package.open_packet(response)
        expected = opened[0][1]
        # if package is successfully sent
        if expected == sequence:
            print(sequence, " sent successfully")
            total_sent += sent_data
            count_sent += 1
            # Set sequence to ack received
            sequence = opened[0][2]
        # else resend it one more
        else:
            print("resend")
            sender.send(packet)
    except:
       print(sys.exc_info()[1])
       
elapsed = time.time() - start_time   
if total_sent == os.stat(filename).st_size:
    after_time = time.time()
    print("Successfully sent all data in ",elapsed," seconds")
else:
    print("Process ended in ",elapsed," seconds")
    print(total_sent - sent_data, " bytes could not sent")


# Different version to check new file
filename = "Chapter_6_V6.1.ppt"
file = open(filename, 'wb+')

# Receive file
count_received = 0
total_received = 0
sequence = 0
expected = 0
start_time = time.time()
while count_received < count_sent:
    package = tcppacket.TCPPacket(4444,sequence,expected)
    received_data = receiver.recv(package_size+10)
    header = package.open_package(received_data)
    print(header)
    if expected == header[0][1]:
        total_received += header[1]
        # increasing by one insted of the size
        expected += 1
        sequence = header[0][1]
        package_next = tcppacket.TCPPacket(4444,sequence,expected)
        packet = package_next.create_packet(b"")
        receiver.send(packet)
    else:
        packet = package.create_packet(b"")
        receiver.send(packet)
    
file = file.write(receivedData)
print("Successfully created received data")

sender.close()
receiver.close()

