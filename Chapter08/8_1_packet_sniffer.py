#!/usr/bin/env python
# Python Network Programming Cookbook, Second Edition -- Chapter - 8
# This program is optimized for Python 2.7.12.
# It may run on any other version with/without modifications.

import argparse
import pcap
from construct.protocols.ipstack import ip_stack


def print_packet(pktlen, data, timestamp):
    """ Callback for priniting the packet payload"""
    if not data:
        return
    
    stack = ip_stack.parse(data)
    payload = stack.next.next.next
    print (payload)

def main():
    # setup commandline arguments
    parser = argparse.ArgumentParser(description='Packet Sniffer')
    parser.add_argument('--iface', action="store", dest="iface", default='eth0')
    parser.add_argument('--port', action="store", dest="port", default=80, type=int)
    # parse arguments
    given_args = parser.parse_args()
    iface, port =  given_args.iface, given_args.port
    # start sniffing
    pc = pcap.pcapObject()
    pc.open_live(iface, 1600, 0, 100)
    pc.setfilter('dst port %d' %port, 0, 0)
    
    print ('Press CTRL+C to end capture')
    try:
        while True:
            pc.dispatch(1, print_packet)
    except KeyboardInterrupt:
        print ('Packet statistics: %d packets received, %d packets dropped, %d packets dropped by the interface' % pc.stats())

if __name__ == '__main__':
    main()
        
