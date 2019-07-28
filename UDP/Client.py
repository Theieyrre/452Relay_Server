from socket import *

s = socket(AF_INET, SOCK_DGRAM)
host = "0.0.0.0"
port = 9999
buf = 1024
addr = (host, port)

file_name = "10mb.ppt"

f = open(file_name, "rb")
data = f.read(buf)

s.sendto(file_name.encode(), addr)
s.sendto(data, addr)
while (data):
    if (s.sendto(data, addr)):
        print("client send to server...")
        data = f.read(buf)
s.close()
f.close()
