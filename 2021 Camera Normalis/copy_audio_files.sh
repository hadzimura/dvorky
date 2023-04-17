#!/usr/bin/env bash

# Set source and destination
# SOURCE_DIR="/home/pi/dvorky/2021/audio_files"
SOURCE_DIR="../audio_files"
DESTINATION_DIR="/media/pi/3A9E-C3AB"

# Get filenames
shopt -s nullglob
AMBIENT_FILES=(${SOURCE_DIR}/ambient*)
SCENE_FILES=$(ls "${SOURCE_DIR}" | grep scene)

# Delete the contents of the SD Card first
rm /media/pi/3A9E-C3AB/*

# Destination folders structure:
# 01/*.mp3 -> ambient tracks
# 02/*.mp3 -> scene tracks

TRACK_NAME=1
for AMBIENT_FILE in "${AMBIENT_FILES[@]}"
  do
	  SOURCE_FILE=$(echo "${AMBIENT_FILE}" | cut -d '/' -f 3)
	  TARGET_FILE="1${TRACK_NAME}.mp3"

    echo "cp ${AMBIENT_FILE} ${DESTINATION_DIR}"
    cp "${AMBIENT_FILE}" "${DESTINATION_DIR}"
    echo "mv ${DESTINATION_DIR}/${AMBIENT_FILE} ${DESTINATION_DIR}/${TARGET_FILE}"
    mv "${DESTINATION_DIR}/${SOURCE_FILE}" "${DESTINATION_DIR}/${TARGET_FILE}"
	  TRACK_NAME=$((TRACK_NAME + 1))
  done

umount "${DESTINATION_DIR}"

