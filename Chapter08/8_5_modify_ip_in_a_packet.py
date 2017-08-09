#!/usr/bin/env python
# Python Network Programming Cookbook, Second Edition -- Chapter - 8
# This program is optimized for Python 2.7.12 and Python 3.5.2.
# It may run on any other version with/without modifications.


import argparse
import sys
import re
from random import randint

from scapy.all import IP,TCP,UDP,conf,send


def send_packet(protocol=None, src_ip=None, src_port=None, flags=None, dst_ip=None, dst_port=None, iface=None):
    """Modify and send an IP packet."""
    if protocol == 'tcp':
        packet = IP(src=src_ip, dst=dst_ip)/TCP(flags=flags, sport=src_port, dport=dst_port)
    elif protocol == 'udp':
        if flags: raise Exception(" Flags are not supported for udp")
        packet = IP(src=src_ip, dst=dst_ip)/UDP(sport=src_port, dport=dst_port)
    else:
        raise Exception("Unknown protocol %s" % protocol)

    send(packet, iface=iface)
   

if __name__ == '__main__':
    # setup commandline arguments
    parser = argparse.ArgumentParser(description='Packet Modifier')
    parser.add_argument('--iface', action="store", dest="iface", default='eth0')
    parser.add_argument('--protocol', action="store", dest="protocol", default='tcp')
    parser.add_argument('--src-ip', action="store", dest="src_ip", default='1.1.1.1')
    parser.add_argument('--src-port', action="store", dest="src_port", default=randint(0, 65535))
    parser.add_argument('--dst-ip', action="store", dest="dst_ip", default='192.168.1.51')
    parser.add_argument('--dst-port', action="store", dest="dst_port", default=randint(0, 65535))
    parser.add_argument('--flags', action="store", dest="flags", default=None)
    # parse arguments
    given_args = parser.parse_args()
    iface, protocol, src_ip,  src_port, dst_ip, dst_port, flags =  given_args.iface, given_args.protocol, given_args.src_ip,\
      given_args.src_port, given_args.dst_ip, given_args.dst_port, given_args.flags
    send_packet(protocol, src_ip, src_port, flags, dst_ip, dst_port, iface)

