#!/bin/bash
##############################################################################
# Python Network Programming Cookbook, Second Edition -- Chapter - 13
##############################################################################

sudo apt-get update
sudo apt-get install -y git
# To offer the capability for sys-admins to restrict program capabilities 
#   with per-program profiles.
sudo apt-get install -y apparmor

# Pyyaml is a required package for the configuration scripts.
sudo pip2 install pyyaml

# Cheetah is a required package for the templates and code generation.
sudo pip2 install cheetah

git clone https://gerrit.opnfv.org/gerrit/compass4nfv

cd compass4nfv

CURRENT_DIR=$PWD
SCENARIO=${SCENARIO:-os-nosdn-nofeature-ha.yml}

# The build script builds the iso file.
# You could also have downloaded the iso file: such as,
# $ wget http://artifacts.opnfv.org/compass4nfv/danube/opnfv-2017-07-19_08-55-09.iso
./build.sh

export TAR_URL=file://$CURRENT_DIR/work/building/compass.tar.gz

# Export the below locations. 
export DHA=$CURRENT_DIR/deploy/conf/vm_environment/$SCENARIO
export NETWORK=$CURRENT_DIR/deploy/conf/vm_environment/network.yml
# Otherwise, your installation will fail with an error message similar to the below:
#   + check_input_para
#   + python /home/pradeeban/programs/opnfv/util/check_valid.py '' ''
#   DHA file doesn't exist
#   + '[' 1 -ne 0 ']'
#   + exit 1


# If you were following the offline installation, you also need to download a jumpshot environment bundle.
# It consists of the dependencies.
# $ wget http://artifacts.opnfv.org/compass4nfv/package/master/jh_env_package.tar.gz
# Now export the absolute path for these directions (following the below example):
# export ISO_URL=file:///home/compass/compass4nfv.iso
# export JHPKG_URL=file:///home/compass/jh_env_package.tar.gz

# This is the command that is common for both online and offline installations.
./deploy.sh
