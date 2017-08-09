#!/bin/bash
##############################################################################
# Python Network Programming Cookbook, Second Edition -- Chapter - 12
# Adopted from https://github.com/Juniper/contrail-controller/wiki/Install-and-Configure-OpenContrail-1.06
##############################################################################

# Configue the Ubuntu repositories.
echo "deb http://ppa.launchpad.net/opencontrail/ppa/ubuntu precise main" | sudo tee -a /etc/apt/sources.list.d/opencontrail.list
sudo apt-key adv --keyserver keyserver.ubuntu.com --recv-keys 16BD83506839FE77
sudo apt-get update

# Install Contrail Virtual Rouer Agent
sudo apt-get install contrail-vrouter-agent

sudo modprobe vrouter
echo "vrouter" | sudo tee -a /etc/modules
