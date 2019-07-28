from socket import *

host = "0.0.0.0"
port = 9999
s = socket(AF_INET, SOCK_DGRAM)
s.bind((host, port))

addr = (host, port)
buf = 1024

f = open("10mb2.ppt", 'wb')

data, addr = s.recvfrom(buf)
try:
    while (data):
        f.write(data)
        s.settimeout(2)
        data, addr = s.recvfrom(buf)
except timeout:
    f.close()
    s.close()




sB = socket(AF_INET, SOCK_DGRAM)
hostB = "0.0.0.0"
portB = 5000
bufB = 1024
addrB = (hostB, portB)

file_nameB = "10mb2.ppt"

fB = open(file_nameB, "rb")
dataB = fB.read(bufB)

sB.sendto(file_nameB.encode(), addrB)
sB.sendto(dataB, addrB)
while (dataB):
    if (sB.sendto(dataB, addrB)):
        print("server send to receiver...")
        dataB = fB.read(bufB)
sB.close()
fB.close()
