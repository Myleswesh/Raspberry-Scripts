#Python 2.7.9
# https://www.raspberrypi.org/forums/viewtopic.php?f=63&t=148582#p979510

import sys
import pygame
import pygame.camera
import datetime as dt
import time

pygame.init()
pygame.camera.init()

change_channel = False
channel = 0
changeover_time = 5
Run = True

#create display 
screen = pygame.display.set_mode((1240,768),0)
pygame.font.init()
ovl_font = pygame.font.Font(None,30)
label1 = ovl_font.render('Camera 1', True,(255,255,255),(0,0,0))
label2 = ovl_font.render('Camera 2', True,(255,255,255),(0,0,0))

#find, open and start low-res camera
cam_list = pygame.camera.list_cameras()
webcam1 = pygame.camera.Camera(cam_list[0],(1024,768))
webcam2 = pygame.camera.Camera(cam_list[1],(320,240))
#webcam = pygame.camera.Camera(cam_list[channel],(1280,720))
#If no cameras found then nothing to do, quit
if(len(cam_list)==0):
    pygame.quit()
    sys.exit()
  
webcam1.start()
webcam2.start()
#webcam.start()

while Run:
     time.sleep(0.01)  
    #grab image, scale and blit to screen
    imagen1 = webcam1.get_image()
    imagen2 = webcam2.get_image()
    #imagen = webcam.get_image()
     #imagen = pygame.transform.scale(imagen,(1920,1080))
    screen.blit(imagen1,(0,0))
    screen.blit(imagen2,(0,0))
    screen.blit(label1,(imagen1.get_width()-label1.get_width()-10,imagen1.get_height() - label1.get_height() - 10))
    screen.blit(label2,(imagen2.get_width() - label2.get_width() - 10,imagen2.get_height() - label2.get_height() - 10))
    
    #draw all updates to display
    pygame.display.update()

    # check for events ESC key quits
    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                Run = False
                webcam1.stop()
                webcam2.stop()
