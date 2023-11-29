# Code from https://realpython.com/python-sockets/#echo-server used

# echo-server.py

import socket
from dnslib import *
import requests

HOST = "172.26.13.129"  # Standard loopback interface address (localhost)
PORT = 53  # Port to listen on (non-privileged ports are > 1023)


def get_html(url):
    r = requests.get("https://" + url)
    return r.text

with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
    s.bind((HOST, PORT))
    print(f"Connected by {HOST}, on port: {PORT}")

    subdomain_check = ""
    while True:
        
        # changed to recvfrom to get src addr
        data, addr = s.recvfrom(1024)
        #print(f"Received: {data} from {addr}")

        dns_request = DNSRecord.parse(data)

        url = str(dns_request.q.qname)

        subdomain = (url.split('.')[0]).lower()

        if subdomain != subdomain_check:
            subdomain_check = subdomain
            new_subdomain = subdomain[:3] + "." + subdomain[3:(len(subdomain)-3)] + "." + subdomain[(len(subdomain)-3):] # reinsert dots to url
            new_data = bytes(get_html(new_subdomain), 'utf-8')
        

        if not data:
            break

        answer = dns_request.reply()
        answer.add_answer(RR(url,QTYPE.TXT,rdata=TXT(new_data),ttl=60))
        # Not send all just send back same request
        s.sendto(answer, addr)

# Need to work with DNS
# dnslib? dnspython?
#172-26-13-129


# Running terminal commands: https://stackoverflow.com/questions/3730964/python-script-execute-commands-in-terminal
# Preview HTML in Terminal: https://askubuntu.com/questions/58416/how-can-i-preview-html-documents-from-the-command-line