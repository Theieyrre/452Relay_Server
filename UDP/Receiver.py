from socket import *

host = "0.0.0.1"
port = 5000
s = socket(AF_INET, SOCK_DGRAM)
s.bind((host, port))

addr = (host, port)
buf = 1024

f = open("10mb3.ppt", 'wb')

data, addr = s.recvfrom(buf)
try:
    while (data):
        f.write(data)
        s.settimeout(2)
        data, addr = s.recvfrom(buf)
except timeout:
    f.close()
    s.close()
    print("File Received")