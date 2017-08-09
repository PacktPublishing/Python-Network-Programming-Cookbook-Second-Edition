#!/usr/bin/env python
# Python Network Programming Cookbook, Second Edition -- Chapter - 5
# This program is optimized for Python 2.7.12 and Python 3.5.2.
# It may run on any other version with/without modifications.

import re
import smtplib
import dns.resolver
import argparse


def mail_checker(fromAddress, toAddress):

    regex = '^[a-z0-9][a-z0-9._%+-]{0,63}@[a-z0-9-]+(\.[a-z0-9-]+)*(\.[a-z]{2,})$'

    addressToVerify = str(toAddress)

    match = re.match(regex, addressToVerify)
    if match == None:
	    print('Bad Syntax in the address to verify. Re-enter the correct value')
	    raise ValueError('Bad Syntax')

    splitAddress = addressToVerify.split('@')
    domain = str(splitAddress[1])

    records = dns.resolver.query(domain, 'MX')
    mxRecord = records[0].exchange
    mxRecord = str(mxRecord)


    server = smtplib.SMTP()
    server.set_debuglevel(1)

    try:
        server.connect(mxRecord)
    except Exception as e:
        print ("Mail Check Failed Due to Error: %s" %str(e))
        return
 
    server.helo(server.local_hostname) 
    server.mail(fromAddress)
    code, message = server.rcpt(str(addressToVerify))
    server.quit()

    if code == 250:
	    print('Successfully verified the email: %s', fromAddress)
    else:
	    print('Failed to verify the email: %s', fromAddress)



if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Mail Server Example')
    parser.add_argument('--fromAddress', action="store", dest="fromAddress", type=str, required=True)
    parser.add_argument('--toAddress', action="store", dest="toAddress", type=str, required=True)
    given_args = parser.parse_args()
    mail_checker(given_args.fromAddress, given_args.toAddress)

