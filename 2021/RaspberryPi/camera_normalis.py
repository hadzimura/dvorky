#!/usr/bin/env python3
# coding=utf-8

from Controller import AKAI_LPD8_MIDI
from Display import MiniDisplay
from glob import glob
import mido
import RPi.GPIO as GPIO
import time


class Samples(object):

    def __init__(self, audio_path=None):
        files = glob(audio_path + '*.wav')
        print(files)


class Relay(object):

    def __init__(self, pinout):

        # Setting a current GPIO mode
        GPIO.setmode(GPIO.BCM)

        # Removing the warnings
        GPIO.setwarnings(False)

        self.pinout = pinout
        self.pins = list(self.pinout.values())

        GPIO.setup(self.pins, GPIO.OUT)

        self.test = self.self_test()

        self.state = {
            1: None,
            2: None,
            3: None,
            4: None
        }

    def self_test(self):

        """ Test all the relays """
        relay_state = 'OK'
        for pin in self.pinout:
            current_pin = self.pinout[pin]
            GPIO.output(current_pin, GPIO.HIGH)
            time.sleep(0.5)
            GPIO.output(current_pin, GPIO.LOW)
            time.sleep(0.5)

            # Checking if the current relay is running and printing it
            if not GPIO.input(current_pin):
                print('Relay {} on Pin {}: OK'.format(str(pin), current_pin))
            else:
                print('Relay {} on Pin {}: ERROR'.format(str(pin), current_pin))
                relay_state = 'Fail'
        return relay_state

    def on(self, relay_number):
        GPIO.output(self.pinout[relay_number], GPIO.HIGH)
        self.state[relay_number] = True

    def off(self, relay_number):
        GPIO.output(self.pinout[relay_number], GPIO.LOW)
        self.state[relay_number] = False

    @staticmethod
    def shutdown(self):
        """ Turn the board off """
        GPIO.cleanup()


class CameraNormalis(object):

    def __init__(self, midi_name=None, relays=None, samples=None):

        # Init Display
        self.lcd = MiniDisplay()

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

    audio_folder = '../source/'

    app = CameraNormalis(midi_name='LPD8',
                         relays=Relay(relay_pinout),
                         samples=Samples(audio_folder))
    app.test_midi()
