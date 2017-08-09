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
from base64 import b64decode

from xmlrpc.server import SimpleXMLRPCServer, SimpleXMLRPCRequestHandler
# Comment out the above line and uncomment the below line for Python 2.x.
#from SimpleXMLRPCServer  import SimpleXMLRPCServer, SimpleXMLRPCRequestHandler


class SecureXMLRPCServer(SimpleXMLRPCServer):

    def __init__(self, host, port, username, password, *args, **kargs):
        self.username = username
        self.password = password
        # authenticate method is called from inner class
        class VerifyingRequestHandler(SimpleXMLRPCRequestHandler):
              # method to override
              def parse_request(request):
                  if SimpleXMLRPCRequestHandler.parse_request(request):
                      # authenticate
                      if self.authenticate(request.headers):
                          return True
                      else:
                          # if authentication fails return 401
                          request.send_error(401, 'Authentication failed, Try agin.')
                  return False
        # initialize
        SimpleXMLRPCServer.__init__(self, (host, port), requestHandler=VerifyingRequestHandler, *args, **kargs)

    def authenticate(self, headers):
        headers = headers.get('Authorization').split()
        basic, encoded = headers[0], headers[1]
        if basic != 'Basic':
            print ('Only basic authentication supported')
            return False
        secret = b64decode(encoded).split(b':')
        
        username, password = secret[0].decode("utf-8"), secret[1].decode("utf-8")
        return True if (username == self.username and password == self.password) else False
    

def run_server(host, port, username, password):
    server = SecureXMLRPCServer(host, port, username, password)
    # simple test function
    def echo(msg):
        """Reply client in  uppser case """
        reply = msg.upper()
        print ("Client said: %s. So we echo that in uppercase: %s" %(msg, reply))
        return reply
    server.register_function(echo, 'echo')
    print ("Running a HTTP auth enabled XMLRPC server on %s:%s..." %(host, port))
    server.serve_forever()


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
    run_server(host, port, username, password)
