# -*- coding: UTF-8 -*-
# Library : https://pypi.python.org/pypi/pushbullet.py

import RPi.GPIO as GPIO
import time
from pushbullet import Pushbullet


pb = Pushbullet('MYAPIKEYHERE')
me = 'YOURADRESSEMAIL@gmail.com'
pin = 21
SLEEP = 5
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
GPIO.setup(pin, GPIO.OUT)
GPIO.output(pin, GPIO.LOW)


def notification(pitch, duration):
    period = 1.0 / pitch
    delay = period / 2
    cycles = int(duration * pitch)
    for i in range(cycles):
        GPIO.output(pin, True)
        time.sleep(delay)
        GPIO.output(pin, False)
        time.sleep(delay)


while True:
    count = len(pb.get_pushes())
    pushes = pb.get_pushes()
    if count >= 1:
        if not pushes[0]['sender_email'] == me:
            notification(10, 0.5)
            time.sleep(0.25)
            notification(20, 0.5)
            time.sleep(0.25)
    else:
        GPIO.output(pin, GPIO.LOW)
    print 'Check In Progress'
    time.sleep(SLEEP)
