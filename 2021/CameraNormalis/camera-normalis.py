#!/usr/bin/env python3
# coding=utf-8

from modules.Audio import Player
from modules.Controller import AKAI_LPD8_MIDI
from modules.Display import LcdMini
from modules.Relay import FourPortRelay

import argparse
from json import load
import mido


class CameraNormalis(object):

    # def __init__(self, playtime=10, midi=None, relay=None, audio=None, display=None):
    def __init__(self, cn_config, runtime_mode):

        # Set the exhibition cycle time (minutes)
        self.playtime = cn_config['playtime']

        self.runtime_mode = runtime_mode

        # Init Audio Player
        self.audio = Player(audio_path=cn_config['audio_files'], audio_format=cn_config['audio_format'])

        # MacOS specific exception (do not init HW modules)
        if self.runtime_mode != 'macos':

            # Init LCD Display
            self.lcd = LcdMini()

            # Init 4 Port Relay
            self.relay = FourPortRelay(cn_config['relays'])

        # Runtime mode specific initializations
        if self.runtime_mode == 'tuneup':

            # Init MIDI Controller
            self.controller = AKAI_LPD8_MIDI(device_name=cn_config['midi_device'])

        # All set, display LCD Welcome Message
        if self.runtime_mode != 'macos':
            try:
                if self.lcd.state is True:
                    self.lcd.clear()
                    self.lcd.create('CAMERA NORMALIS\nControl... {}\nRelays.... {}\nAudio.... {}'.format(
                        str(self.controller.test), str(self.relay.test), str(self.audio.count)))
                else:
                    # LCD init failed, who cares?
                    pass
            except Exception:
                pass

    def run(self):
        """ Execute the Main Camera Normalis Loop based on the selected runtime mode """
        if self.runtime_mode == 'showtime':
            self.audio.showtime()
        elif self.runtime_mode == 'tuneup':
            self.audio.self_test()
            exit()
            self.configuration()
            # TODO: What next?
        elif self.runtime_mode == 'macos':
            self.audio.list()
            self.audio.self_test()

    def configuration(self):
        """ Test various functionalities and allow user to change configuration parameters(?) """

        # If controller was not found, perform basic functionality checks
        if self.controller.state is False:

            # Test relays on/off state
            self.relay.self_test(delay_time=1)

            # Test audio player
            # self.audio.self_test()

            return None

        # Main MIDI controller loop for input actions
        with mido.open_input(self.controller.device_id) as inport:
            # https://mido.readthedocs.io/en/latest/message_types.html
            for message in inport:
                # Input mode on controller is set to "CC" – control_change
                if message.is_cc():
                    # Volume
                    if getattr(msg, 'control'):
                        self.lcd.clear()
                        self.lcd.create('Knob: {}\nVolume: {}'.format(msg.control, msg.value))
                        print('{} | Volume ({}) - {}'.format(msg.type, msg.control, msg.value))
                elif message.is_meta:
                    pass
                elif message.is_realtime:
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

    # Parse incoming parameters
    parser = argparse.ArgumentParser()

    parser.add_argument("-c",
                        "--config",
                        help="Specify config file to be used.",
                        type=str,
                        default='camera-normalis.json',
                        dest='cn_config_file')
    parser.add_argument("-m",
                        "--macos",
                        help="On MacOSX there is no GPIO... :)",
                        default=False,
                        action="store_true")
    parser.add_argument("-s",
                        "--showtime",
                        help="Run Camera Normalis in the showtime mode.",
                        default=False,
                        action="store_true")
    parser.add_argument("-t",
                        "--tuneup",
                        help="Run Camera Normalis in the tuneup mode.",
                        default=False,
                        action="store_true")

    args = parser.parse_args()

    # Load configuration file
    with open(args.cn_config_file) as configuration_file:
        cn_configuration = load(configuration_file)

    set_mode = None
    if args.macos is True:
        set_mode = 'macos'
    elif args.showtime is True:
        set_mode = 'showtime'
    elif args.tuneup is True:
        set_mode = 'tuneup'
    else:
        print('Mode undefined! Exiting...')
        exit(1)

    # Initialize Camera Normalis application
    app = CameraNormalis(cn_configuration, set_mode)

    # Run specified mode
    app.run()

    # if args.config is True:
    #     # Run in the CONFIG mode
    #     app = CameraNormalis(playtime=None,
    #                          midi=AKAI_LPD8_MIDI(device_name='LPD8'),
    #                          relay=FourPortRelay(relay_pinout, self_test=True),
    #                          audio=Player(audio_folder, audio_format='mp3'),
    #                          display=LcdMini())
    #     app.test_midi()
    # elif args.showtime is True:
    #     # Run in the SHOWTIME mode
    #     app = CameraNormalis(playtime=playtime,
    #                          midi=AKAI_LPD8_MIDI(device_name='LPD8'),
    #                          relay=FourPortRelay(relay_pinout, self_test=False),
    #                          audio=Player(audio_folder, audio_format='mp3'),
    #                          display=LcdMini())
    #     app.relay.on(1)
    #     app.relay.off(2)
    #     app.relay.on(3)
    #     app.relay.off(4)
    #     while True:
    #         pass
