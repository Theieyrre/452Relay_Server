#!/usr/bin/env python3

import socket

import tcppacket

host = "localhost"
portA = 3333
portB = 4444
# Receive and send 2KB
package_size = 2048
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
print("Waiting for packages for A")

# Bind to socket_for_b
socket_for_b = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
try:
    socket_for_b.bind((host, portB))
except socket.error as message:
    print("Bind faile with error ", message[1]) 

# Set maximum client for this socket wait for data
socket_for_b.listen(1)
print("Waiting for packages for B")

connectionA, addressA = socket_for_a.accept()
print("Connected with ", portA)
connectionB, addressB = socket_for_b.accept()
print("Connected with ", portB)


# Receive data from A
total_received = b""
sequence_A = 0
expected_A = 0

while True:
    # Header size is 10 bytes
    data = connectionA.recv(package_size+10)
    package_next_A = tcppacket.TCPPacket(3333,sequence_A,expected_A+1)    
    package_resend_A = tcppacket.TCPPacket(3333,sequence_A, expected_A)   
    header = package_next_A.open_packet(data)
    if header[1] == b"closethestream":
        break
    print(header[0])
    # Second index of tuple is sequence number
    sequence_A = header[0][1]
    # Received from A true
    if sequence_A == expected_A:
        total_received += header[1]
        # Send ack
        packet_A = package_next_A.create_packet(b"")
        connectionA.send(packet_A)
        expected_A += 1
        
    # Received from A false
    else:
        packet = package_resend_A.create_packet(b"")
        connectionA.send(packet)

# Send data to B
count_sent = 0
total_sent = 0
sequence_B = 0
expected_B = 0
index = 0
package_count = len(total_received) / package_size

while count_sent < package_count:
    package_B = tcppacket.TCPPacket(4444,sequence_B, expected_B)
    data_to_send = total_received[index:package_size+index]
    packet_B = package_B.create_packet(data_to_send)
    sent_data = connectionB.send(packet_B)
    index += 1
    # Get response
    response = connectionB.recv(10)
    opened = package_B.open_packet(response)
    expected_B == opened[0][2] -1
    print(expected_B," ",sequence_B)
    # Sent to B true
    if expected_B == sequence_B:
        total_sent += sent_data
        count_sent += 1
        sequence_A = opened[0][2]
    # Sent to B false
    else:
         connectionB.send(packet_B)

package_end = tcppacket.TCPPacket(3333,sequence_B,expected_B)
packet_end = package_end.create_packet(b"closethestream")
connectionB.send(packet_end)         

