#!/usr/bin/env python
# Python Network Programming Cookbook, Second Edition -- Chapter - 1
# This program is optimized for Python 2.7.12 and Python 3.5.2.
# It may run on any other version with/without modifications.

import socket


def print_machine_info():
    host_name = socket.gethostname()
    ip_address = socket.gethostbyname(host_name)
    print ("Host name: %s" %host_name)
    print ("IP address: %s" %ip_address)

if __name__ == '__main__':
    print_machine_info()
