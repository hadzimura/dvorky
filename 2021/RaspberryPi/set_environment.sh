#!/usr/bin/env bash

# Set default Python interpreter
update-alternatives --install /usr/bin/python python /usr/bin/python3.7 10 \
update-alternatives --install /usr/bin/pip pip /usr/bin/pip3 10

# Install PIGPIO packages for NRF24L01 comms
sudo apt-get install pigpio python-pigpio python3-pigpio

# Sound too low?
# 1) Run alsamixer from console
# 2) Press F6 and select the "bcm2835 Headphones"
# 3) Press UP to increase the volume level
