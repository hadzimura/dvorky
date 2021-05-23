#!/usr/bin/env python3
# coding=utf-8

from Display import MiniDisplay
from Controller import AKAI_LPD8
import mido
import time


class CameraNormalis(object):

	def __init__(self, midi_device=None):

		# Init Display
		self.lcd = MiniDisplay()

		# Init Controller
		self.controller = AKAI_LPD8(device_id=midi_device)

		# Init Radio
		# self.radio = Transmitter()
		radio_state = 'Fail'

		# Welcome message
		if self.lcd.state is True:
			self.lcd.clear()
			self.lcd.create('CAMERA NORMALIS\n\nControl... {}\nRadio....... {}'.format(
				str(self.controller.state()), str(radio_state)))
		else:
			print('Not Raspberry Pi platform, LCD init Failed!')

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

	# Configuration
	# cfg = Config(basename(__file__),
	#              configs_path=getenv('pfl_cfg_connectors'),
	#              apps_path=getenv('pfl_cfg_apps'),
	#              parameters=runtime_arg)
	
	# app = CameraNormalis(midi_device='LPD8:LPD8 MIDI 1 20:0')
	app = CameraNormalis(midi_device='LPD8:LPD8 MIDI 1 24:0')
	# app.test_display()
	app.test_midi()

