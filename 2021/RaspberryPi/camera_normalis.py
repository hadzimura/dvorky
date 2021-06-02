#!/usr/bin/env python3
# coding=utf-8

from Audio import Samples
from Controller import AKAI_LPD8_MIDI
from Display import LcdMini
from Relay import FourPortRelay

import mido


class CameraNormalis(object):

    def __init__(self, midi=None, relays=None, samples=None, display=None):

        # Init Display
        self.lcd = display

        # Init Relays
        self.relay = relays

        # Init Controller
        self.controller = AKAI_LPD8_MIDI(device_name=midi_name)

        # Welcome message
        if self.lcd.state is True:
            print('Raspberry Pi platform, initializing LCD unit...')
            self.lcd.clear()
            self.lcd.create('CAMERA NORMALIS\n\nControl... {}\nRelays.... {}'.format(
                str(self.controller.test), str(self.relay.test)))
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

                        relay = msg.note - 35

                        if msg.type == 'note_on':
                            if self.relay.state[relay] is None:
                                self.relay.on(relay)
                            elif self.relay.state[relay] is True:
                                self.relay.off(relay)
                            elif self.relay.state[relay] is False:
                                self.relay.on(relay)

                        self.lcd.clear()
                        self.lcd.create('Relay: {}\n' + str(relay))
                        print('Relay on ({}) - {}'.format(str(msg.note - 35), msg.type))


if __name__ == '__main__':
    relay_pinout = {
        1: 14,
        2: 15,
        3: 17,
        4: 18
    }

    audio_folder = '../source'

    app = CameraNormalis(midi_name='LPD8',
                         relays=FourPortRelay(relay_pinout, self_test=False),
                         samples=Samples(audio_folder),
                         display=LcdMini())
    app.test_midi()
