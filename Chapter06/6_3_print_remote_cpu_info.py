#!/usr/bin/env python
# Python Network Programming Cookbook, Second Edition -- Chapter - 6
# This program is optimized for Python 3.5.2.
# It may run on any other version with/without modifications.
# To make it run on Python 2.7.x, needs some changes due to API differences.
# Follow the comments inline to make the program work with Python 2.


import argparse
import getpass
import paramiko

RECV_BYTES = 4096
COMMAND = 'cat /proc/cpuinfo'

def print_remote_cpu_info(hostname, port, username, password):
    client = paramiko.Transport((hostname, port))
    client.connect(username=username, password=password)
    
    stdout_data = []
    stderr_data = []
    session = client.open_channel(kind='session')
    session.exec_command(COMMAND)
    while True:
        if session.recv_ready():
            stdout_data.append(session.recv(RECV_BYTES))
        if session.recv_stderr_ready():
            stderr_data.append(session.recv_stderr(RECV_BYTES))
        if session.exit_status_ready():
            break
    
    print ('exit status: ', session.recv_exit_status())
    print (b''.join(stdout_data))
    print (b''.join(stderr_data))
    
    session.close()
    client.close()

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Remote file copy')
    parser.add_argument('--host', action="store", dest="host", default='localhost')
    parser.add_argument('--port', action="store", dest="port", default=22, type=int)    
    given_args = parser.parse_args()
    hostname, port =  given_args.host, given_args.port
    
    user = input("Enter your remote account: ")
    # Comment out the above line and uncomment the below line for Python 2.7.
    # user = raw_input("Enter your remote account: ")

    password = getpass.getpass("Enter password for %s: " %user)
    print_remote_cpu_info(hostname, port, user, password)

