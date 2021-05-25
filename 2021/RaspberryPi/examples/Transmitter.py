# NRF24L01
from lib_nrf24 import NRF24
import RPi.GPIO as GPIO
import spidev

# General imports
from sys import stdout
import time


class Transmitter(object):
    """ The nRF24L01 RF Module
    The module has on operating voltage from 1.9V to 3.6V (typically 3.3V) and consumes very less current
    of only 12mA during normal operation which makes it battery efficient and hence can even run on coin cells.
    Even though the operating voltage is 3.3V most of the pins are 5V tolerant and hence can be directly interfaced
    with 5V microcontrollers like Arduino.
    Another advantage of using these modules is that, each module has 6 Pipelines. Meaning, each module can
    communicate with 6 other modules to transmit or receive data. This makes the module suitable for creating
    star or mesh networks in IoT applications. Also they have a wide address range of 125 unique ID’s,
    hence in a closed area we can use 125 of these modules without interfering with each other. """

    def __init__(self):
        # Set the GPIO mode in "Broadcom SOC channel". This means that you are referring to the pins by the
        # "Broadcom SOC channel" number, these are the numbers after "GPIO"( for e.g. GPIO01,GPIO02…).
        # These are not the Board Numbers.
        GPIO.setmode(GPIO.BCM)

        # Next we will set it up the pipe address.
        # This address is important in order to communicate with the Arduino receiver.
        # The address will be in the hex code.
        pipes = [[0xE0, 0xE0, 0xF1, 0xF1, 0xE0], [0xF1, 0xF1, 0xF0, 0xF0, 0xE0]]

        # Begin the radio using GPIO08 as CE and GPIO25 as CSN pins.
        radio.begin(0, 25)

        # Set payload size as 32 bit, channel address as 76, data rate of 1 mbps and power levels as minimum.
        radio.setPayloadSize(32)
        radio.setChannel(0x76)
        radio.setDataRate(NRF24.BR_1MBPS)
        radio.setPALevel(NRF24.PA_MIN)
