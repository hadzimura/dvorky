#!/usr/bin/env bash

# Blank the terminal screen completely
sudo sh -c "TERM=linux setterm -foreground black -clear all >/dev/tty0"

# Start Comedia
python3 comedia.py

# Turn the screen on again
sudo sh -c "TERM=linux setterm -foreground white -clear all >/dev/tty0"