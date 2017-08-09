#!/usr/bin/env python
# Python Network Programming Cookbook, Second Edition -- Chapter - 7
# This program is optimized for Python 3.5.2.
# To make it work with Python 2.7.12:
#      Follow through the code inline for some changes.
# It may run on any other version with/without modifications.


import argparse
import xmlrpc
# Comment out the above line and uncomment the below line for Python 2.x.
#import xmlrpclib

from xmlrpc.server import SimpleXMLRPCServer
# Comment out the above line for Python 2.x.

def run_client(host, port, username, password):
    server = xmlrpc.client.ServerProxy('http://%s:%s@%s:%s' %(username, password, host, port, ))
    # Comment out the above line and uncomment the below line for Python 2.x.
    #server = xmlrpclib.ServerProxy('http://%s:%s@%s:%s' %(username, password, host, port, ))
    msg = "hello server..."
    print ("Sending message to server: %s  " %msg)
    print ("Got reply: %s" %server.echo(msg))

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Multithreaded multicall XMLRPC Server/Proxy')
    parser.add_argument('--host', action="store", dest="host", default='localhost')
    parser.add_argument('--port', action="store", dest="port", default=8000, type=int)
    parser.add_argument('--username', action="store", dest="username", default='user')
    parser.add_argument('--password', action="store", dest="password", default='pass')
    # parse arguments
    given_args = parser.parse_args()
    host, port =  given_args.host, given_args.port
    username, password = given_args.username, given_args.password
    run_client(host, port, username, password)
