#!/bin/bash
set -e

# Update the package list and install prerequisite packages
sudo apt-get update -y
sudo apt-get install -y \
    apt-transport-https \
    ca-certificates \
    curl \
    software-properties-common

# Add Docker’s official GPG key
curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo gpg --dearmor -o /usr/share/keyrings/docker-archive-keyring.gpg

# Set up the stable Docker repository
echo "deb [arch=$(dpkg --print-architecture) signed-by=/usr/share/keyrings/docker-archive-keyring.gpg] https://download.docker.com/linux/ubuntu $(lsb_release -cs) stable" | sudo tee /etc/apt/sources.list.d/docker.list > /dev/null

# Update the package list and install Docker
sudo apt-get update -y
sudo apt-get install -y docker-ce docker-ce-cli containerd.io

# Start Docker and enable it to run on startup
sudo systemctl start docker
sudo systemctl enable docker

# Pull the Docker image
sudo docker pull sundance02/memmy:1.0

# Run the Docker container
sudo docker run -d -p 8000:8000 --name mem_med_app sundance02/memmy:1.0
