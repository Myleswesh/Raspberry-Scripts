#!/usr/bin/env python
# -*- coding: utf8 -*-

import RPi.GPIO as GPIO
import MFRC522
import signal
import time

MYCARD = 'MY_UID_CARD'

continue_reading = True

def end_read(signal,frame):
    global continue_reading
    print "Ctrl+C captured, ending read."
    continue_reading = False
    GPIO.cleanup()

def buzzer(number):
    if number  == '1':
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

signal.signal(signal.SIGINT, end_read)

# Create an object of the class MFRC522
MIFAREReader = MFRC522.MFRC522()

while continue_reading:
    GPIO.setup(33, GPIO.OUT) # Red
    GPIO.setup(31, GPIO.OUT) # Yellow
    GPIO.setup(35, GPIO.OUT) # Green
    GPIO.setup(37, GPIO.OUT) # Buzzer

# Scan for cards
    (status,TagType) = MIFAREReader.MFRC522_Request(MIFAREReader.PICC_REQIDL)

    # If a card is found
    if status == MIFAREReader.MI_OK:
        print "Card detected"

    # Get the UID of the card
    (status,uid) = MIFAREReader.MFRC522_Anticoll()

    # If we have the UID, continue
    if status == MIFAREReader.MI_OK:

        # Print UID
        UIDcode = str(uid[0])+str(uid[1])+str(uid[2])+str(uid[3])
        print UIDcode

        if UIDcode == MYCARD:
            adminpriv = 1
        else:
            adminpriv = 0

        if UIDcode == MYCARD:
            if adminpriv == 1:
		GPIO.output(35, GPIO.HIGH)  # Green On
		GPIO.output(33, GPIO.LOW)  # Red Off
		buzzer('1')
                print "Door open"
                time.sleep(3)
		GPIO.output(35, GPIO.LOW) # Red 
		GPIO.output(33, GPIO.HIGH) #
                print "Finished"
            else:
                print "Door locked"
        else:
	    GPIO.output(31, GPIO.HIGH) # Yellow On
	    GPIO.output(33, GPIO.LOW)  # Red Off
            buzzer('2')
            time.sleep(3)
	    GPIO.output(31, GPIO.LOW)  # Yellow Off
            GPIO.output(33, GPIO.HIGH)  # Red On
            print "Unrecognised Card"
