#!/usr/bin/env python
# -*- coding: utf8 -*-

import RPi.GPIO as GPIO
import MFRC522
import time

MYCARD = '3590562'


GPIO.setmode(GPIO.BOARD)
GPIO.setwarnings(False)

GPIO.setup(33, GPIO.OUT)  # Red Led
GPIO.setup(31, GPIO.OUT)  # Yellow Led
GPIO.setup(35, GPIO.OUT)  # Green Led
GPIO.setup(37, GPIO.OUT)  # Buzzer

GPIO.setup(11, GPIO.OUT)  # IN1
GPIO.setup(12, GPIO.OUT)  # IN2
GPIO.setup(13, GPIO.OUT)  # IN3
GPIO.setup(15, GPIO.OUT)  # IN4


def buzzer(number):
    if number == '1':
        GPIO.output(37, GPIO.HIGH)
        time.sleep(0.05)
        GPIO.output(37, GPIO.LOW)
    elif number == '2':
        GPIO.output(37, GPIO.HIGH)
        time.sleep(0.05)
        GPIO.output(37, GPIO.LOW)
        time.sleep(0.05)
        GPIO.output(37, GPIO.HIGH)
        time.sleep(0.05)
        GPIO.output(37, GPIO.LOW)


def setStep(w1, w2, w3, w4):
    GPIO.output(11, w1)
    GPIO.output(12, w2)
    GPIO.output(13, w3)
    GPIO.output(15, w4)


def stop():
    setStep(0, 0, 0, 0)


def forward(delay, steps):
    for i in range(0, steps):
        setStep(1, 0, 0, 0)
        time.sleep(delay)
        setStep(0, 1, 0, 0)
        time.sleep(delay)
        setStep(0, 0, 1, 0)
        time.sleep(delay)
        setStep(0, 0, 0, 1)
        time.sleep(delay)


def backward(delay, steps):
    for i in range(0, steps):
        setStep(0, 0, 0, 1)
        time.sleep(delay)
        setStep(0, 0, 1, 0)
        time.sleep(delay)
        setStep(0, 1, 0, 0)
        time.sleep(delay)
        setStep(1, 0, 0, 0)
        time.sleep(delay)

MIFAREReader = MFRC522.MFRC522()

try:
    while True:
        (status, TagType) = MIFAREReader.MFRC522_Request(MIFAREReader.PICC_REQIDL)

        if status == MIFAREReader.MI_OK:
            print "Card detected"

        (status, uid) = MIFAREReader.MFRC522_Anticoll()

        if status == MIFAREReader.MI_OK:
            UIDcode = str(uid[0]) + str(uid[1]) + str(uid[2]) + str(uid[3])
            print UIDcode

            if UIDcode == MYCARD:
                adminpriv = 1
            else:
                adminpriv = 0

            if UIDcode == MYCARD:
                if adminpriv == 1:
                    GPIO.output(35, GPIO.HIGH)  # Green On
                    GPIO.output(33, GPIO.LOW)   # Red Off
                    buzzer('1')
                    backward(0.003, 128)
                    print "Door open"
                    time.sleep(3)
                    stop()

                    forward(0.0030, 128)
                    print "Door closed"
                    GPIO.output(35, GPIO.LOW)   # Red
                    GPIO.output(33, GPIO.HIGH)  #
                    stop()
            else:
                print "Unrecognised Card"
                GPIO.output(31, GPIO.HIGH)  # Yellow On
                GPIO.output(33, GPIO.LOW)  # Red Off
                buzzer('2')
                time.sleep(3)
                GPIO.output(31, GPIO.LOW)  # Yellow Off
                GPIO.output(33, GPIO.HIGH)  # Red On
except KeyboardInterrupt:
    GPIO.cleanup()
