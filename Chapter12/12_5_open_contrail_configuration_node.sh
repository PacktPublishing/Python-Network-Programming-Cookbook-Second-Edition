#!/bin/bash
##############################################################################
# Python Network Programming Cookbook, Second Edition -- Chapter - 12
# Adopted from https://github.com/Juniper/contrail-controller/wiki/Install-and-Configure-OpenContrail-1.06
##############################################################################

# Download and manually install python-support, as it is dropped from Ubuntu 16.04.
wget http://launchpadlibrarian.net/109052632/python-support_1.0.15_all.deb
sudo dpkg -i python-support_1.0.15_all.deb

# Configuring the package list.
echo "deb http://ppa.launchpad.net/opencontrail/ppa/ubuntu precise main" | sudo tee -a /etc/apt/sources.list.d/opencontrail.list
sudo apt-key adv --keyserver keyserver.ubuntu.com --recv-keys 16BD83506839FE77
echo "deb http://debian.datastax.com/community stable main" | sudo tee -a /etc/apt/sources.list.d/cassandra.sources.list
curl -L http://debian.datastax.com/debian/repo_key | sudo apt-key add -

# Run update
sudo apt-get update

# Install dependencies
sudo apt-get install cassandra=1.2.18 zookeeperd rabbitmq-server ifmap-server

# Install Contrail Config
sudo apt-get install contrail-config

# Configre ifmap-server
echo "control:control" | sudo tee -a /etc/ifmap-server/basicauthusers.properties
sudo service ifmap-server restart
