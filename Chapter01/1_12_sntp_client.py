#!/usr/bin/env python
# Python Network Programming Cookbook, Second Edition -- Chapter - 1
# This program is optimized for Python 2.7.12 and Python 3.5.2.
# It may run on any other version with/without modifications.


import socket
import struct
import sys
import time

NTP_SERVER = "0.uk.pool.ntp.org"
TIME1970 = 2208988800

def sntp_client():
    client = socket.socket( socket.AF_INET, socket.SOCK_DGRAM )
    data = '\x1b' + 47 * '\0'
    client.sendto( data.encode('utf-8'), ( NTP_SERVER, 123 ))
    data, address = client.recvfrom( 1024 )
    if data:
        print ('Response received from:', address)
    t = struct.unpack( '!12I', data )[10]
    t -= TIME1970
    print ('\tTime=%s' % time.ctime(t))


if __name__ == '__main__':
    sntp_client()
