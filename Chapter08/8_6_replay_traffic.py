#!/usr/bin/env python
# Python Network Programming Cookbook, Second Edition -- Chapter - 8
# This program is optimized for Python 2.7.12 and Python 3.5.2.
# It may run on any other version with/without modifications.


import argparse
from scapy.all import *


def send_packet(recvd_pkt, src_ip, dst_ip, count):
    """ Send modified packets"""
    pkt_cnt = 0
    p_out = []

    for p in recvd_pkt:
        pkt_cnt += 1
        new_pkt = p.payload
        new_pkt[IP].dst = dst_ip
        new_pkt[IP].src = src_ip
        del new_pkt[IP].chksum
        p_out.append(new_pkt)
        if pkt_cnt % count == 0:
            send(PacketList(p_out))
            p_out = []

    # Send rest of packet
    send(PacketList(p_out))
    print ("Total packets sent: %d" %pkt_cnt)

if __name__ == '__main__':
    # setup commandline arguments
    parser = argparse.ArgumentParser(description='Packet Sniffer')
    parser.add_argument('--infile', action="store", dest="infile", default='pcap1.pcap')
    parser.add_argument('--src-ip', action="store", dest="src_ip", default='1.1.1.1')
    parser.add_argument('--dst-ip', action="store", dest="dst_ip", default='2.2.2.2')
    parser.add_argument('--count', action="store", dest="count", default=100, type=int)
    # parse arguments
    given_args = ga = parser.parse_args()
    global src_ip, dst_ip
    infile, src_ip, dst_ip, count =  ga.infile, ga.src_ip, ga.dst_ip, ga.count
    try:
        pkt_reader = PcapReader(infile)
        send_packet(pkt_reader, src_ip, dst_ip, count)
    except IOError:
        print ("Failed reading file %s contents" % infile)
        sys.exit(1)
