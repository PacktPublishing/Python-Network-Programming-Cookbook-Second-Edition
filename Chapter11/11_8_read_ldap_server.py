#!/usr/bin/env python
# Python Network Programming Cookbook, Second Edition -- Chapter - 11
# This program is optimized for Python 2.7.12 and Python 3.5.2.
# It may run on any other version with/without modifications.
# Adopted from http://ldap3.readthedocs.io/tutorial_abstraction_basic.html

from ldap3 import Server, Connection, ObjectDef, AttrDef, Reader, Writer, ALL


def main():
    server = Server('ipa.demo1.freeipa.org', get_info=ALL)
    conn = Connection(server, 'uid=admin,cn=users,cn=accounts,dc=demo1,dc=freeipa,dc=org', 'Secret123', auto_bind=True)
    person = ObjectDef('person', conn)
    r = Reader(conn, person, 'ou=ldap3-tutorial,dc=demo1,dc=freeipa,dc=org')
    print(r)
    print('************')
    person+='uid'
    print(r)

if __name__ == '__main__':
    main ()

