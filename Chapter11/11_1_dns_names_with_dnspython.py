#!/usr/bin/env python
# Python Network Programming Cookbook, Second Edition -- Chapter - 11
# This program is optimized for Python 2.7.12 and Python 3.5.2.
# It may run on any other version with/without modifications.


import argparse
import dns.name

def main(site1, site2):
    _site1 = dns.name.from_text(site1)
    _site2 = dns.name.from_text(site2)
    print("site1 is subdomain of site2: ", _site1.is_subdomain(_site2)) 
    print("site1 is superdomain of site2: ", _site1.is_superdomain(_site2)) 
    print("site1 labels: ", _site1.labels)
    print("site2 labels: ", _site2.labels)

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='DNS Python')
    parser.add_argument('--site1', action="store", dest="site1",  default='www.dnspython.org')
    parser.add_argument('--site2', action="store", dest="site2",  default='dnspython.org')
    given_args = parser.parse_args() 
    site1 = given_args.site1
    site2 = given_args.site2
    main (site1, site2)

