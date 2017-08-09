#!/usr/bin/env python
# Python Network Programming Cookbook, Second Edition -- Chapter - 8
# This program is optimized for Python 2.7.12 and Python 3.5.2.
# It may run on any other version with/without modifications.


import os
from scapy.all import *

pkts = []
count = 0
pcapnum = 0

def write_cap(x):
    global pkts
    global count
    global pcapnum
    pkts.append(x)
    count += 1
    if count == 3:
        pcapnum += 1
        pname = "pcap%d.pcap" % pcapnum
        wrpcap(pname, pkts)
        pkts = []
        count = 0

def test_dump_file():
    print ("Testing the dump file...")
    dump_file = "./pcap1.pcap"
    if os.path.exists(dump_file):
        print ("dump fie %s found." %dump_file)
        pkts = sniff(offline=dump_file)
        count = 0
        while (count <=2):
            print ("----Dumping pkt:%s----" %count)
            print (hexdump(pkts[count]))
            count += 1
        
    else:
        print ("dump fie %s not found." %dump_file)

if __name__ == '__main__':
    print ("Started packet capturing and dumping... Press CTRL+C to exit")
    sniff(prn=write_cap)
    test_dump_file()

