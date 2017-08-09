#!/usr/bin/env python
# Python Network Programming Cookbook, Second Edition -- Chapter - 11
# This program is optimized for Python 2.7.12 and Python 3.5.2.
# It may run on any other version with/without modifications.

import argparse
import dns.zone
import dns.resolver
import socket

def main(address):
    soa_answer = dns.resolver.query(address, 'SOA')
    master_answer = dns.resolver.query(soa_answer[0].mname, 'A')
    try:
        z = dns.zone.from_xfr(dns.query.xfr(master_answer[0].address, address))
        names = z.nodes.keys()
        names.sort()
        for n in names:
            print(z[n].to_text(n))
    except socket.error as e:
        print('Failed to perform zone transfer:', e)
    except dns.exception.FormError as e:
        print('Failed to perform zone transfer:', e)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='DNS Python')
    parser.add_argument('--address', action="store", dest="address",  default='dnspython.org')
    given_args = parser.parse_args() 
    address = given_args.address
    main (address)

