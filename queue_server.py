# queue_server.py
# Author: Joe Stearns
# Date: Dec, 2023
#
# Code used for DNS tunneling, will get HTML data from page and send back to client
#

import socket
from dnslib import *
import requests

HOST = "172.26.13.129"  # IP for AWS instance
PORT = 53  # Port to listen on

# Get HTML test of page
def get_html(subdomain):
    """
    Get the HTML code of a given website

    Args:
        subdomain: The name of the website to get (eg "google")
    
    Returns:
        r.text: A string of the HTML code of website
    """
    # Reinsert dots to url to get HTML data
    url = subdomain[:3] + "." + subdomain[3:(len(subdomain)-3)] + "." + subdomain[(len(subdomain)-3):]
    print(f"New_sub: {url}")

    # Get HTML data
    r = requests.get("https://" + url)
    return r.text

client_dic = {}

with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
    s.bind((HOST, PORT))
    print(f"Connected by {HOST}, on port: {PORT}")

    while True:

        # Get subdomain from DNS request
        data, addr = s.recvfrom(1024)
        dns_request = DNSRecord.parse(data)
        url = str(dns_request.q.qname)
        dns_subdomain = (url.split('.')[0]).lower()

        # If first time request create new elm in dic
        if dns_subdomain not in client_dic:
            client_dic[dns_subdomain] = {"index": 0, "data": []}

            html_data = get_html(dns_subdomain)

            # Split HTML data into strings of length 150
            # 150 to account for space when encoding
            grouped_data = [html_data[i:i+150] for i in range(0, len(html_data), 150)]
            print(f"Grouped_data: {grouped_data}")

            # Access subdomain elm in dic
            current_subdomain = client_dic[dns_subdomain]

            # Encode the strings with Base64 and add to data list for subdomain elm in dic
            for group in grouped_data:
                current_subdomain["data"].append(base64.b64encode(bytes(group, "utf-8")))

        # Access subdomain elm in dic
        current_subdomain = client_dic[dns_subdomain]

        # Check if not at end of subdomain data list, use index key to index into data list
        if current_subdomain["index"] < len(current_subdomain["data"]):

            # Auto create empty reply response
            dns_answer = dns_request.reply()
            
            # Index into subdomain data list to grab right string
            group_to_send = current_subdomain["data"][current_subdomain["index"]]

            # Add TXT record to reply response
            dns_answer.add_answer(RR(url, QTYPE.TXT, rdata=TXT(group_to_send), ttl = 0))

            print(f"answer: {dns_answer}")
            print(f"addr: {addr}")

            # Send packed reply response
            s.sendto(dns_answer.pack(), addr)
            print("Sent")

            # Advance subdomain index for next go around
            current_subdomain["index"] = current_subdomain["index"] + 1
        
        # If at end of subdomain data list
        else:

             # Auto create empty reply response
            dns_answer = dns_request.reply()

            # Send "END" for client to stop sending requests
            dns_answer.add_answer(RR(url, QTYPE.TXT, rdata=TXT(base64.b64encode(bytes("END", "utf-8"))), ttl = 0))

            # Send packed reply response
            s.sendto(dns_answer.pack(), addr)
            print("Sent END reply")
