#!/usr/bin/env python
# Python Network Programming Cookbook, Second Edition -- Chapter - 11
# This program is optimized for Python 2.7.12 and Python 3.5.2.
# It may run on any other version with/without modifications.

import argparse
from ldap3 import Server, Connection, ALL, core


def main(address, dn, password):
    # Create the Server object with the given address.
    server = Server(address, get_info=ALL)
    #Create a connection object, and bind with the given DN and password.
    try: 
        conn = Connection(server, dn, password, auto_bind=True)
        print('LDAP Bind Successful.')
        # Perform a search for a pre-defined criteria.
        # Mention the search filter / filter type and attributes.
        conn.search('dc=example,dc=com', '(&(uid=euler))' , attributes=['sn'])
        # Print the resulting entries.
        print(conn.entries[0])
    except core.exceptions.LDAPBindError as e:
        # If the LDAP bind failed for reasons such as authentication failure.
        print('LDAP Bind Failed: ', e)

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Query LDAP Server')
    parser.add_argument('--address', action="store", dest="address",  default='ldap.forumsys.com')
    parser.add_argument('--dn', action="store", dest="dn",  default='cn=read-only-admin,dc=example,dc=com')
    parser.add_argument('--password', action="store", dest="password",  default='password')
    given_args = parser.parse_args() 
    address = given_args.address
    dn = given_args.dn
    password = given_args.password
    main (address, dn, password)

