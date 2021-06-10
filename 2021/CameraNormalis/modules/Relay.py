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

        # self.on('control1')
        # self.on('control2')
        # self.off('power1')
        # self.off('power2')

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

    def power_on(self, relay_name):
        # print('pon - start', relay_name, self.state[relay_name])
        if self.state[relay_name] is False:
            GPIO.output(self.pinout[relay_name], GPIO.LOW)
            self.state[relay_name] = True
        # print('pon - end', relay_name, self.state[relay_name])

    def power_off(self, relay_name):
        # print('pof - start', relay_name, self.state[relay_name])
        if self.state[relay_name] is True:
            GPIO.output(self.pinout[relay_name], GPIO.HIGH)
            self.state[relay_name] = False
        # print('pof - end', relay_name, self.state[relay_name])

    def control_on(self, control_name):
        if self.state[control_name] is False:
            GPIO.output(self.pinout[control_name], GPIO.HIGH)
            self.state[control_name] = True

    def control_off(self, control_name):
        if self.state[control_name] is True:
            GPIO.output(self.pinout[control_name], GPIO.LOW)
            self.state[control_name] = False

    def on(self, relay_name):
        GPIO.output(self.pinout[relay_name], GPIO.HIGH)
        self.state[relay_name] = True
        print('on', self.state)

    def off(self, relay_name):
        GPIO.output(self.pinout[relay_name], GPIO.LOW)
        self.state[relay_name] = False
        print('off', self.state)

    def flip(self, relay, flip_time):
        """ FLip """
        print('Flip on {}'.format(relay))
        self.on(relay)
        time.sleep(1)
        print('Flip off {}'.format(relay))
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

        self.flip('control1', 0.7)
        # time.sleep(1)
        self.flip('control2', 0.7)

    @staticmethod
    def shutdown(self):
        """ Turn the board off """
        GPIO.cleanup()
