# Code from https://realpython.com/python-sockets/#echo-server used

# echo-client.py

import socket
from dnslib import *

#HOST = "54.225.14.129" IP of server
URL = "joe.unsatisfiable.net"  # The server's hostname or IP address (will need to be domain name)
DNS_HOST = "8.8.8.8"
PORT = 65432  # The port used by the server
#PORT = 1024


print("TEST")

'''user_input = input("Please enter then data to send: ")
query = DNSRecord.question(user_input + "." + HOST)

print(query)'''

# Had to change SCOK_STREAM to SOCK_DGRAM to fix broken pipe error
with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
    while True:
        user_input = input("Please enter then data to send: ")
        query = DNSRecord.question(user_input + "." + URL)

        print(query)
        #.pack to return bytes object can not send a DNSRecord
        s.sendto(query.pack(), (DNS_HOST, PORT)) # need to send the info to a DNS server for this it is google
        #s.sendall(b"\n")
        #print("HERE")
        #user_input = input("Please enter then data to send: ")
        #query = DNSRecord.question(user_input + "." + HOST)
        #print(query)
        #s.sendall(user_input.encode('uft-8') + "." + HOST)
        #s.sendall(b"\n")
        if user_input == "":
            break
        data = s.recv(1024)

    s.close()

print(f"Received {data!r}")