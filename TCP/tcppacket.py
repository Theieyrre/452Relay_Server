#!/user/bin/env python3

import socket
# For checksum
import hashlib
import struct

class TCPPacket:
    def __init__(self, port_src, sequence, ack):
        checksum = hashlib.sha3_256()
        host = 'localhost'
        self.port_src = port_src
        self.seq = sequence
        self.ack = ack

    def create_packet(self,data):
        # Create struct from int to binary
        # H is unsigned short with size 2
        # L is unsigned long with size 4
        header = struct.pack("!HLL",self.port_src,self.seq,self.ack)
        return header+data
    
    def open_packet(self,packet):
        # Only unpack 10 bytes
        header = struct.unpack_from("!HLL",packet[0:10])
        # Remainder is already in bytes
        data = packet[10:]
        # return tuple
        return header, data;

