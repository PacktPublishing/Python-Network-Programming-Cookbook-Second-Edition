#!/bin/bash
##############################################################################
# Python Network Programming Cookbook, Second Edition -- Chapter - 12
# Adopted from https://github.com/Juniper/contrail-controller/wiki/Install-and-Configure-OpenContrail-1.06
##############################################################################

# Get the redis server binary from http://ftp.ksu.edu.tw/FTP/Linux/ubuntu/ubuntu/pool/universe/r/redis/
# You may use any other working mirror as well.
wget http://ftp.ksu.edu.tw/FTP/Linux/ubuntu/ubuntu/pool/universe/r/redis/redis-server_2.6.13-1_amd64.deb
sudo apt-get install libjemalloc1

# Install redis server
sudo dpkg -i redis-server_2.6.13-1_amd64.deb

echo "deb http://ppa.launchpad.net/opencontrail/ppa/ubuntu precise main" | sudo tee -a /etc/apt/sources.list.d/opencontrail.list
sudo apt-key adv --keyserver keyserver.ubuntu.com --recv-keys 16BD83506839FE77
sudo apt-get update

# Install Contrail Analytics
sudo apt-get install contrail-analytics
