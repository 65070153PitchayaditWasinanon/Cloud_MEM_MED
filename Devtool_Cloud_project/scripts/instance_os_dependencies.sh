#!/usr/bin/env bash

# Update package list
sudo apt update

# Install prerequisites
sudo apt install -y software-properties-common

# Add deadsnakes PPA for newer Python versions
sudo add-apt-repository ppa:deadsnakes/ppa
sudo apt update

# Install Python 3.12
sudo apt install -y python3.12

# Install pip for Python 3.12
sudo apt install -y python3.12-distutils
curl -sS https://bootstrap.pypa.io/get-pip.py | sudo python3.12

# Install Virtualenv (using pip)
python3.12 -m pip install virtualenv

# Verify installations
python3.12 --version
pip3.12 --version
virtualenv --version
