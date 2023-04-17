#!/usr/bin/env bash

source ".env"

# Set default Python interpreter
update-alternatives --install /usr/bin/python python /usr/bin/python3.7 10 \
update-alternatives --install /usr/bin/pip pip /usr/bin/pip3 10

sudo systemctl enable pigpiod
sudo systemctl start pigpiod

# Blank the terminal screen completely
sudo sh -c "TERM=linux setterm -foreground black -clear all >/dev/tty0"

# Start Garden Od The Day
if [[  -d "${VIRTUAL_ENVIRONMENT_PATH}" ]]; then
  source "${VIRTUAL_ENVIRONMENT_PATH}/bin/activate"
else
  echo "Not deploy.sh - ed?"
  python3 -m pip install --user --upgrade --quiet pip setuptools wheel virtualenv
  virtualenv "${VIRTUAL_ENVIRONMENT_PATH}"
  source "${VIRTUAL_ENVIRONMENT_PATH}"/bin/activate
  python3 -m pip install --upgrade --quiet pip setuptools wheel
  python3 -m pip install --upgrade --quiet -r requirements.txt
fi

python3 garden.py

# Turn the screen on again
sudo sh -c "TERM=linux setterm -foreground white -clear all >/dev/tty0"