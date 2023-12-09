# Code from https://realpython.com/python-sockets/#echo-server used

# echo-client.py

import socket
from dnslib import *

SERVER_IP = "54.225.14.129"
URL = "a.unsatisfiable.net"  # The server's hostname or IP address (will need to be domain name)
DNS_HOST = "8.8.8.8"
PORT = 53  # The port used by the server

html_data = ""

# Had to change SCOK_STREAM to SOCK_DGRAM to fix broken pipe error
with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
    while True:
        user_input = input("Please enter then data to send: ")
        query = DNSRecord.question(user_input + "." + URL, qtype = "TXT")

        #.pack to return bytes object can not send a DNSRecord
        s.sendto(query.pack(), (DNS_HOST, PORT)) # need to send the info to a DNS server for this it is google

        print(query)
        
        # Recieve DNS response from server
        data, addr = s.recvfrom(1500)
        print(f"Received data from {addr}: {data}")

        # Parse DNS response
        dns_response = DNSRecord.parse(data)
        print(f"DNS Data: {dns_response}")

        # Decode DNS response data from Base64 - bytes - string
        txt_string = base64.b64decode(dns_response.rr).decode('utf-8')

        # As long as data is not "END" request again
        if txt_string != "END":

            # Addend DNS response data to html string
            html_data += txt_string

            # Send another query for next TXT record
            s.sendto(query.pack(), (DNS_HOST, PORT))

        # If string in TXT record is "END" print the html data
        else:
            for htlm_string in html_data:
                print(htlm_string)


        if user_input == "":
            break
        

    s.close()

#print(f"Received {data!r}")

# print(subprocess.run(['lynx', '-stdin', '-dump'], input=html, capture_output=True, text=True).stdout)