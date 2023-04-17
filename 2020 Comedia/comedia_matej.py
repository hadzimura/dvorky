#!/usr/bin/env python3
import RPi.GPIO as GPIO
from gpiozero import Button

import os
import sys
import time
from subprocess import Popen
from subprocess import call
from time import sleep, time

# There are two ways of numbering the IO pins on a Raspberry Pi within RPi.GPIO.
# The first is using the BOARD numbering system. This refers to the pin numbers on the P1 header of the Raspberry Pi
# board. The advantage of using this numbering system is that your hardware will always work, regardless of the board
# revision of the RPi. You will not need to rewire your connector or change your code.
# The second numbering system is the BCM numbers. This is a lower level way of working - it refers to the channel
# numbers on the Broadcom SOC. You have to always work with a diagram of which channel number goes to which pin
# on the RPi board. Your script could break between revisions of Raspberry Pi boards.

# Docs: https://sourceforge.net/p/raspberry-gpio-python/wiki/Inputs/
# You need to set up every channel you are using as an input or an output. To configure a channel as an input:


class Player(object):
	""" OMXPlayer: https://github.com/popcornmix/omxplayer/ """
	
	def __init__(self, video, audio='local'):

		self.play_once = ['omxplayer', '-r', '-b', '--aspect-mode', 'fill', '--no-osd', '-o', audio, video]
		self.play_loop = ['omxplayer', '-r', '-b', '--aspect-mode', 'fill', '--no-osd', '--loop', '-o', audio, video]

	def play(self, mode='looped', style='background'):

		"""
		Using the 'play' method without arguments defaults to mode='looped' and style='background',
		so the video is looped and user input continuously read.

		Mode:
			once    = play video without the '--loop' parameter
			looped  = loop the video in a "až do zblbnutí" manner

		Style:
			foreground  = does not allow any other kind of interaction (interrupts are ignored)
			background  = reads the input interrupts (keypresses, button actions etc.)
		"""

		play_me = None

		# Set the video behaviour (once/looped)
		if mode == 'once':
			play_me = self.play_once
		elif mode == 'looped':
			play_me = self.play_loop

		# Play video using the defined behaviour in a selected style (background/foreground)
		if style == 'foreground':
			call(play_me)
		elif style == 'background':
			Popen(play_me)


class ShowMustGoOn(object):

	# Define HW Button
	main_switch = Button(17)

	# Define MAIN video
	video_feature = Player('/home/pi/filmy/aaaaaaaa.mp4')

	# Define support videos
	video_intro = Player('/home/pi/filmy/bbbbbbbbb.mp4')
	video_outro = Player('/home/pi/filmy/ccccccccc.mp4')

	# Enter the endless loop
	while True:

		# Play the "Push the button" video endlessly but read
		video_intro.play()

		# Wait for start of the show (i.e. when someone do the button pressing)
		while main_switch.value == 0:
			pass

		# Button pressed: kill the intro video first
		os.system('killall -s 9 omxplayer.bin > /dev/null 2>&1')

		# Wait for a split second so that the button pres too long does not end the video
		# Another possible solution to the button zapping would be to play the Feature video in a
		# once/foreground manner so that anyone can press the button however he/she wants and THEN run it in a looped
		# background way. Caveat of this is obvious: the first playthrough is breakable only via RPi reboot :)

		# Block the press, Method 1: The Good Old Powerplay, i.e. just wait
		sleep(0.3)
		# Block the press, Method 2: Set a timer. Get current time first:
		safety_timer = time()

		# Adjust the possible Player lag?
		# sleep(?)

		# Run the main video! Looped & background, as this is still a default behaviour
		video_feature.play()

		# Block the press, Method 2: Get current time and subtract the safety_timer time.
		# And only when the result time-delta is bigger than 5 seconds, let anything else happen'...
		while int(time() - safety_timer) < 5:
			pass

		# And wait for any other button presses.
		while main_switch.value == 0:
			pass

		# Button pressed so kill the looped video first:
		os.system('killall -s 9 omxplayer.bin > /dev/null 2>&1')

		# Optional: Display exit video with message such as "Neverending story interrupted"
		# But play it only 'once' and do not let the user mashing the button break things
		video_outro.play(mode='once', style='foreground')

		# When the video ends, the endless loop will proceed to initial sequence above, no need to kill the player


if __name__ == "__main__":
	ShowMustGoOn()
