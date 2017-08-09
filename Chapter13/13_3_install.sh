#!/bin/bash
##############################################################################
# Python Network Programming Cookbook, Second Edition -- Chapter - 13
##############################################################################


# Install Dependencies
sudo apt-get install python-dev python-pip libsnappy-dev
sudo pip install python-snappy kafka-python pyyaml

# Install SNAS Python API
git clone https://github.com/OpenBMP/openbmp-python-api-message.git
cd openbmp-python-api-message
sudo pip install .

# Go back to the root directory.
cd ..

# Download Apache Kafka
wget http://apache.belnet.be/kafka/0.11.0.0/kafka_2.11-0.11.0.0.tgz

tar -xzf kafka_2.11-0.11.0.0.tgz

