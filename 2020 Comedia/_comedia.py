#!/usr/bin/env python3

import RPi.GPIO as GPIO
# from gpiozero import LED
from gpiozero import Button
import os
import sys
import time
from subprocess import Popen

# There are two ways of numbering the IO pins on a Raspberry Pi within RPi.GPIO.
# The first is using the BOARD numbering system. This refers to the pin numbers on the P1 header of the Raspberry Pi
# board. The advantage of using this numbering system is that your hardware will always work, regardless of the board
# revision of the RPi. You will not need to rewire your connector or change your code.
# The second numbering system is the BCM numbers. This is a lower level way of working - it refers to the channel
# numbers on the Broadcom SOC. You have to always work with a diagram of which channel number goes to which pin
# on the RPi board. Your script could break between revisions of Raspberry Pi boards.

# Docs: https://sourceforge.net/p/raspberry-gpio-python/wiki/Inputs/
# You need to set up every channel you are using as an input or an output. To configure a channel as an input:


class Comedia(object):

    """ The main Comedia """
    def __init__(self, video_file):

        # self.video_file = video_file
        self.player_state = None
        self.error_message = None
        self.light_state = None

        # https://github.com/popcornmix/omxplayer/
        self.play_me = ['omxplayer', '-b', '--loop', '--no-osd', '-o', 'local', video_file]

        # Setup the PINs
        # self.led_switch = LED("GPIO17")

        self.led_out = 17

        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.led_out, GPIO.OUT)

    def switch_light(self):

        if self.light_state is None:
            GPIO.output(self.led_out, GPIO.HIGH)
            self.light_state = True
            print(self.light_state)

        elif self.light_state is True:
            GPIO.output(self.led_out, GPIO.LOW)
            self.light_state = False
            print(self.light_state)

        elif self.light_state is False:
            GPIO.output(self.led_out, GPIO.HIGH)
            self.light_state = True
            print(self.light_state)

    def play(self):

        if self.player_state is None:

            # Not playing, try to start
            try:
                os.system('killall omxplayer.bin')
                Popen(self.play_me)
                self.player_state = True

            except Exception as error:

                self.error_message = error

        elif self.player_state is True:

            # Playing, try to stop
            try:

                os.system('killall omxplayer.bin')
                self.player_state = False

            except Exception as error:

                self.player_state = None
                self.error_message = error

        elif self.player_state is False:

            # Stopped, try to start
            try:

                os.system('killall omxplayer.bin')
                Popen(self.play_me)
                self.player_state = True

            except Exception as error:

                self.error_message = error


class LetsPlayButton(object):
    pass


class LetsPlayButtonLights(object):
    pass


class Introduzzione(object):
    pass


class LaFinita(object):
    pass


class ComediaMustGoOn(object):

    # Define all video files
    intro = Introduzzione('/home/pi/comedia/intro.mp4')
    comedia = Comedia('/home/pi/Desktop/TTv1.mp4')
    outro = LaFinita('/home/pi/comedia/outro.mp4')

    # Define action(s)
    godot = LetsPlayButton()

    # button = Button("GPIO17")

    # Start the endless loop
    while True:

        # 0 Boot the button
        godot.boot()

        # 1 When Booted Up, the looped intro video shows up (automatically plays on the background)
        intro.play()

        # 2 Start sequence begins monitoring of the button, glowing it at the same time
        while godot.touched() is False:
            godot.waiting()
            # (Dont forget to put button into SOME state)

        # 3 When we detect te button interaction, we are about to start Comedia:
        # But we first flash the "Comedia" button onscreen
        intro.stop()

        # 4 We run Comedia and monitor the state of the button(!)
        comedia.play()

        # 5 Fade to black
        comedia.stop()

        # 6 let the room dark for 10 seconds
        godot.darkroom()



if __name__ == "__main__":
    ComediaMustGoOn()

