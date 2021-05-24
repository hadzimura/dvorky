#!/usr/bin/env python3
# coding=utf-8

from Display import MiniDisplay
from Controller import AKAI_LPD8_MIDI
import mido
import time


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
		else:
			print('Not Raspberry Pi platform, LCD unit initialization failed!')

	def test_display(self):
		a = 1
		while True:
			self.lcd.clear()
			# self.lcd.create('PAD: 1\n' + str(a), line=1, color=128)
			self.lcd.create('PAD: 1\n' + str(a))
			a += 1
			time.sleep(.1)

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

	app = CameraNormalis(midi_name='LPD8')
	# app.test_display()
	app.test_midi()

