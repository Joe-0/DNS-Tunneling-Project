# Code from https://realpython.com/python-sockets/#echo-server used

# echo-client.py

import socket
from dnslib import *

SERVER_IP = "54.225.14.129"
URL = "a.unsatisfiable.net"  # The server's hostname or IP address (will need to be domain name)
DNS_HOST = "8.8.8.8"
PORT = 53  # The port used by the server

# Had to change SCOK_STREAM to SOCK_DGRAM to fix broken pipe error
with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
    while True:
        user_input = input("Please enter then data to send: ")
        query = DNSRecord.question(user_input + "." + URL, qtype = "TXT")

        #.pack to return bytes object can not send a DNSRecord
        s.sendto(query.pack(), (DNS_HOST, PORT)) # need to send the info to a DNS server for this it is google

        print(query)
        
        # Should be same as what was sent
        data, addr = s.recvfrom(1024)
        print(f"Received data from {addr}: {data}")

        dns_response = DNSRecord.parse(data)
        print(f"DNS Data: {dns_response}")


        if user_input == "":
            break
        

    s.close()

#print(f"Received {data!r}")

# print(subprocess.run(['lynx', '-stdin', '-dump'], input=html, capture_output=True, text=True).stdout)