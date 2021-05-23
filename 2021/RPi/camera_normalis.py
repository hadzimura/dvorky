#!/usr/bin/env python3
# coding=utf-8

from Display import MiniDisplay
from Controller import AKAI_LPD8
import time

class CameraNormalis(object):

	def __init__(self, midi_device=None):

		self.lcd = MiniDisplay()
		self.controller = AKAI_LPD8(device_id=midi_device)

	def test_display(self):
		a = 1
		while True:
			self.lcd.clear()
			# self.lcd.create('PAD: 1\n' + str(a), line=1, color=128)
			self.lcd.create('PAD: 1\n' + str(a))
			a += 1
			time.sleep(.1)

	def test_midi(self):
		pass


if __name__ == '__main__':

	# Configuration
	# cfg = Config(basename(__file__),
	#              configs_path=getenv('pfl_cfg_connectors'),
	#              apps_path=getenv('pfl_cfg_apps'),
	#              parameters=runtime_arg)
	
	app = CameraNormalis(midi_device='LPD8:LPD8 MIDI 1 20:0')
	app.test_display()
