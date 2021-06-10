#!/usr/bin/env python3
# coding=utf-8
import time

from modules.Audio import Player
from modules.Controller import AKAI_LPD8_MIDI
# from modules.Display import LcdMini
from modules.Relay import FourPortRelay

import argparse
from json import load
import mido
from random import randrange


class CameraNormalis(object):

    def __init__(self, cn_config, runtime_mode):

        self.cfg = cn_config
        self.cfg_show = cn_config['showtime']
        self.cfg_audio = cn_config['audio']

        # Set the exhibition cycle time (recalculate minutes to secs first)
        self.total_time = self.cfg_show['total_time'] * 60

        self.runtime_mode = runtime_mode

        # Init Audio Player
        self.audio = Player(audio_path=self.cfg_audio['path'],
                            audio_format=self.cfg_audio['format'])

        # MacOS specific exception (do not init HW modules)
        if self.runtime_mode != 'macos':

            # Init LCD Display
            # self.lcd = LcdMini()

            # Init 4 Port Relay
            self.relay = FourPortRelay(self.cfg['relays'])

        # Runtime mode specific initializations
        if self.runtime_mode == 'tuneup':

            # Init MIDI Controller
            self.controller = AKAI_LPD8_MIDI(device_name=self.cfg['midi_device'])

        # All set, display LCD Welcome Message
        # if self.runtime_mode != 'macos':
        #     try:
        #         if self.lcd.state is True:
        #             self.lcd.clear()
        #             self.lcd.create('CAMERA NORMALIS\nControl... {}\nRelays.... {}\nAudio.... {}'.format(
        #                 str(self.controller.test), str(self.relay.test), str(self.audio.count)))
        #         else:
        #             # LCD init failed, who cares?
        #             pass
        #     except Exception:
        #         pass

    def run(self):
        """ Execute the Main Camera Normalis Loop based on the selected runtime mode """
        if self.runtime_mode == 'showtime':

            # True Showtime Main Endless Loop is here
            while True:

                self.relay.on('power1')
                self.relay.on('power2')
                self.relay.on('control1')
                self.relay.on('control2')

                self.relay.crowd_on()
                # Play the crowds (custom samples handled inside the class)
                self.audio.partytime(self.total_time,
                                     scene_probability=self.cfg_show['scene_probability'],
                                     volume_change_period=self.cfg_show['volume_change_period'])

                #self.relay.off('power1')
                #self.relay.off('power2')

                # Play the speech announcement
                # self.audio.announce()

                # TODO: ...and shut the Arduino crowd
                # self.relay.crowd_control(total_time=self.cfg_show['crowd_control_fadeout'])

                # Crowd was hushed: play the speech
                self.audio.speech()

                # Play the Clap Your Hands outro
                # self.audio.clap_your_hands()

                # Moment for the inner peace
                time.sleep(self.cfg_show['end_silence'])

                # ...rinse and repeat :)

        elif self.runtime_mode == 'tuneup':
            # self.configuration()

            self.relay.crowd_on()
            time.sleep(5)
            self.relay.crowd_off()
            time.sleep(5)
            self.relay.crowd_on()
            time.sleep(5)
            self.relay.crowd_off()
            exit()
            self.player_switch.on()
            time.sleep(1)
            self.player_switch.off()
            exit()
            while True:
                self.audio.speech()

            # TODO: What next?
        elif self.runtime_mode == 'macos':
            # True Showtime Main Endless Loop is here
            while True:

                # Play the crowds (custom samples handled inside the class)
                self.audio.partytime(self.total_time)

                # Play the speech announcement
                # self.audio.play_track(self.audio.get_track('announce'))

                # ...and shut the Arduino crowd
                self.relay.crowd_control(total_time=4)

                # Crowd was hushed: play the speech
                self.audio.play_track(self.audio.get_track('speech'))

                # Wait for it to end...
                self.audio.wait_for_end_of_track()

                # Moment for the inner peace
                time.sleep(3)

                # ...rinse and repeat :)
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
                print(message)
                # Input mode on controller is set to "CC" – control_change
                if message.is_cc():
                    # Volume
                    if getattr(message, 'control'):
                        pass
                        # print('{} | Volume ({}) - {}'.format(msg.type, msg.control, msg.value))
                elif message.is_meta:
                    pass
                else:
                    if getattr(message, 'note'):
                        if message.note == 36:
                            relay = 'control1'
                        elif message.note == 37:
                            relay = 'control2'
                        elif message.note == 38:
                            relay = 'power1'
                        elif message.note == 39:
                            relay = 'power2'
                        # relay = message.note - 35

                        if message.type == 'note_on':
                            if self.relay.state[relay] is True:
                                self.relay.off(relay)
                            elif self.relay.state[relay] is False:
                                self.relay.on(relay)


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

    cn_path = '/home/pi/dvorky/2021/CameraNormalis'

    # Load configuration file
    with open('{}/{}'.format(cn_path, args.cn_config_file)) as configuration_file:
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
