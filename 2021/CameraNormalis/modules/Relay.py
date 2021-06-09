#!/usr/bin/env python3
# coding=utf-8

import RPi.GPIO as GPIO
from random import randrange
import time


class SinglePortRelay(object):

    def __init__(self):

        # Setting a current GPIO mode
        GPIO.setmode(GPIO.BCM)

        # Removing the warnings
        GPIO.setwarnings(False)

        self.pin = 5


        # TODO: what?
        self.test = 'OK'

        GPIO.setup(self.pin, GPIO.OUT)

        print('aaa')
        GPIO.output(self.pin, GPIO.HIGH)
        time.sleep(1)
        GPIO.output(self.pin, GPIO.LOW)
        time.sleep(1)
        GPIO.output(self.pin, GPIO.HIGH)
        time.sleep(1)
        GPIO.output(self.pin, GPIO.LOW)
        time.sleep(1)
        GPIO.output(self.pin, GPIO.HIGH)
        time.sleep(1)
        GPIO.output(self.pin, GPIO.LOW)
        time.sleep(1)

        self.state = None
        # self.state = {
        #     1: self.off(1),
        #     2: self.off(2),
        #     3: self.off(3),
        #     4: self.off(4)
        # }

    def on(self):
        GPIO.output(self.pin, GPIO.HIGH)
        self.state = True

    def off(self):
        GPIO.output(self.pin, GPIO.LOW)
        self.state = False



class FourPortRelay(object):

    def __init__(self, pinout):

        # Setting a current GPIO mode
        GPIO.setmode(GPIO.BCM)

        # Removing the warnings
        GPIO.setwarnings(False)

        self.pinout = pinout
        self.pins = list(self.pinout.values())

        # TODO: what?
        self.test = 'OK'

        GPIO.setup(self.pins, GPIO.OUT)

        # self.state = {
        #     1: self.off(1),
        #     2: self.off(2),
        #     3: self.off(3),
        #     4: self.off(4)
        # }

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

    def on(self, relay_number):
        GPIO.output(self.pinout[relay_number], GPIO.HIGH)
        self.state[relay_number] = True

    def off(self, relay_number):
        GPIO.output(self.pinout[relay_number], GPIO.LOW)
        self.state[relay_number] = False

    def crowd_control(self, total_time=4):
        """ Shut the relays randomly over fixed timespan (should be 4 seconds) """
        wait_time = total_time / len(self.state)
        all_clear = False

        while all_clear is False:
            test_state = randrange(1, 4, 1)
            if self.state[test_state] is True:
                self.off(test_state)
                time.sleep(wait_time)
        return None

    @staticmethod
    def shutdown(self):
        """ Turn the board off """
        GPIO.cleanup()
