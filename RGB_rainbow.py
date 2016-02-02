#!/usr/bin/python

import RPi.GPIO as GPIO
import colorsys
import time

red = 23                    
green = 22                  
blue = 27                   

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)

GPIO.setup(red, GPIO.OUT)
GPIO.setup(green, GPIO.OUT)
GPIO.setup(blue, GPIO.OUT)

pr = GPIO.PWM(red, 100)     
pg = GPIO.PWM(green, 100)    
pb = GPIO.PWM(blue, 100)    
pr.start(0)               
pg.start(0)
pb.start(0)

try:
    while True:
        steps = 200
        for h in range(0, steps):
            hue = h/steps
            rgb = colorsys.hsv_to_rgb(hue, 1, 1)

            pr.ChangeDutyCycle(rgb[0]*100)
            pg.ChangeDutyCycle(rgb[1]*100)
            pb.ChangeDutyCycle(rgb[2]*100)

            time.sleep(0.05)

except KeyboardInterrupt:
    pr.stop()
    pg.stop()
    pb.stop()
    GPIO.cleanup()
 
