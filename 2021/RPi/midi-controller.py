#!/usr/bin/env python3
# coding=utf-8

import mido
from sys import stdout

print('Controller: {}'.format(mido.get_input_names()))

events = [
    'program_change',
    'control_change',
    'channel',
    'program',
    'time'
    'control',
    'value'
]

pads_cc = [
    'control_change',
    'channel',
    'control',
    'value',
    'time'
]

pads_pc = [
    'program_change',
    'channel',
    'program',
    'time'
]

pads_pad = [
    'note_on',
    'note_off',
    'channel',
    'note',
    'velocity',
    'time'
]

knobs = [
    'control_change',
    'channel',
    'control',
    'value',
    'time'
]

with mido.open_input('LPD8') as inport:
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
