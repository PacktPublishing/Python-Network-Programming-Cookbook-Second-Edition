#!/usr/bin/env python
# Python Network Programming Cookbook, Second Edition -- Chapter - 11
# This program is optimized for Python 2.7.12 and Python 3.5.2.
# It may run on any other version with/without modifications.

import argparse
import ntplib
from time import ctime


def main(address, v):
    c = ntplib.NTPClient()
    response = c.request(address, version=v)
    print("Response Offset: ", response.offset)
    print("Version: ", response.version)
    print("Response (Time): ", ctime(response.tx_time))
    print("Leap: ", ntplib.leap_to_text(response.leap))
    print("Root Delay: ", response.root_delay)
    print(ntplib.ref_id_to_text(response.ref_id))


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Query NTP Server')
    parser.add_argument('--address', action="store", dest="address",  default='pool.ntp.org')
    parser.add_argument('--version', action="store", dest="version",  type=int, default=3)
    given_args = parser.parse_args() 
    address = given_args.address
    version = given_args.version
    main (address, version)

