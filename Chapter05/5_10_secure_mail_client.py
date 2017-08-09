#!/usr/bin/env python
# Python Network Programming Cookbook, Second Edition -- Chapter - 5
# This program is optimized for Python 2.7.12 and Python 3.5.2.
# It may run on any other version with/without modifications.

import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import argparse
import getpass

def mail_client(host, port, fromAddress, password, toAddress, subject, body):
    msg = MIMEMultipart()

    msg['From'] = fromAddress
    msg['To'] = toAddress
    msg['Subject'] = subject
    message = body
    msg.attach(MIMEText(message))

    mailserver = smtplib.SMTP(host,port)

    # Identify to the SMTP Gmail Client
    mailserver.ehlo()

    # Secure with TLS Encryption
    mailserver.starttls()

    # Reidentifying as an encrypted connection
    mailserver.ehlo()
    mailserver.login(fromAddress, password)

    mailserver.sendmail(fromAddress,toAddress,msg.as_string())
    print ("Email sent from:", fromAddress)

    mailserver.quit()



if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Mail Server Example')
    parser.add_argument('--host', action="store", dest="host", type=str, required=True)
    parser.add_argument('--port', action="store", dest="port", type=int, required=True)
    parser.add_argument('--fromAddress', action="store", dest="fromAddress", type=str, required=True)
    parser.add_argument('--toAddress', action="store", dest="toAddress", type=str, required=True)
    parser.add_argument('--subject', action="store", dest="subject", type=str, required=True)
    parser.add_argument('--body', action="store", dest="body", type=str, required=True)
    password = getpass.getpass("Enter your Password:")
    given_args = parser.parse_args()
    mail_client(given_args.host, given_args.port, given_args.fromAddress, password, given_args.toAddress, given_args.subject, given_args.body)

