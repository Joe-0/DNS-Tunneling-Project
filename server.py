# Code from https://realpython.com/python-sockets/#echo-server used

# echo-server.py

import socket
from dnslib import *

HOST = "172.26.13.129"  # Standard loopback interface address (localhost)
PORT = 53  # Port to listen on (non-privileged ports are > 1023)

with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
    s.bind((HOST, PORT))
    print(f"Connected by {HOST}, on port: {PORT}")

    while True:
        
        # changed to recvfrom to get src addr
        data, addr = s.recvfrom(1024)
        print(f"Received: {data} from {addr}")

        dns_request = DNSRecord.parse(data)

        print(dns_request)

        if not data:
            break

        # Not send all just send back same request
        s.sendto(data, addr)


# Need to work with DNS
# dnslib? dnspython?
#172-26-13-129