#!/usr/bin/env python
# Python Network Programming Cookbook, Second Edition -- Chapter - 6
# This program is optimized for Python 3.5.2.
# It may run on any other version with/without modifications.
# To make it run on Python 2.7.x, needs some changes due to API differences.
# Follow the comments inline to make the program work with Python 2.


import argparse
import paramiko
import getpass


SOURCE = '6_2_copy_remote_file_over_sftp.py' 
DESTINATION ='/tmp/6_2_copy_remote_file_over_sftp.py '


def copy_file(hostname, port, username, password, src, dst):
    client = paramiko.SSHClient()
    client.load_system_host_keys()
    print (" Connecting to %s \n with username=%s... \n" %(hostname,username))
    t = paramiko.Transport(hostname, port)
    t.connect(username=username,password=password)
    sftp = paramiko.SFTPClient.from_transport(t)
    print ("Copying file: %s to path: %s" %(src, dst))
    sftp.put(src, dst)
    sftp.close()
    t.close()


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Remote file copy')
    parser.add_argument('--host', action="store", dest="host", default='localhost')
    parser.add_argument('--port', action="store", dest="port", default=22, type=int)
    parser.add_argument('--src', action="store", dest="src", default=SOURCE)
    parser.add_argument('--dst', action="store", dest="dst", default=DESTINATION)
    
    given_args = parser.parse_args()
    hostname, port =  given_args.host, given_args.port
    src, dst = given_args.src, given_args.dst
    
    user = input("Enter your remote account: ")
    # Comment out the above line and uncomment the below line for Python 2.7.
    # user = raw_input("Enter your remote account: ")

    password = getpass.getpass("Enter password for %s: " %user)
    
    copy_file(hostname, port, user, password, src, dst)
