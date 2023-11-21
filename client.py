# Code from https://realpython.com/python-sockets/#echo-server used

# echo-client.py

import socket
from dnslib import *

#HOST = "54.225.14.129" IP of server
HOST = "joe.unsatisfiable.net"  # The server's hostname or IP address (will need to be domain name)
#HOST = "8.8.8.8"
PORT = 53  # The port used by the server
#PORT = 1024


print("TEST")

user_input = input("Please enter then data to send: ")
query = DNSRecord.question(user_input + "." + HOST)
print(query)


'''with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect((HOST, PORT))
    while True:
        print("HERE")
        user_input = input("Please enter then data to send: ")
        query = DNSRecord.question(user_input + "." + HOST)
        print(query)
        #s.sendall(user_input.encode('uft-8') + "." + HOST)
        s.sendall(b"\n")
        if user_input == "":
            break
    data = s.recv(1024)'''

#print(f"Received {data!r}")