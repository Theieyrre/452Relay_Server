import socket
import time
import sys

UDP_IP = "127.0.0.1"
UDP_PORT = 5005
buf = 1024
file_name = "deneme.txt"

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.sendto(file_name.encode(), (UDP_IP, UDP_PORT))
print("Sending %s ..." % file_name)

file = open(file_name, "r")
data = file.read(buf)
while (data):
    if (sock.sendto(data.encode(), (UDP_IP, UDP_PORT))):
        data = file.read(buf)
        time.sleep(0.02)  # Give receiver a bit time to save

sock.close()
file.close()
