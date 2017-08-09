#!/usr/bin/env python
# Python Network Programming Cookbook, Second Edition -- Chapter - 7
# This program is optimized for Python 2.7.12.
# Supervisor requires Python 2.x, and does not run on Python 3.x.


import supervisor.xmlrpc
import xmlrpclib

def query_supervisr(sock):
    transport = supervisor.xmlrpc.SupervisorTransport(None, None,
                'unix://%s' %sock)
    proxy = xmlrpclib.ServerProxy('http://127.0.0.1',
            transport=transport)
    print ("Getting info about all running processes via Supervisord...")
    print (proxy.supervisor.getAllProcessInfo())

if __name__ == '__main__':
    query_supervisr(sock='/tmp/supervisor.sock')
    

