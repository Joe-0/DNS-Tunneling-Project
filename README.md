# CS330 Final Project, Joe Stearns, 2023
**This code requires [Lynx](https://github.com/ThomasDickey/lynx-snapshots) and [dnslib](https://pypi.org/project/dnslib/) to run

## queue_server.py
**This is the final version of server code**

- This code simply runs on an AWS instance where a subdomain is pointed at. If the AWS node's IP changes the HOST constant will need to change as well

- The socket code was adapted from [Real Python's Guide](https://realpython.com/python-sockets/#echo-server)
- Code to split a string of HTML data into groups was adapted from [HERE](https://stackoverflow.com/questions/43982938/split-string-into-groups-of-3-characters)

## queue_client.py
**This is the final version of client code**

- It is important to note when using this code you cannot include "." in the website you want. E.g. wwwexamplecom for www.example.com

- The socket code was adapted from [Real Python's Guide](https://realpython.com/python-sockets/#echo-client)
- Code for running terminal commands in Python adapted from [HERE](https://stackoverflow.com/questions/3730964/python-script-execute-commands-in-terminal)
- Code for previewing HTML in terminal adapted from [HERE](https://askubuntu.com/questions/58416/how-can-i-preview-html-documents-from-the-command-line)
