#!/usr/bin/env python
# Python Network Programming Cookbook, Second Edition -- Chapter - 5
# This program is optimized for Python 2.7.12 and Python 3.5.2.
# It may run on any other version with/without modifications.

import smtplib
import email.utils
import argparse
from email.mime.text import MIMEText

def mail_client(host, port, fromAddress, toAddress, subject, body):
    msg = MIMEText(body)
    msg['To'] = email.utils.formataddr(('Recipient', toAddress))
    msg['From'] = email.utils.formataddr(('Author', fromAddress))
    msg['Subject'] = subject

    server = smtplib.SMTP(host, port)
    server.set_debuglevel(True)  
    try:
        server.sendmail(fromAddress, toAddress, msg.as_string())
    finally:
        server.quit()


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Mail Server Example')
    parser.add_argument('--host', action="store", dest="host", type=str, required=True)
    parser.add_argument('--port', action="store", dest="port", type=int, required=True)
    parser.add_argument('--fromAddress', action="store", dest="fromAddress", type=str, required=True)
    parser.add_argument('--toAddress', action="store", dest="toAddress", type=str, required=True)
    parser.add_argument('--subject', action="store", dest="subject", type=str, required=True)
    parser.add_argument('--body', action="store", dest="body", type=str, required=True)
    given_args = parser.parse_args()
    mail_client(given_args.host, given_args.port, given_args.fromAddress, given_args.toAddress, given_args.subject, given_args.body)

