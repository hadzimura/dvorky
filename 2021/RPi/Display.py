#!/usr/bin/env python3
# coding=utf-8

from Adafruit_SSD1306 import SSD1306_128_64
from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont
import time


class MiniDisplay(object):

    def __init__(self):
        # Init 128x64 display on hardware I2C bus
        self.d = SSD1306_128_64(rst=None)

        # Get proper display size directly from hardware
        self.width = self.d.width
        self.height = self.d.height

        padding = -2
        self.top = padding
        self.bottom = self.height - padding
        self.x = 0

        # Start the display
        self.d.begin()

        # Clear the display
        self.d.clear()
        self.d.display()

        # Vytvoreni prazdneho obrazce pro vymazani displeje
        self.image = Image.new('1', (self.width, self.height))

        # Vytvoreni objektu pro kresleni
        self.draw = ImageDraw.Draw(self.image)

        # Vykresleni cerneho obdelnika pro vymazani obsahu displeje
        self.clear()

        # Set font (http://www.dafont.com/bitmap.php)
        # self.font = ImageFont.load_default()
        self.font = ImageFont.truetype('fonts/RetroGaming.ttf', 8)

    def clear(self):
        # Vykresleni cerneho obdelnika pro vymazani obsahu displeje
        self.draw.rectangle((0, 0, self.width, self.height), outline=0, fill=0)

    def create(self, words, line, color):

        if line == 1:
            line = 0
        else:
            line = (line - 1) * 8

        # print(words, line, color)
        self.draw.text((self.x, self.top + line), str(words), font=self.font, fill=color)
        self.d.image(self.image)
        self.d.display()

    def zobraz(self):
        # Zobrazeni na displej
        self.d.image(self.image)
        self.d.display()


lcd = MiniDisplay()
a = 1
ab = "start"

while True:
    # Vykresleni cerneho obdelnika pro vymazani obrazovky
    lcd.clear()

    # a = + 1
    # ab = str(a) + "\n" + str(a)
    lcd.create('test\n' + str(a), 1, 128)
    a += 1
    time.sleep(.1)
