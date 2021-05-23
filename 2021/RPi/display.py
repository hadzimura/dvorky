# pripojeni knihoven
import time
from Adafruit_SSD1306 import SSD1306_128_64

from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont

import subprocess


class Display(object):

    def __init__(self):
        # Nastaveni displeje 128x64 s hardware I2C sbernici
        self.d = SSD1306_128_64(rst=None)

        # Display Size from HW
        self.width = self.d.width
        self.height = self.d.height

        padding = -2
        self.top = padding
        self.bottom = self.height - padding
        self.x = 0

        # Zahajeni komunikace s displejem
        self.d.begin()

        # Vycisteni displeje
        self.d.clear()
        self.d.display()

        # Vytvoreni prazdneho obrazce pro vymazani displeje
        self.image = Image.new('1', (self.width, self.height))

        # Vytvoreni objektu pro kresleni
        self.draw = ImageDraw.Draw(self.image)

        # Vykresleni cerneho obdelnika pro vymazani obsahu displeje
        self.clear()

        # Nacteni zakladniho pisma
        self.font = ImageFont.load_default()

    # Muzeme pouzit take jine fonty, napriklad z:
    # http://www.dafont.com/bitmap.php
    # Pote staci umistit font do stejne slozky a nastavit:
    # font = ImageFont.truetype('RetroComputer.ttf', 8)

    def clear(self):
        # Vykresleni cerneho obdelnika pro vymazani obsahu displeje
        self.draw.rectangle((0, 0, self.width, self.height), outline=0, fill=0)

    def create(self, words, line, color):

        if line == 1:
            line = 0
        else:
            line = (line - 1) * 8

        print(words, line, color)
        self.draw.text((self.x, self.top + line), str(words), font=self.font, fill=color)
        self.d.image(self.image)
        self.d.display()

    def zobraz(self):
        # Zobrazeni na displej
        self.d.image(self.image)
        self.d.display()


my_display = Display()
a = 1
ab = "start"

while True:
    # Vykresleni cerneho obdelnika pro vymazani obrazovky
    my_display.clear()

    # Skripty pro nacteni informaci o systemu, zdroj:
    # https://unix.stackexchange.com/questions/119126/command-to-display-memory-usage-disk-usage-and-cpu-load
    # cmd = "hostname -I | cut -d\' \' -f1"
    # IP = subprocess.check_output(cmd, shell = True )
    # my_display.create("IP: " + str(IP), 8, 128)
    # my_display.zobraz
    a = + 1
    ab = str(a) + "\n" + str(a)
    my_display.create(ab, 1, 128)

    # draw.text((x, top+8),     str(CPU), font=font, fill=255)
    # draw.text((x, top+16),    str(MemUsage),  font=font, fill=255)
    # draw.text((x, top+25),    str(Disk),  font=font, fill=255)
    # Vypsani naseho textu
    # draw.text((x, top+32),    str("Arduino navody"),  font=font, fill=127)

    # Zobrazeni na displej
#    disp.image(image)
#   disp.display()
# Kratka pauza 100 ms
# time.sleep(.1)
