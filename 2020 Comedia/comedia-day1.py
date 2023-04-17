#!/usr/bin/env python3
import RPi.GPIO as GPIO
from gpiozero import PWMLED
from gpiozero import Button
# from gpiozero import LED

import os
import sys
import time
from subprocess import Popen
from time import sleep


# There are two ways of numbering the IO pins on a Raspberry Pi within RPi.GPIO.
# The first is using the BOARD numbering system. This refers to the pin numbers on the P1 header of the Raspberry Pi
# board. The advantage of using this numbering system is that your hardware will always work, regardless of the board
# revision of the RPi. You will not need to rewire your connector or change your code.
# The second numbering system is the BCM numbers. This is a lower level way of working - it refers to the channel
# numbers on the Broadcom SOC. You have to always work with a diagram of which channel number goes to which pin
# on the RPi board. Your script could break between revisions of Raspberry Pi boards.

# Docs: https://sourceforge.net/p/raspberry-gpio-python/wiki/Inputs/
# You need to set up every channel you are using as an input or an output. To configure a channel as an input:

class Choreography(object):
    def __init__(self):
        self.dancers= {
            'Godard': {'RedButton': 17,
                       'RedLight': 27},
            'Dante': {'MainFeature': '/home/pi/Comedia/test/FullHD_CBR_15_contrast.mp4'}
        }

class Comedia(object):

    """ The main Comedia """
    def __init__(self, video_file, loop=False):

        self.player_state = None
        self.error_message = None
        self.light_state = None

        if loop is True:
            self.play_me = ['omxplayer', '--loop', '--no-osd', '-o', 'local', video_file]
        else:
            self.play_me = ['omxplayer', '--no-osd', '-o', 'local', video_file]
        # https://github.com/popcornmix/omxplayer/
        # self.play_me = ['omxplayer', '-b', '--loop', '--no-osd', '-o', 'local', video_file]
        # self.play_me = ['omxplayer', '--no-osd', '-o', 'local', video_file]

        # Setup the PINs
        # self.led_switch = LED("GPIO17")

        # self.led_out = 17

        # GPIO.setmode(GPIO.BCM)
        # GPIO.setup(self.led_out, GPIO.OUT)

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

    def stop(self):
        os.system('killall omxplayer.bin')

    def play(self):

        if self.player_state is None:

            # Not playing, try to start
            try:
                os.system('killall omxplayer.bin')
            except Exception as error:
                self.error_message = error

            Popen(self.play_me)
            self.player_state = True

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
                # Popen(self.play_me, stdout=subprocess.PIPE)
            except Exception as error:

                self.error_message = error
            Popen(self.play_me)
            self.player_state = True


class Misanscene(object):

    def __init__(self, play, cfg):

        self.cfg = cfg.dancers[play]

        # Button(cfg.buttons[where_you_want_it])
        # self.leds = PWMLED(cfg.leds[where_you_want_it], frequency=1000)
        # Seconds of button boot
        self.boot_time = 1
        self.boot_step = 5000

    def boot(self):
        # Turn it off
        self.leds.value = 0
        sleep(2)

        self.leds.blink(on_time=0, off_time=0, fade_in_time=10, fade_out_time=0, n=1, background=False)

    def lights_off(self, which=None):
        self.leds.value = 0



class ShowMustGoOn(object):

    # cfg = Config()
    print('SMGO')
    # Define action(s)
    # godard = Misanscene('Godard', cfg)
    # godot = Misanscene('Godot', cfg)
    # dante = Misanscene('Dante', cfg)
    button1 = Button(17)
    led1 = PWMLED(27)
    # dante = Comedia('/home/pi/Comedia/test/FullHD_CBR_15_contrast.mp4')
    # intro = Comedia('/home/pi/Comedia/intro.mp4', loop=True)
    # led1.blink(on_time=0, off_time=0, fade_in_time=2, fade_out_time=0, n=10, background=False)

    # Popen(['omxplayer', '--loop', '--no-osd', '-o', 'local', '/home/pi/Comedia/intro.mp4'])
    # Popen(['omxplayer', '--no-osd', '-o', 'local', '/home/pi/Comedia/intro.mp4'])
    # intro.play()
    Popen(['omxplayer', '--loop', '--aspect-mode', 'fill', '--no-osd', '-o', 'local', '/home/pi/Comedia/intro.mp4'])
    led1.blink(on_time=0.5, off_time=0.5, fade_in_time=1, fade_out_time=1)

    while button1.value == 0:
        pass
    os.system('killall -s 9 omxplayer.bin')
    # Popen(['omxplayer', '-i', '/home/pi/Comedia/intro.mp4'])
    # intro.stop()
    led1.off()
    Popen(['omxplayer', '--aspect-mode', 'fill', '--no-osd', '-o', 'local', '/home/pi/Comedia/test/FullHD_CBR_15_contrast.mp4'])
    # Popen(['omxplayer', '--no-osd', '-o', 'local', '/home/pi/Comedia/ComediaTest.mp4'])
    exit()


if __name__ == "__main__":
    ShowMustGoOn()