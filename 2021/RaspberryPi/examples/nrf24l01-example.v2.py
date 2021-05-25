import RPi.GPIO as GPIO
import time
import spidev
from lib_nrf24 import NRF24

# Set the GPIO mode in "Broadcom SOC channel". This means that you are referring to the pins by the "Broadcom SOC channel" number,
# these are the numbers after "GPIO"( for e.g. GPIO01,GPIO02…). These are not the Board Numbers.
GPIO.setmode(GPIO.BCM)

# Next we will set it up the pipe address. This address is important in order to communicate with the Arduino receiver.
# The address will be in the hex code.
pipes = [[0xE0, 0xE0, 0xF1, 0xF1, 0xE0], [0xF1, 0xF1, 0xF0, 0xF0, 0xE0]]

# Begin the radio using GPIO08 as CE and GPIO25 as CSN pins.
radio.begin(0, 25)

# Set payload size as 32 bit, channel address as 76, data rate of 1 mbps and power levels as minimum.
radio.setPayloadSize(32)
radio.setChannel(0x76)
radio.setDataRate(NRF24.BR_1MBPS)
radio.setPALevel(NRF24.PA_MIN)

# Open the pipes to start writing the data and print the basic details of nRF24l01.
radio.openWritingPipe(pipes[0])
radio.printDetails()

# Prepare a message in the string form. This message will be sent to Arduino UNO.
sendMessage = list("Hi..Arduino UNO")
while len(sendMessage) < 32:
    sendMessage.append(0)

# Start writing to the radio and keep on writing the complete string till the radio is available.
# Along with it, note down the time and print a debug statement of message delivery.
while True:
    start = time.time()
    radio.write(sendMessage)
    print("Sent the message: {}".format(sendMessage))
send
    radio.startListening()

# If the string is completed and pipe is closed then print a debug message of timed out.
while not radio.available(0):
        time.sleep(1/100)
        if time.time() - start > 2:
            print("Timed out.")  # print error message if radio disconnected or not functioning anymore
            break

# Stop listening to the radio and close the communication and restart the communication after 3 seconds to send another message.
  radio.stopListening()     # close radio
    time.sleep(3)  # give delay of 3 seconds

