#!/usr/bin/env python
# Python Network Programming Cookbook, Second Edition -- Chapter - 11
# This program is optimized for Python 2.7.12 and Python 3.5.2.
# It may run on any other version with/without modifications.


import argparse
import dns.reversename
import dns.resolver

def main(address):
    n = dns.reversename.from_address(address)
    print(n)
    print(dns.reversename.to_address(n))

    try:
        # Pointer records (PTR) maps a network interface (IP) to the host name.
        domain = str(dns.resolver.query(n,"PTR")[0])
        print(domain)
    except Exception as e:
        print ("Error while resolving %s: %s" %(address, e))


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='DNS Python')
    parser.add_argument('--address', action="store", dest="address",  default='127.0.0.1')
    given_args = parser.parse_args() 
    address = given_args.address
    main (address)

