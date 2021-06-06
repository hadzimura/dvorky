#!/usr/bin/env python3
# coding=utf-8

from Audio import Player
from Controller import AKAI_LPD8_MIDI
from Display import LcdMini
from Relay import FourPortRelay

import argparse
import mido


class CameraNormalis(object):

    def __init__(self, playtime=10, midi=None, relay=None, audio=None, display=None):

        # Set the exhibition cycle time (minutes)
        self.playtime = playtime

        # Init Display
        self.lcd = display

        # Init Relays
        self.relay = relay

        # Init Controller
        self.controller = midi

        # Init Audio subsystem
        self.audio = audio

        # Welcome message
        if self.lcd.state is True:
            print('Raspberry Pi platform, initializing LCD unit...')
            self.lcd.clear()
            self.lcd.create('CAMERA NORMALIS\nControl... {}\nRelays.... {}\nAudio.... {}'.format(
                str(self.controller.test), str(self.relay.test), str(self.audio.count)))
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

    parser = argparse.ArgumentParser()
    parser.add_argument("-c", "--config", help="Enter the configuration mode", default=False, action="store_true")
    parser.add_argument("-s", "--showtime", help="Enter the showtime mode", default=False, action="store_true")
    args = parser.parse_args()

    relay_pinout = {
        1: 14,
        2: 15,
        3: 17,
        4: 18
    }

    playtime = 10

    audio_folder = '../source'

    if args.config is True:
        app = CameraNormalis(playtime=None,
                             midi=AKAI_LPD8_MIDI(device_name='LPD8'),
                             relay=FourPortRelay(relay_pinout, self_test=True),
                             audio=Player(audio_folder, audio_format='mp3'),
                             display=LcdMini())
        app.test_midi()
    elif args.showtime is True:
        app = CameraNormalis(playtime=playtime,
                             midi=AKAI_LPD8_MIDI(device_name='LPD8'),
                             relay=FourPortRelay(relay_pinout, self_test=False),
                             audio=Player(audio_folder, audio_format='mp3'),
                             display=LcdMini())
        app.relay.on(1)
        app.relay.off(2)
        app.relay.on(3)
        app.relay.off(4)
