# Code from https://realpython.com/python-sockets/#echo-server used

# echo-server.py

import socket

HOST = "172.26.13.129"  # Standard loopback interface address (localhost)
PORT = 65432  # Port to listen on (non-privileged ports are > 1023)

with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
    s.bind((HOST, PORT))
    print(f"Connected by {HOST}, on port: {PORT}")

    while True:
        data, addr = s.recvfrom(1024)

        msg = bytes("Hello, Client", 'utf-8')

        s.sendto(msg, addr)

        print(f"Received and sent data from {addr}: {msg.decode('utf-8')}")
