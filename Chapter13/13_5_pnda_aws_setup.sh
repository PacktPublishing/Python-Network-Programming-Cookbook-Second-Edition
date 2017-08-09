#!/bin/bash
##############################################################################
# Python Network Programming Cookbook, Second Edition -- Chapter - 13
##############################################################################

# Clone the Platform Salt
git clone https://github.com/pndaproject/platform-salt.git
cd platform-salt
git checkout release/3.4.1

cd ..

# Clone the PNDA AWS Template latest release tag
git clone git@github.com:pndaproject/pnda-aws-templates.git
cd pnda-aws-templates
git checkout release/3.4.1

# Copy the sample pnda_env.yaml to the project after modifying as in the recipe.
cp ../pnda_env.yaml pnda_env.yaml

# Install Dependencies
cd cli
sudo pip install -r requirements.txt


