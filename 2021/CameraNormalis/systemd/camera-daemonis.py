#!/usr/bin/env python3
# coding=utf-8

""" The SystemD Daemon script """

from gpiozero import LED
from os.path import isfile
from os import kill
from os import system
import signal
import subprocess
import sys
import time
import RPi.GPIO as GPIO


class CameraNormalis(object):

    def __init__(self, cn_folder, cn_script):

        cn_file = '{}/{}'.format(str(cn_folder), str(cn_script))
        self.main_dir = cn_folder

        GPIO.setmode(GPIO.BOARD)

        # Suppress warnings
        GPIO.setwarnings(False)

        # LED diode
        self.red_diode = LED(5)

        # Test if Camera Normalis script is to be found
        if isfile(cn_file) is False:
            # Blink crazily!
            self.red_diode.blink(on_time=0.1, off_time=0.1, n=100)
            time.sleep(10)
            exit(1)

        self.cn_script = cn_file
        self.state = None
        self.cn_pid = None

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
                    self.run('showtime')
                    self.state = True
                elif 0 < time.time() - timer < 3:
                    # Switch was flipped down for less than 3 seconds = run showtime
                    timer = 0
                    self.run('showtime')
                elif 3 < time.time() - timer < 10:
                    # Switch was flipped down for more than 3 seconds and less than 10 seconds = run config
                    timer = 0
                    self.run('tuneup')

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

    def run(self, run_mode):

        """ Manage the running version of Camera Normalis """

        # Kill previous instance if exists
        if self.cn_pid is not None:
            kill(self.cn_pid, signal.SIGTERM)

        # Try fetch the latest Git repository version before running again
        try:
            system('git -C {} pull'.format(self.main_dir))
        except Exception:
            pass

        # Run new instance in the desired mode (showtime|config)
        process = subprocess.Popen([sys.executable,
                                    self.cn_script, '--{}'.format(run_mode)],
                                   stdout=subprocess.PIPE,
                                   stderr=subprocess.PIPE,
                                   shell=False)

        # Get the PID of current instance to be able to kill it during next change
        self.cn_pid = process.pid

    @staticmethod
    def shutdown():
        """ Shutdown the Raspberry Pi """
        # Rather nasty but then again: who cares a lot...?
        system("echo sh4d0w | sudo shutdown now -h")


if __name__ == '__main__':
    app = CameraNormalis(cn_folder='/home/pi/dvorky', cn_script='2021/CameraNormalis/camera-normalis.py')
    app.daemon()
