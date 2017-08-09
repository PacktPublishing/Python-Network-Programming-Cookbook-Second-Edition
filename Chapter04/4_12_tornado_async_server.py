#!/usr/bin/env python
# Python Network Programming Cookbook, Second Edition -- Chapter - 3
# This program is optimized for Python 2.7.12 and Python 3.5.2.
# It may run on any other version with/without modifications.

import argparse
import tornado.ioloop
import tornado.httpclient


class TornadoAsync():
    def handle_request(self,response):
        if response.error:
            print ("Error:", response.error)
        else:
            print (response.body)
        tornado.ioloop.IOLoop.instance().stop()

def run_server(url):
    tornadoAsync = TornadoAsync()
    http_client = tornado.httpclient.AsyncHTTPClient()
    http_client.fetch(url, tornadoAsync.handle_request)
    tornado.ioloop.IOLoop.instance().start()

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Async Server Example')
    parser.add_argument('--url', action="store", dest="url", type=str, required=True)
    given_args = parser.parse_args() 
    url = given_args.url
    run_server(url)
