#!/usr/bin/env python
# Python Network Programming Cookbook, Second Edition -- Chapter - 11
# This program is optimized for Python 2.7.12 and Python 3.5.2.
# It may run on any other version with/without modifications.

import argparse
import dns.zone
import dns.resolver
import socket

def main(address):
    # IPv4 DNS Records
    answer = dns.resolver.query(address, 'A')
    for i in xrange(0, len(answer)):
        print("Default: ", answer[i])

    # IPv6 DNS Records
    try:
        answer6 = dns.resolver.query(address, 'AAAA')
        for i in xrange(0, len(answer6)):
            print("Default: ", answer6[i])
    except dns.resolver.NoAnswer as e:
        print("Exception in resolving the IPv6 Resource Record:", e)

    # MX (Mail Exchanger) Records
    try:
        mx = dns.resolver.query(address, 'MX')
        for i in xrange(0, len(mx)):
            print("Default: ", mx[i])
    except dns.resolver.NoAnswer as e:
        print("Exception in resolving the MX Resource Record:", e)

    try: 
        cname_answer = dns.resolver.query(address, 'CNAME')
        print("CNAME: ", cname_answer)
    except dns.resolver.NoAnswer as e:
        print('Exception retrieving CNAME', e)

    try:
        ns_answer = dns.resolver.query(address, 'NS')
        print(ns_answer)
    except dns.resolver.NoAnswer as e:
        print("Exception in resolving the NS Resource Record:", e)

    try: 
        sig_answer = dns.resolver.query(address, 'SIG')
        print("SIG: ", sig_answer)
    except dns.resolver.NoAnswer as e:
        print('Exception retrieving SIG', e)

    try: 
        key_answer = dns.resolver.query(address, 'KEY')
        print("KEY: ", key_answer)
    except dns.resolver.NoAnswer as e:
        print('Exception retrieving KEY', e)

    soa_answer = dns.resolver.query(address, 'SOA')
    print("SOA Answer: ", soa_answer[0].mname)
    master_answer = dns.resolver.query(soa_answer[0].mname, 'A')
    print("Master Answer: ", master_answer[0].address)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='DNS Python')
    parser.add_argument('--address', action="store", dest="address",  default='dnspython.org')
    given_args = parser.parse_args() 
    address = given_args.address
    main (address)

