import RPi.GPIO as GPIO
import time


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

        self.state = {
            1: None,
            2: None,
            3: None,
            4: None
        }

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
            # TODO SOund the buzzer in case of a failed relay
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

    @staticmethod
    def shutdown(self):
        """ Turn the board off """
        GPIO.cleanup()
