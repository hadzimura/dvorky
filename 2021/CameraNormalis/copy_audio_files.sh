#!/usr/bin/env bash

# Set source and destination
# SOURCE_DIR="/home/pi/dvorky/2021/audio_files"
SOURCE_DIR="../audio_files"
DESTINATION_DIR=""

# Get filenames
shopt -s nullglob
AMBIENT_FILES=(${SOURCE_DIR}/ambient*)
SCENE_FILES=$(ls "${SOURCE_DIR}" | grep scene)


# Destination folders structure:
# 01/*.mp3 -> ambient tracks
# 02/*.mp3 -> scene tracks

TRACK_NAME=1
for AMBIENT_FILE in "${AMBIENT_FILES[@]}"
  do
	  echo "${AMBIENT_FILE} -> 0${TRACK_NAME}.mp3"
	  TRACK_NAME=$((TRACK_NAME + 1))
  done


