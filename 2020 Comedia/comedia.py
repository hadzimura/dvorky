#!/usr/bin/env python3
import RPi.GPIO as GPIO
from gpiozero import PWMLED
from gpiozero import Button
from gpiozero import MotionSensor

import os
import sys
import time
from subprocess import Popen
from subprocess import call
from time import sleep

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
	
	def __init__(self, video_file):
		
		self.play_loop = ['omxplayer', '-r', '-b', '--aspect-mode', 'fill', '--no-osd', '--loop', '-o', 'local', video_file]
		self.play_once = ['omxplayer', '-r', '-b', '--aspect-mode', 'fill', '--no-osd', '-o', 'local', video_file]
		
		self.kill = 'killall -s 9 omxplayer.bin > /dev/null 2>&1'

	def kill(self):
		os.system(self.kill)

	def play(self, mode='once', style='blocking'):
		
		if mode == 'once':
			play_me = self.play_once
		elif mode == 'looped':
			play_me = self.play_loop
	
		if style == 'foreground':
			call(play_me)
		elif style == 'background':
			Popen(play_me)


class ShowMustGoOn(object):

	# Define HW components
	red_switch = Button(17)
	red_light = PWMLED(27, initial_value=0)
	sensor_motion = MotionSensor(x)
	
	# Define board lights
	system_red = LED(x, initial_value=0)
	system_green = LED(x, initial_value=0)
	system_white = LED(x, initial_value=0)

	# Define videos
	video_intro = Player('/home/pi/Comedia/intro.mp4')
	video_feature = Player('/home/pi/Comedia/comedia.mp4')
	video_outro = Player('/home/pi/Comedia/outro.mp4')

	# Clear system status
	system_red.off()
	system_green.off()
	system_white.off()

	# States of the play
	number_of_laughs = 0
	audience = False

	# TODO: Log number of plays!

	# Endless loop
	while True:
		
		# First boot
		if number_of_laughs == 0:
			for frenzy in range(1, 10):
				red_light.on()
				sleep(1 / frenzy)
				red_light.off(0.2)
		
		# Wait for audience: motion based
		if audience is False:
			# TODO: fallback if broken
			sensor_motion.wait_for_motion()
			audience = True
		
		# Boot sequence
		system_white.on()
		video_intro.start(mode='looped', style='background')
		
		# Wait for Godot
		# red_light.blink(on_time=1, off_time=1, fade_in_time=1, fade_out_time=1)
		red_light.pulse(fade_in_time=1, fade_out_time=1, n=None, background=True)
		while red_switch.value == 0:
			# TODO: TonalBuzzer
			pass
		
		# Show is a go!
		system_white.on()
		# TODO: TonalBuzzer
		
		# Shut the RedLight off
		for showtime in range(1, 100):
			red_light.value = (1 - showtime / 100)
			sleep(0.01)
			
		system_white.off()
		
		# The wait is over
		# TODO: Intro fadeout?
		video_intro.stop()

		# Comedia
		system_green.on()
		video_feature.start(mode='once', style='foreground')
		system_green.off()
		
		# TODO: wait for this to end...?
		
		# Release the audience
		# video_outro.start()
		
		# Wait before next show
		system_red.on()
		sleep(15)
		system_red.off()
		
		# See if there is anyone present
		if sensor_motion.motion_detected() is True:
			audience = True
		else:
			audience = False


if __name__ == "__main__":
	
	# Board lights:
	# Boot & wait: White ON
	# Comedia: Green ON
	# Outro: Red ON
	ShowMustGoOn()
