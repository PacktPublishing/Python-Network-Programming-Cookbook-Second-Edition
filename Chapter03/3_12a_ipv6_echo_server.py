#!/usr/bin/env python
# Python Network Programming Cookbook, Second Edition -- Chapter - 3
# This program is optimized for Python 2.7.12 and Python 3.5.2.
# It may run on any other version with/without modifications.

import argparse 
import socket
import sys

HOST = 'localhost'

def echo_server(port, host=HOST):
    """Echo server using IPv6 """
    for result in socket.getaddrinfo(host, port, socket.AF_UNSPEC, socket.SOCK_STREAM, 0, socket.AI_PASSIVE):
        af, socktype, proto, canonname, sa = result
        try:
            sock = socket.socket(af, socktype, proto)
        except socket.error as err:
            print ("Error: %s" %err)
        
        try:
            sock.bind(sa)
            sock.listen(1)
            print ("Server lisenting on %s:%s" %(host, port))
        except socket.error as msg:
            sock.close()
            continue
        break
        sys.exit(1)
    conn, addr = sock.accept()
    print ('Connected to', addr)
    while True:
        data = conn.recv(1024)
        print ("Received data from the client: [%s]" %data)
        if not data: break
        conn.send(data)
        print ("Sent data echoed back to the client: [%s]" %data)
    conn.close()

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='IPv6 Socket Server Example')
    parser.add_argument('--port', action="store", dest="port", type=int, required=True)
    given_args = parser.parse_args() 
    port = given_args.port
    echo_server(port)
    
