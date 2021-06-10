#!/usr/bin/env python3
# coding=utf-8

import RPi.GPIO as GPIO
from random import randrange
import time


class FourPortRelay(object):

    def __init__(self, pinout):

        # Setting a current GPIO mode
        GPIO.setmode(GPIO.BCM)

        # Removing the warnings
        GPIO.setwarnings(False)

        self.pinout = pinout
        self.pins = list(self.pinout.values())

        print(self.pinout)

        # TODO: what?
        self.test = 'OK'

        GPIO.setup(self.pins, GPIO.OUT)

        self.state = {
             'control1': False,
             'control2': False,
             'power1': False,
             'power2': False
        }

        self.off('control1')
        self.off('control2')
        self.off('power1')
        self.off('power2')

    def self_test(self, delay_time=1):

        """ Test all the relays """
        relay_state = 'OK'

        for pin in self.pinout:
            current_pin = self.pinout[pin]
            GPIO.output(current_pin, GPIO.HIGH)
            time.sleep(delay_time)
            GPIO.output(current_pin, GPIO.LOW)
            time.sleep(delay_time)

            # Checking if the current relay is running and printing it
            # TODO Sound the buzzer in case of a failed relay
            if not GPIO.input(current_pin):
                print('Relay {} on Pin {}: OK'.format(str(pin), current_pin))
            else:
                print('Relay {} on Pin {}: ERROR'.format(str(pin), current_pin))
                relay_state = 'Fail'

    def on(self, relay_name):
        GPIO.output(self.pinout[relay_name], GPIO.HIGH)
        self.state[relay_name] = True

    def off(self, relay_name):
        GPIO.output(self.pinout[relay_name], GPIO.LOW)
        self.state[relay_name] = False

    def flip(self, relay, flip_time):
        """ FLip """
        self.on(relay)
        time.sleep(flip_time)
        self.off(relay)

    def crowd_off(self):
        """ Turn off the MP3 relays """
        self.off('power1')
        time.sleep(1)
        self.off('power2')

    def crowd_on(self):
        """ Turn on the MP3 relays and send the control pulse for auto-playback """

        self.on('power1')
        self.on('power2')

        time.sleep(2)

        self.flip('control1', 0.3)
        self.flip('control2', 0.3)

    @staticmethod
    def shutdown(self):
        """ Turn the board off """
        GPIO.cleanup()
