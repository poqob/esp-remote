#!/bin/bash
# This script is used to install the required packages for the project. 
# package: lftp
# environment: ubuntu, debian, termux, arch, fedora, centos, alpine, windows
# usage: ./install-dependencies.sh

# Check if lftp is installed
if ! command -v lftp &> /dev/null
then
    echo "lftp could not be found, installing..."
    # Check the package manager and install lftp
    if [ -f /etc/debian_version ]; then
        sudo apt-get update && sudo apt-get install -y lftp
    elif [ -f /etc/redhat-release ]; then
        sudo yum install -y lftp
    elif [ -f /etc/arch-release ]; then
        sudo pacman -Syu lftp
    elif [ -f /etc/alpine-release ]; then
        sudo apk add lftp
    elif [ -f /data/data/com.termux/files/usr/bin/bash ]; then
        pkg install lftp
    elif [[ "$OSTYPE" == "msys" || "$OSTYPE" == "cygwin" || "$OSTYPE" == "win32" ]]; then
        echo "Detected Windows. Installing lftp using Chocolatey..."
        if ! command -v choco &> /dev/null
        then
            echo "Chocolatey is not installed. Please install Chocolatey first: https://chocolatey.org/install"
            exit 1
        fi
        choco install -y lftp
    else
        echo "Unsupported OS. Please install lftp manually."
        exit 1
    fi
else
    echo "lftp is already installed."
fi
