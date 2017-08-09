#!/usr/bin/env python
# Python Network Programming Cookbook, Second Edition -- Chapter - 3
# This program is optimized for Python 3.5.2.
# It may run on any other version with/without modifications.
# To make it run on Python 2.7.x, needs some changes due to API differences.
# Follow the comments inline to make the program work with Python 2.


import socket
import sys

SERVER_PATH = "/tmp/python_unix_socket_server"

def run_unix_domain_socket_client():
    """ Run "a Unix domain socket client """
    sock = socket.socket(socket.AF_UNIX, socket.SOCK_DGRAM)
    
    # Connect the socket to the path where the server is listening
    server_address = SERVER_PATH 
    print ("connecting to %s" % server_address)
    try:
        sock.connect(server_address)
    except socket.error as msg:
        print (msg)
        sys.exit(1)
    
    try:
        message = "This is the message.  This will be echoed back!"
        print  ("Sending [%s]" %message)

        sock.sendall(bytes(message, 'utf-8'))
        # Comment out the above line and uncomment the below line for Python 2.7.
        # sock.sendall(message)

        amount_received = 0
        amount_expected = len(message)
        
        while amount_received < amount_expected:
            data = sock.recv(16)
            amount_received += len(data)
            print ("Received [%s]" % data)
    
    finally:
        print ("Closing client")
        sock.close()

if __name__ == '__main__':
    run_unix_domain_socket_client()
