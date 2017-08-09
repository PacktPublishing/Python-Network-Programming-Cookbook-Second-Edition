#!/usr/bin/env python
# Python Network Programming Cookbook, Second Edition -- Chapter - 11
# This program is optimized for Python 2.7.12.
# It may run on any other version with/without modifications.

import argparse
import requests
from throttler.base_throttler import BaseThrottler


def main(address):

    # Throttle the requests with the BaseThrottler, delaying 1.5s.
    bt = BaseThrottler(name='base-throttler', delay=1.5)

    # Visit the address provided by the user. Complete URL only.
    r = requests.Request(method='GET', url=address)

    # 10 requests.
    reqs = [r for i in range(0, 10)]

    # Submit the requests with the required throttling.
    with bt:
        throttled_requests = bt.submit(reqs)

    # Print the response for each of the requests.
    for r in throttled_requests:
        print (r.response)

    # Final status of the requests.
    print ("Success: {s}, Failures: {f}".format(s=bt.successes, f=bt.failures))


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Requests Throttling')
    parser.add_argument('--address', action="store", dest="address",  default='http://www.google.com')
    given_args = parser.parse_args() 
    address = given_args.address
    main (address)

