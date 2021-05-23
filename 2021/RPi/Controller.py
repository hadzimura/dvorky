#!/usr/bin/env python3
# coding=utf-8

import mido


class AKAI_LPD8(object):

    def __init__(self, device_id=None):

        self.device_id = None
        if device_id in mido.get_input_names():
            self.device_id = device_id
            print('Found MIDI Controller Device ID: {}'.format(device_id))
        else:
            print('Not Found MIDI Controller Device ID: {}'.format(device_id))
            try:
                print('Available Device ID(s):')
                for midi_device in mido.get_input_names():
                    print(' * {}'.format(str(midi_device)))
            except Exception as error:
                print('MIDI Controller error: {}'.format(str(error)))

    def state(self):
        if self.device_id is None:
            return 'Fail'
        else:
            return 'OK'

    def listen(self):

        with mido.open_input(self.device_id) as inport:
            # https://mido.readthedocs.io/en/latest/message_types.html
            for msg in inport:
                if msg.is_cc():
                    # Control Message

                    # Volume
                    if getattr(msg, 'control'):
                        print('{} | Volume ({}) - {}'.format(msg.type, msg.control, msg.value))
                else:

                    if getattr(msg, 'note'):
                        print('PAD on ({}) - {}'.format(str(msg.note - 35), msg.type))
