#!/usr/bin/env python
# Python Network Programming Cookbook, Second Edition -- Chapter - 2
# This program is optimized for Python 2.7.12.
# It will work with Python 3.5.2 once the depedencies for diesel are sorted out.
# It may run on any other version with/without modifications.
# You also need diesel library 3.0 or a later version.
# Make sure to install the dependencies beforehand.

import diesel
import argparse

class EchoServer(object):
    """ An echo server using diesel"""

    def handler(self, remote_addr):
        """Runs the echo server"""
        host, port = remote_addr[0], remote_addr[1]
        print ("Echo client connected from: %s:%d" %(host, port))
        
        while True:
            try:
                message = diesel.until_eol()
                your_message = ': '.join(['You said', message])
                diesel.send(your_message)
            except Exception as e:
                print ("Exception:",e)
                

def main(server_port):
    app = diesel.Application()
    server = EchoServer()    
    app.add_service(diesel.Service(server.handler, server_port))
    app.run()


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Echo server example with Diesel')
    parser.add_argument('--port', action="store", dest="port", type=int, required=True)
    given_args = parser.parse_args() 
    port = given_args.port
    main(port)


