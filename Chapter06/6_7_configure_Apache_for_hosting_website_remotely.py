#!/usr/bin/env python
# Python Network Programming Cookbook, Second Edition -- Chapter - 6
# This program is optimized for Python 2.7.12 and Python 3.5.2.
# It may run on any other version with/without modifications.

from getpass import getpass
from fabric.api import env, put, sudo, prompt
from fabric.contrib.files import exists

WWW_DOC_ROOT = "/data/apache/test/"
WWW_USER = "www-data"
WWW_GROUP = "www-data"
APACHE_SITES_PATH = "/etc/apache2/sites-enabled/"
APACHE_INIT_SCRIPT = "/etc/init.d/apache2 "


def remote_server():
    env.hosts = ['127.0.0.1']
    env.user = prompt('Enter user name: ')
    env.password = getpass('Enter your system password: ')


def setup_vhost():
    """ Setup a test website """
    print ("Preparing the Apache vhost setup...")
    print ("Setting up the document root...")
    if exists(WWW_DOC_ROOT):
        sudo("rm -rf %s" %WWW_DOC_ROOT)
    sudo("mkdir -p %s" %WWW_DOC_ROOT)
    sudo("chown -R %s.%s %s" %(env.user, env.user, WWW_DOC_ROOT))
    put(local_path="index.html", remote_path=WWW_DOC_ROOT)
    sudo("chown -R %s.%s %s" %(WWW_USER, WWW_GROUP, WWW_DOC_ROOT))
    print ("Setting up the vhost...")
    sudo("chown -R %s.%s %s" %(env.user, env.user, APACHE_SITES_PATH))
    put(local_path="vhost.conf", remote_path=APACHE_SITES_PATH)
    sudo("chown -R %s.%s %s" %('root', 'root', APACHE_SITES_PATH))
    sudo("%s restart" %APACHE_INIT_SCRIPT)
    print ("Setup complete. Now open the server path http://abc.remote-server.org/ in your web browser.")

