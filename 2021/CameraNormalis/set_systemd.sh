#!/usr/bin/env bash

sudo cp /home/pi/dvorky/2021/CameraNormalis/systemd/camera-daemonis.service /etc/systemd/system/camera-daemonis.service
sudo cp /home/pi/dvorky/2021/CameraNormalis/systemd/cn-watcher.service /etc/systemd/system/cn-watcher.service
sudo cp /home/pi/dvorky/2021/CameraNormalis/systemd/cn-watcher.path /etc/systemd/system/cn-watcher.path

sudo systemctl enable camera-daemonis.service
sudo systemctl enable cn-watcher.service

sudo systemctl start camera-daemonis.service
sudo systemctl start cn-watcher.service