#!/usr/bin/env python
# Python Network Programming Cookbook, Second Edition -- Chapter - 3
# This program is optimized for Python 3.5.2.
# It may run on any other version with/without modifications.

import argparse
import time
import datetime

import tornado.httpserver
import tornado.ioloop
import tornado.options
import tornado.web

from tornado import gen
from tornado.concurrent import return_future

class AsyncUser(object):
    @return_future
    def req1(self, callback=None):
        time.sleep(0.1)
        result = datetime.datetime.utcnow()
        callback(result)

    @return_future
    def req2(self, callback=None):
        time.sleep(0.2)
        result = datetime.datetime.utcnow()
        callback(result)



class Application(tornado.web.Application):
    def __init__(self):
        handlers = [
            (r"/", UserHandler),
        ]
        tornado.web.Application.__init__(self, handlers)


class UserHandler(tornado.web.RequestHandler):
    @gen.coroutine
    def get(self):
        user = AsyncUser()
        response1 = yield (user.req1())
        response2 = yield (user.req2())
        print ("response1,2: %s %s" %(response1, response2))
        self.finish()

def main(port):
    http_server = tornado.httpserver.HTTPServer(Application())
    print("Server listening at Port: ", port)
    http_server.listen(port)
    tornado.ioloop.IOLoop.instance().start()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Async Server Example')
    parser.add_argument('--port', action="store", dest="port", type=int, required=True)
    given_args = parser.parse_args() 
    port = given_args.port
    main(port)
