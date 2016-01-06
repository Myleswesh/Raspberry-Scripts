# -*- coding: UTF-8 -*-
# Library : https://github.com/charlierguo/gmail/

import gmail
import RPi.GPIO as GPIO
import time

USERNAME = 'Your Username'
PASSWORD = 'Your Password'

NEWMAIL_OFFSET = 0
MAIL_CHECK_FREQ = 10  # Check every 10 secondes

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
GREEN_LED = 18
RED_LED = 23
GPIO.setup(GREEN_LED, GPIO.OUT)
GPIO.setup(RED_LED, GPIO.OUT)

def loop():
	g = gmail.login(USERNAME, PASSWORD)
	mails = len(g.inbox().mail(unread=True))
	print mails
    	if mails > NEWMAIL_OFFSET:
        	GPIO.output(GREEN_LED, GPIO.HIGH)
        	GPIO.output(RED_LED, GPIO.LOW)
    	else:
        	GPIO.output(GREEN_LED, GPIO.LOW)
        	GPIO.output(RED_LED, GPIO.HIGH) 
    	time.sleep(MAIL_CHECK_FREQ)

try:
	while True:
		loop()
finally:
	GPIO.cleanup()
