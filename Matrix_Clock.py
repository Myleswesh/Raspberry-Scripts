#!/usr/bin/env python
# -*- coding: utf-8 -*-

import max7219.led as led
import datetime
import time
from max7219.font import proportional, SINCLAIR_FONT, TINY_FONT, CP437_FONT
from random import randrange
import locale

device = led.matrix(cascaded=5)
device.brightness(1)
locale.setlocale(locale.LC_ALL, '')

while(True):
        clock = time.strftime("%H:%M")
        seconds = int(time.strftime("%S"))
        month = time.strftime(" %m")
        day = time.strftime(" %d")
        year = time.strftime("%Y")
        for n, c in enumerate(clock):
                device.letter(n, ord(c))
        if seconds == 59 :
                for row in range(8):
                        device.scroll_up()
                        time.sleep(0.1)
                for n, c in enumerate(day):
                        device.letter(n, ord(c))
                time.sleep(1)
                for row in range(8):
                        device.scroll_down()
                        time.sleep(0.1)
                for n, c in enumerate(month):
                        device.letter(n, ord(c))
                time.sleep(1)
                for row in range(8):
                        device.scroll_down()
                        time.sleep(0.1)
                for n, c in enumerate(year):
                        device.letter(n, ord(c))
                time.sleep(1)
                for row in range(8):
                        device.scroll_down()
                        time.sleep(0.1)
                device.show_message(time.strftime("%d %B %Y"))
