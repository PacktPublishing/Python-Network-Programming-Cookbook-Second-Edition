#!/usr/bin/env python
# Python Network Programming Cookbook, Second Edition -- Chapter - 6
# This program is optimized for Python 3.5.2.
# It may run on any other version with/without modifications.
# To make it run on Python 2.7.x, needs some changes due to API differences.
# Follow the comments inline to make the program work with Python 2.


import getpass
import sys
import telnetlib

HOST = "localhost"

def run_telnet_session():

    user = input("Enter your remote account: ")
    # Comment out the above line and uncomment the below line for Python 2.7.
    # user = raw_input("Enter your remote account: ")

    password = getpass.getpass()
    
    session = telnetlib.Telnet(HOST)
    
    session.read_until(b"login: ")
    session.write(user.encode('ascii') + b"\n")
    if password:
        session.read_until(b"Password: ")
        session.write(password.encode('ascii') + b"\n")
    
    session.write(b"ls\n")
    session.write(b"exit\n")
    
    print (session.read_all())

if __name__ == '__main__':
    run_telnet_session()

