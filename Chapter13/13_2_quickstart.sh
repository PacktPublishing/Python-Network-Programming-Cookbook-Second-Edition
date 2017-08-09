#!/bin/bash
##############################################################################
# Python Network Programming Cookbook, Second Edition -- Chapter - 13
##############################################################################

# Install Dependencies
sudo apt-get install libpcap-dev

# Get DPDK
wget http://fast.dpdk.org/rel/dpdk-17.05.1.tar.xz
tar -xvf dpdk-17.05.1.tar.xz
cd dpdk-stable-17.05.1

# Build DPDK
make config T=x86_64-native-linuxapp-gcc
sed -ri 's,(PMD_PCAP=).*,\1y,' build/.config
make

# Install DPDK
sudo make install
printf "DPDK Installation Complete.\n"
