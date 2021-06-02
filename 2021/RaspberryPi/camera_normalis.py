#!/usr/bin/env python3
# coding=utf-8

from Display import MiniDisplay
from Controller import AKAI_LPD8_MIDI
import mido
import RPi.GPIO as GPIO
import time


class Relay(object):
	
	def __init__(self, pinout):
		
		# Setting a current GPIO mode
		GPIO.setmode(GPIO.BCM)
		
		# Removing the warnings
		GPIO.setwarnings(False)
		
		# creating a list (array) with the number of GPIO's that we use
		self.pins = pinout
		
		# setting the mode for all pins so all will be switched on
		GPIO.setup(self.pins, GPIO.OUT)
		# GPIO.cleanup()
		# time.sleep(0.5)


	def self_test(self, pin):

		""" Test all the relays """

		if pin in self.pins:
			GPIO.output(pin, GPIO.HIGH)
			time.sleep(0.5)
			GPIO.output(pin, GPIO.LOW)
			time.sleep(0.5)
			GPIO.cleanup()

			# Checking if the current relay is running and printing it
			if not GPIO.input(pin):
				return True
			else:
				return False
		else:
			return None


class CameraNormalis(object):

	def __init__(self, midi_name=None):

		# Init Display
		self.lcd = MiniDisplay()

		# Init Controller
		self.controller = AKAI_LPD8_MIDI(device_name=midi_name)

		# Init Radio
		# self.radio = Transmitter()
		radio_state = 'Fail'

		# Welcome message
		if self.lcd.state is True:
			print('Raspberry Pi platform, initializing LCD unit...')
			self.lcd.clear()
			self.lcd.create('CAMERA NORMALIS\n\nControl... {}\nRadio....... {}'.format(
				str(self.controller.state), str(radio_state)))
			print('LCD welcome message sent.')
		else:
			print('Not Raspberry Pi platform, LCD unit initialization failed!')

	def test_midi(self):

		with mido.open_input(self.controller.device_id) as inport:
			# https://mido.readthedocs.io/en/latest/message_types.html
			for msg in inport:
				if msg.is_cc():
					# Volume
					if getattr(msg, 'control'):
						self.lcd.clear()
						self.lcd.create('Knob: {}\nVolume: {}'.format(msg.control, msg.value))
						print('{} | Volume ({}) - {}'.format(msg.type, msg.control, msg.value))
				else:
					if getattr(msg, 'note'):
						self.lcd.clear()
						self.lcd.create('PAD: {}\n' + str(str(msg.note - 35)))
						print('PAD on ({}) - {}'.format(str(msg.note - 35), msg.type))


if __name__ == '__main__':

	r = Relay([18, 17, 15, 14])
	r.self_test(14)
	exit()
	
	app = CameraNormalis(midi_name='LPD8')
	app.test_midi()

