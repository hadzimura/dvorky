#!/usr/bin/env python3

import os
from subprocess import Popen
from subprocess import call
import RPi.GPIO as GPIO
from gpiozero import LED



class GardenOfTheDay(object):

    """ OMXPlayer: https://github.com/popcornmix/omxplayer/ """

    def __init__(self, video):

        self.play_loop = ['omxplayer', '-r', '-b', '--aspect-mode', 'fill', '--no-osd', '--loop', '-o', 'local', video]
        self.play_once = ['omxplayer', '-r', '-b', '--aspect-mode', 'fill', '--no-osd', '-o', 'local', video]
        self.kill = 'killall -s 9 omxplayer.bin > /dev/null 2>&1'


        GPIO.setmode(GPIO.BOARD)

        # Suppress warnings
        GPIO.setwarnings(False)

        # LED diode
        self.red_diode = LED(5)

        # Define front plate switch pins
        self.switch_up = 31
        self.switch_down = 33

        # Setup the initial pins values
        GPIO.setup(self.switch_up, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
        GPIO.setup(self.switch_down, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

    def daemon(self):

        """ Run this in the background """

        timer = 0
        mode_set = None

        # Main endless loop
        while True:

            # Switch is UP
            if GPIO.input(self.switch_up) == GPIO.HIGH:

                # Light the diode (stop blinking)
                self.red_diode.on()

                if self.state is None:
                    # Never started = run Camera Normalis
                    timer = 0
                    self.run('s')
                    self.state = True
                elif 0 < time.time() - timer < 3:
                    # Switch was flipped down for less than 3 seconds = run showtime
                    timer = 0
                    self.run('s')
                elif 3 < time.time() - timer < 10:
                    # Switch was flipped down for more than 3 seconds and less than 10 seconds = run config
                    timer = 0
                    self.run('t')

            # Switch is DOWN
            if GPIO.input(self.switch_down) == GPIO.HIGH:

                if timer == 0:
                    # Diode turned off – first blink it for 3 seconds rapidly...
                    timer = time.time()
                    self.red_diode.blink(on_time=0.25, off_time=0.25, n=12)
                    mode_set = 'showtime'

                if 3 < time.time() - timer < 10 and mode_set == 'showtime':
                    # Diode blinked for 3 seconds – secondly blink it for 7 seconds slowly...
                    self.red_diode.blink(on_time=0.5, off_time=0.5, n=14)
                    mode_set = 'tuneup'

                if time.time() - timer > 10:
                    # Initiate shutdown sequence
                    # Blink the diode for another 10 secs slowly then turn it off (to make a statement)
                    self.red_diode.blink(on_time=0.1, off_time=0.1, n=30)
                    time.sleep(3)
                    self.shutdown()


    def kill(self):
        os.system(self.kill)

    def play(self, mode='looped', style='foreground'):

        play_me = None
        if mode == 'once':
            play_me = self.play_once
        elif mode == 'looped':
            play_me = self.play_loop

        if style == 'foreground':
            call(play_me)
        elif style == 'background':
            Popen(play_me)


if __name__ == "__main__":

    show = GardenOfTheDay('/home/pi/Garden/Banner.mp4')
