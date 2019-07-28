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
sequence_A = 0
expected_A = 0

start_time = time.time()
while count_sent < package_count:
        file_data = file.read(package_size)
        package_A = tcppacket.TCPPacket(3333,sequence_A,expected_A)
        packet_A = package_A.create_packet(file_data)
        sent_data = sender.send(packet_A)
        # Get response
        response = sender.recv(10)
        opened = package_A.open_packet(response)
        expected_A = opened[0][2] - 1
        # if package is successfully sent
        if expected_A == sequence_A:
            total_sent += sent_data
            count_sent += 1
            # Set sequence to ack received
            sequence_A = opened[0][2]
        # else resend it one more
        else:
            sender.send(packet_A)
            
print("Ended in ", time.time()-start_time," seconds")

# Notify server with "fin" message
package_end = tcppacket.TCPPacket(3333,sequence_A,expected_A)
packet_end = package_end.create_packet(b"closethestream")
sender.send(packet_end)

filename = "Chapter_6_V6.1.ppt"
file = open(filename, 'wb+')

total_received = b""
sequence_B = 0
expected_B = 0
start_time = time.time()

while True:
      received_data = receiver.recv(package_size+10)
      package_next_B = tcppacket.TCPPacket(4444,sequence_B,expected_B+1)
      package_resend_B = tcppacket.TCPPacket(4444,sequence_B,expected_B)
      header = package_next_B.open_packet(received_data)
      if header[1]==b"closethestream":
            break
      sequence_B = header[0][1]
            # if received successfully
      print(sequence_B," ",expected_B)
      if sequence_B == expected_B :
            total_received += header[1]
            # Send ack
            packet_B = package_next_B.create_packet(b"")
            receiver.send(packet_B)
            expected_B += 1
      else:
            packet_B = package_resend_B.create_packet(b"")
            receiver.send(packet_B)
            
file = file.write(total_received)

elapsed = time.time() - start_time   
if total_sent == os.stat(filename).st_size:
     after_time = time.time()
     print("Successfully sent all data in ",elapsed," seconds")
else:
    print("Process ended in ",elapsed," seconds")
    print(total_sent - sent_data, " bytes could not sent")

sender.close()
receiver.close()

