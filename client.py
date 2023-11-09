# Code from https://realpython.com/python-sockets/#echo-server used

# echo-client.py

import socket

HOST = "127.0.0.1"  # The server's hostname or IP address (will need to be domain name)
PORT = 53  # The port used by the server

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect((HOST, PORT))
    while True:
        user_input = input("Please enter then data to send")
        s.sendall(user_input.encode('uft-8') + ".domain.com")
        s.sendall(b"\n")
        if user_input == "":
            break
    data = s.recv(1024)

print(f"Received {data!r}")