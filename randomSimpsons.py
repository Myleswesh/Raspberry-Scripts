#!/usr/bin/python
# source and all copyright to Stephen Coyle ( http://stephencoyle.net/the-pi-zero-simpsons-shuffler )


import RPi.GPIO as GPIO
import time
import os
import random

buttonPin = 17

directory = "/home/pi/simpsons/"

GPIO.setmode(GPIO.BCM)
GPIO.setup(buttonPin, GPIO.IN)

def playEpisode():
	episode = random.choice(os.listdir(directory))
	cmd = "nohup omxplayer -b -o hdmi "+"'"+directory+episode+"' &"
	os.system('killall omxplayer.bin')
	os.system(cmd)

try:
	
	GPIO.wait_for_edge(buttonPin, GPIO.FALLING)
	playEpisode()


	os.system('sudo python /home/pi/randomSimpsons.py') #point this to the location of this file

except KeyboardInterrupt:  
    GPIO.cleanup()      
