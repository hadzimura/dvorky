#!/usr/bin/env python3
# coding=utf-8

import mido


class AKAI_LPD8_MIDI(object):

    def __init__(self, device_name=None):

        self.device_id = None
        self.state = 'Fail'

        if device_name is None:
            print('MIDI Controller Device Name not specified.')
        elif device_name in mido.get_input_names():
            self.device_id = device_name
            self.state = 'OK'
            print('Found MIDI Controller Device ID: {}'.format(self.device_id))
        else:
            for midi_device in mido.get_input_names():
                if device_name in midi_device:
                    self.device_id = midi_device
                    print('Found MIDI Controller Device ID: {}'.format(self.device_id))
                    self.state = 'OK'
                    break
            if self.device_id is None:
                print('Not found any MIDI Controller Device Name as: {}'.format(device_name))

    def listen(self):

        with mido.open_input(self.device_id) as inport:
            # https://mido.readthedocs.io/en/latest/message_types.html
            for msg in inport:
                return msg
                # if msg.is_cc():
                #     # Volume
                #     if getattr(msg, 'control'):
                #         print('{} | Volume ({}) - {}'.format(msg.type, msg.control, msg.value))
                # else:
                #     if getattr(msg, 'note'):
                #         print('PAD on ({}) - {}'.format(str(msg.note - 35), msg.type))
