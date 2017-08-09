#!/usr/bin/env python
# Python Network Programming Cookbook -- Chapter - 4
# This program requires Python 3.5.2 or any later version
# It may run on any other version with/without modifications.
#
# Follow the comments inline to make it run on Python 2.7.x.

import argparse

import http.client
# Comment out the above line and uncomment the below for Python 2.7.x.
#import httplib

import urllib.parse
# Comment out the above line and uncomment the below for Python 2.7.x.
#import urlparse

import re
import urllib.request, urllib.error
# Comment out the above line and uncomment the below for Python 2.7.x.
#import urllib

DEFAULT_URL = 'http://www.python.org'

HTTP_GOOD_CODES =  [http.client.OK, http.client.FOUND, http.client.MOVED_PERMANENTLY]
# Comment out the above line and uncomment the below for Python 2.7.x.
#HTTP_GOOD_CODES =  [httplib.OK, httplib.FOUND, httplib.MOVED_PERMANENTLY]

def get_server_status_code(url):
    """
    Download just the header of a URL and
    return the server's status code.
    """
    host, path = urllib.parse.urlparse(url)[1:3] 
    # Comment out the above line and uncomment the below for Python 2.7.x.
    #host, path = urlparse.urlparse(url)[1:3] 
    try:
        conn = http.client.HTTPConnection(host)       
        # Comment out the above line and uncomment the below for Python 2.7.x.
        #conn = httplib.HTTPConnection(host)

        conn.request('HEAD', path)
        return conn.getresponse().status

    except Exception as e:
        print ("Server: %s status is: %s " %(url, e))
        # Comment out the above line and uncomment the below for Python 2.7.x.
        #except StandardError:
        return None

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Example HEAD Request')
    parser.add_argument('--url', action="store", dest="url", default=DEFAULT_URL)
    given_args = parser.parse_args() 
    url = given_args.url
    if get_server_status_code(url) in HTTP_GOOD_CODES:
        print ("Server: %s status is OK: %s " %(url, get_server_status_code(url)))
    else:
        print ("Server: %s status is NOT OK: %s" %(url, get_server_status_code(url)))
