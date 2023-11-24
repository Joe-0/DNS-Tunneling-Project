# Code from https://realpython.com/python-sockets/#echo-server used

# echo-server.py

import socket
from dnslib import *

HOST = "0.0.0.0"  # Standard loopback interface address (localhost)
PORT = 53  # Port to listen on (non-privileged ports are > 1023)

with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
    s.bind((HOST, PORT))
    #s.listen()
    #conn, addr = s.accept()
    print(f"Connected by {HOST}, on port: {PORT}")
    while True:
        data = s.recv(1024)

        dns_response = DNSRecord.parse(data)

        print(dns_response)

        if not data:
            break
        print(data)
        s.sendall(data)


# Need to work with DNS
# dnslib? dnspython?
