#!/usr/bin/env python
# Python Network Programming Cookbook, Second Edition -- Chapter - 14
# This program is optimized for Python 2.7.12 and Python 3.5.2.
# It may run on any other version with/without modifications.
 
import socket
from sys import stdout
from time import sleep
import argparse
 
def is_alive(address, port):
    # Create a socket object to connect with
    s = socket.socket()
    
    # Now try connecting, passing in a tuple with address & port
    try:
        s.connect((address, port))
        return True
    except socket.error:
        return False
    finally:
        s.close()
 

def confirm(addres, port):
    while True:
        if is_alive(address, port):
            stdout.write(address + ":" + str(port) + ' is alive\n')
            stdout.flush()
        else:
            stdout.write(address + ":" + str(port) + ' is dead\n')
            stdout.flush()
        sleep(10)


if __name__ == '__main__':
    # setup commandline arguments
    parser = argparse.ArgumentParser(description='Health Checker')
    parser.add_argument('--address', action="store", dest="address")
    parser.add_argument('--port', action="store", dest="port", default=80, type=int)
    # parse arguments
    given_args = parser.parse_args()
    address, port =  given_args.address, given_args.port
    confirm(address, port)


