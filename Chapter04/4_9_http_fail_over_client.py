#!/usr/bin/env python
# Python Network Programming Cookbook -- Chapter - 4
# This program requires Python 3.5.2 or any later version
# It may run on any other version with/without modifications.
#
# Follow the comments inline to make it run on Python 2.7.x.

import urllib.request, urllib.parse, urllib.error
# Comment out the above line and uncomment the below for Python 2.7.x.
#import urllib

import os

TARGET_URL = 'http://python.org/ftp/python/2.7.4/'
TARGET_FILE = 'Python-2.7.4.tgz'

class CustomURLOpener(urllib.request.FancyURLopener):
# Comment out the above line and uncomment the below for Python 2.7.x.
#class CustomURLOpener(urllib.FancyURLopener):
    """Override FancyURLopener to skip error 206 (when a
       partial file is being sent)
    """
    def http_error_206(self, url, fp, errcode, errmsg, headers, data=None):
        pass

def resume_download():
	file_exists = False
	CustomURLClass = CustomURLOpener()
	if os.path.exists(TARGET_FILE):
		out_file = open(TARGET_FILE,"ab")
		file_exists = os.path.getsize(TARGET_FILE)
		#If the file exists, then only download the unfinished part
		CustomURLClass.addheader("range","bytes=%s-" % (file_exists))
	else:
		out_file = open(TARGET_FILE,"wb")

	web_page = CustomURLClass.open(TARGET_URL + TARGET_FILE)

	#Check if last download was OK
	if int(web_page.headers['Content-Length']) == file_exists:
		loop = 0
		print ("File already downloaded!")

	byte_count = 0
	while True:
		data = web_page.read(8192)
		if not data:
			break
		out_file.write(data)
		byte_count = byte_count + len(data)

	web_page.close()
	out_file.close()

	for k,v in list(web_page.headers.items()):
    # Comment out the above line and uncomment the below for Python 2.7.x.
	#for k,v in web_page.headers.items():
		print (k, "=",v)
	print ("File copied", byte_count, "bytes from", web_page.url)

if __name__ == '__main__':
	resume_download()
