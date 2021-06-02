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
		self.pinout = pinout
		self.pins = list(self.pinout.values())

		# setting the mode for all pins so all will be switched on
		GPIO.setup(self.pins, GPIO.OUT)

	def _relay_to_pin(self, pinout):
		""" Convert the config dictionary to pin internal values """
		return

	def self_test(self):

		""" Test all the relays """

		for pin in self.pinout:
			current_pin = self.pinout[pin]
			GPIO.output(current_pin, GPIO.HIGH)
			time.sleep(0.5)
			GPIO.output(current_pin, GPIO.LOW)
			time.sleep(0.5)

			# Checking if the current relay is running and printing it
			if not GPIO.input(current_pin):
				print('Relay {} on Pin {}: OK'.format(str(pin), current_pin))
			else:
				print('Relay {} on Pin {}: ERROR'.format(str(pin), current_pin))


	def on(self, relay):
		GPIO.output(self.pinout[relay], GPIO.HIGH)

	def off(self, relay):
		GPIO.output(self.pinout[relay], GPIO.LOW)

	def shutdown(self):
		""" Turn the board off """
		GPIO.cleanup()


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

	relay_pinout = {
		1: 14,
		2: 15,
		3: 17,
		4: 18
	}

	relay = Relay(relay_pinout)
	relay.self_test()

	time.sleep(1)
	relay.on(1)
	time.sleep(1)
	relay.on(2)
	time.sleep(1)
	relay.on(3)
	time.sleep(1)
	relay.on(4)
	exit()
	app = CameraNormalis(midi_name='LPD8')
	app.test_midi()

