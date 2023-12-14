# queue_client.py
# Author: Joe Stearns
# Date: Dec, 2023
#
# Code used for DNS tunneling, will send dns requests to server and display HTML data
#

import socket
from dnslib import *
import subprocess

URL = "a.unsatisfiable.net"  # The server's hostname
DNS_HOST = "8.8.8.8" # Google DNS address
PORT = 53  # Privileged port for DNS requests

# List to store HTML data
html_data = []

def get_unique(lst):
    """
    Get the unique values from a given list in order

    Args:
        lst: A list of values
    
    Returns:
        return_list: A list of all unique values in lst
    """
    return_list = []
    for elm in lst:
        if elm not in return_list:
            return_list.append(elm)
    return return_list

# Had to change SCOK_STREAM to SOCK_DGRAM to fix broken pipe error
with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:

    # Prompt user to input website
    user_input = input("Please enter the website to request (Do not include \".\" e.g. wwwgooglecom): ")
    while True:
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

        print(f"dns_response.rr: {dns_response.rr}")

        # Decode DNS response data from Base64 - bytes - string
        for rr in dns_response.rr:
            txt_string = (base64.b64decode(rr.rdata.data[0])).decode('utf-8')

        # As long as data is not "END" request again
        if txt_string != "END":

            # Append DNS response data to html string
            html_data.append(txt_string)

        # If string in TXT record is "END" stop loop
        else:
            break

    # Get all the unique strings in list
    unique_html_data_list = get_unique(html_data)

    # Combine HTML list into one string
    unique_html_data_string = ''.join(unique_html_data_list)

    # Show the HTML code in terminal using lynx
    print(subprocess.run(['lynx', '-stdin', '-dump'], input=unique_html_data_string, capture_output=True, text=True).stdout)