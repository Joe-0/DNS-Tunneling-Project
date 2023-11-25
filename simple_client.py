# Code from https://realpython.com/python-sockets/#echo-client used

# echo-client.py

import socket

HOST = "54.225.14.129"  # The server's hostname or IP address
PORT = 65432  # The port used by the server

with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
    msg = (b"Hello, world")

    s.sendto(msg, (HOST, PORT))

    data, addr = s.recvfrom(1024)

print(f"Received {data.decode('utf-8')} from {addr}")
