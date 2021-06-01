#!/usr/bin/env bash

# Set default Python interpreter
update-alternatives --install /usr/bin/python python /usr/bin/python3.7 10 \
update-alternatives --install /usr/bin/pip pip /usr/bin/pip3 10

# Install PIGPIO packages for NRF24L01 comms
sudo apt-get install pigpio python-pigpio python3-pigpio