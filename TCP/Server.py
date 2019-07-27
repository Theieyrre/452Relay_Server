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
print("Waiting for packages for A")
socket_for_a.listen(1)

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


# Receive data from A and send data to B
total_sent = b""
total_received = b""
sequence_A = 0
sequence_B = 0
expected_A = 0
expected_B = 0
while True:
    # Header size is 10 bytes
    data = connectionA.recv(package_size+10)
    package_next_A = tcppacket.TCPPacket(3333,sequence_A,expected_A+1)
    package_next_B = tcppacket.TCPPacket(4444,sequence_B, expected_B+1)
    package_resend_A = tcppacket.TCPPacket(3333,sequence_A, expected_A)
    package_resend_B = tcppacket.TCPPacket(4444,sequence_B, expected_B)
    header = package_next_A.open_packet(data)
    # Second index of tuple is sequence number
    sequence_A = header[0][1]
    # Received from A true
    if sequence_A == expected_A:
        print("received from a")
        total_received += header[1]
        packet_B = package_next_B.create_packet(header[1])
        connectionB.send(packet_B)
        # Get response
        response = connectionB.recv(10)
        opened = package_next_B.open_package(response)
        sequence_B == opened[0][1]
        # Sent to B true
        if sequence_B == expected_B:
            print("sent to b")
            total_sent += opened[1]
            packet_B = package_next_B.create_packet(b"")
            connectionB.send(packet_B)
        # Sent to B false
        else:
            print("resend to b")
            packet_B = package_resend_B.create_packet(header[1])
            connectionB.send(packet_B)
        packet_A = package_next_A.create_packet(b"")
        connectionA.send(packet)
        last_ack += 1
    # Received from A false
    else:
        print("resend to a")
        packet = package_resend_A.create_packet(b"")
        connectionA.send(packet)
    if total_sent == total_received:
        print("All data sent successfully")
        break
