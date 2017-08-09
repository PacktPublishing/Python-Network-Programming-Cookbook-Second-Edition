#!/bin/bash
##############################################################################
# Python Network Programming Cookbook, Second Edition -- Chapter - 11
##############################################################################


# Download and extract RequestsThrottler
wget https://pypi.python.org/packages/d5/db/fc7558a14efa163cd2d3e4515cdfbbfc2dacc1d2c4285b095104c58065c7/RequestsThrottler-0.1.0.tar.gz
tar -xvf RequestsThrottler-0.1.0.tar.gz
cd RequestsThrottler-0.1.0

# Copy our recipe into the folder
cp ../11_10_requests_throttling.py requests_throttler

# Configure and Install RequestsThrottling
python setup.py build
sudo python setup.py install

