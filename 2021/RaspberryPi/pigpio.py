#!/usr/bin/env python3
# coding=utf-8

""" This is the main control daemon """

from gpiozero import LED
from os.path import isfile
from os import kill
from os import system
import pigpio
import signal
import subprocess
import sys
import time


class CameraNormalis(object):

    def __init__(self, cn_file):

        if isfile(cn_file) is False:
            print('Main executable not found. Exiting.')
            exit(1)

        self.cn_script = cn_file
        self.state = None
        self.cn_pid = None

        # GPIO.setmode(GPIO.BOARD)

        self.red_diode = LED(5)
        self.red_diode.blink(on_time=0.6, off_time=0.6, n=5)
        time.sleep(10)
        exit()

        # GPIO.setup(10, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
        # Switch UP
        # TODO

        # Switch DOWN
        # TODO

        # LED diode
        self.red_diode = LED(5)
        # pi = pigpio.pi()
        # pi.set_mode(5, pigpio.OUTPUT)

    def daemon(self):

        """ Run this in the background """

        timer = 0
        a = 0
        mode_set = None

        # Main endless loop
        while True:

            # Switch down
            if a == 1:

                if timer == 0:
                    timer = time.time()
                    # Diode turned off – first blink it for 3 seconds rapidly...
                    self.red_diode.blink(on_time=0.3, off_time=0.3)
                    mode_set = 'showtime'

                if 3 < time.time() - timer < 10 and mode_set == 'showtime':
                    # Diode blinked for 3 seconds – secondly blink it for 7 seconds slowly...
                    self.red_diode.blink(on_time=0.6, off_time=0.6)
                    mode_set = 'config'

                if time.time() - timer > 10:
                    # Initiate shutdown sequence

                    # Blink the diode for another 10 secs slowly then turn it off (to make a statement)
                    self.red_diode.blink(on_time=1, off_time=1, n=10)
                    self.shutdown()

            # Switch up
            if a == 2:

                if self.state is None:
                    # Never started = run Camera Normalis
                    self.run()
                    self.state = True
                elif 0 < timer < 3:
                    # Switch was flipped down for less than 3 seconds = run showtime
                    self.run()
                elif 3 < timer < 10:
                    # Switch was flipped down for more than 3 seconds and less than 10 seconds = run config
                    self.run('config')

                # Reset the timer
                timer = 0

    def run(self, run_mode=None):

        """ Manage the running version of Camera Normalis """

        # Kill previous instance if exists
        if self.cn_pid is not None:
            kill(self.cn_pid, signal.SIGTERM)

        # Run new instance in the desired mode (showtime|config)
        process = subprocess.Popen([sys.executable,
                                    self.cn_script, run_mode],
                                   stdout=subprocess.PIPE,
                                   stderr=subprocess.STDOUT,
                                   shell=False)

        # Store the current running instance PID
        self.cn_pid = process.pid

    @staticmethod
    def shutdown(self):

        """ Shutdown the Raspberry Pi """

        system("shutdown now -h")


if __name__ == '__main__':
    app = CameraNormalis('/home/pi/dvorky/2021/RaspberryPi/camera_normalis.py')
    app.daemon()

# pi.write(5, True)
# time.sleep(0.5)
# pi.write(5, False)
# time.sleep(0.5)
