#!/usr/bin/env python
# Python Network Programming Cookbook -- Chapter - 4
# This program requires Python 3.5.2 or any later version
# It may run on any other version with/without modifications.
#
# Follow the comments inline to make it run on Python 2.7.x.

import http.cookiejar 
# Comment out the above line and uncomment the below for Python 2.7.x.
#import cookielib 

import urllib

# Uncomment the below line for Python 2.7.x.
#import urllib2


ID_USERNAME = 'id_username'
ID_PASSWORD = 'id_password'
USERNAME = 'you@email.com'
PASSWORD = 'mypassword'
LOGIN_URL = 'https://bitbucket.org/account/signin/?next=/'
NORMAL_URL = 'https://bitbucket.org/'

def extract_cookie_info():
    """ Fake login to a site with cookie"""
    # setup cookie jar

    cj = http.cookiejar.CookieJar()
    # Comment out the above line and uncomment the below for Python 2.7.x.
    #cj = cookielib.CookieJar()

    login_data = urllib.parse.urlencode({ID_USERNAME : USERNAME, ID_PASSWORD : PASSWORD}).encode("utf-8")
    # Comment out the above line and uncomment the below for Python 2.7.x.
    #login_data = urllib.urlencode({ID_USERNAME : USERNAME, ID_PASSWORD : PASSWORD})

    # create url opener

    opener = urllib.request.build_opener(urllib.request.HTTPCookieProcessor(cj))
    # Comment out the above line and uncomment the below for Python 2.7.x.
    #opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cj))

    resp = opener.open(LOGIN_URL, login_data)

    # send login info 
    for cookie in cj:
        print ("----First time cookie: %s --> %s" %(cookie.name, cookie.value))
    print ("Headers: %s" %resp.headers)

    # now access without any login info
    resp = opener.open(NORMAL_URL)
    for cookie in cj:
        print ("++++Second time cookie: %s --> %s" %(cookie.name, cookie.value))
    
    print ("Headers: %s" %resp.headers)

if __name__ == '__main__':
    extract_cookie_info()
