#!/usr/bin/env python
# -*- coding: utf-8 -*-

import max7219.led as led
import time
import locale
import Adafruit_DHT as dht

DHT22_PIN = 4
SPI_DEVICE_NUMBER = 5

device = led.matrix(cascaded=SPI_DEVICE_NUMBER)
device.brightness(1)
locale.setlocale(locale.LC_ALL, '')


try:
    while (True):
        humidity, temperature = dht.read_retry(dht.DHT22, DHT22_PIN)
        clock = time.strftime("%H:%M")
        minutes = int(time.strftime("%M"))
        seconds = int(time.strftime("%S"))
        month = time.strftime(" %m")
        day = time.strftime(" %d")
        year = time.strftime("%Y")
        for n, c in enumerate(clock):
            device.letter(n, ord(c))

        if seconds == 59:
            device.clear()
            device.show_message('Temp : ' + format(temperature, '.2f') + 'C')
            device.clear()
            device.show_message('Hum : ' + format(humidity, '.2f') + '%')
            device.clear()
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

except KeyboardInterrupt:
    device.clear()
