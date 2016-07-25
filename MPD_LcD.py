# -*- coding: utf-8 -*-

import RPi.GPIO as GPIO
import Adafruit_CharLCD as LCD
from mpd import (MPDClient, CommandError)
from socket import error as SocketError
import sys
import time
import threading
from datetime import datetime

gpio_numbering_mode = GPIO.BCM

BUTTON_PLAY = 16
BUTTON_NEXT = 20
BUTTON_PREV = 26
BUTTON_VUP = 2
BUTTON_VDN = 3
BUTTON_STOP = 4

bounce_time = 200

lcd_rs = 25
lcd_en = 24
lcd_d4 = 23
lcd_d5 = 17
lcd_d6 = 21
lcd_d7 = 22

LCD_BACKLIGHT = 1
lcd_columns = 16
lcd_rows = 2
scrolling_period = 20
scrolling_start = 100
webradio_scroll = True
volume_screen_duration = 300
backlight_timeout = 5

HOST = 'localhost'
PORT = '6600'
PASSWORD = False
CON_ID = {'host': HOST, 'port': PORT}

GPIO.setmode(gpio_numbering_mode)

GPIO.setwarnings(False)

lcd = LCD.Adafruit_CharLCD(lcd_rs, lcd_en, lcd_d4, lcd_d5, lcd_d6, lcd_d7, lcd_columns, lcd_rows, None)
client = MPDClient()
client_cntrl = MPDClient()

data = {'state': 0, 'artist': '', 'title': '', 'type': 0, 'volume': 0}

data_changed = False
data_changed_vol = False;

def update_lcd():
    global data
    global data_changed
    global data_changed_vol
    framebuffer = ['', '']
    direction = [0, 0]
    counter = [0, 0]
    vol_count = 0
    vol_screen = False
    counters = [0, 0]
    backlight = False
    backlight_counter = 0

    if (backlight_timeout > 0):
        GPIO.output(LCD_BACKLIGHT, True)
        backlight = True

    lcd_square = (0b11111, 0b11111, 0b11111, 0b11111, 0b11111, 0b11111, 0b11111, 0b11111)
    lcd.create_char(0, lcd_square)

    old_data = data


# Infinite Loop


    while True:
        today = datetime.today()
        now = today.strftime('%Y-%m-%d %H:%M')
        time.sleep(0.01)

        if (backlight_counter > 0):
            backlight_counter -= 1
            if (backlight_counter == 0):
                if (backlight == True):
                    GPIO.output(LCD_BACKLIGHT, False)
                    backlight = False

        if (data_changed == True):
            if (backlight_timeout > 0 and backlight == False):
                GPIO.output(LCD_BACKLIGHT, True)
                backlight = True
                backlight_counter = 0

            direction = [0, 0]
            counter = [0, 0]
            old_data = data

            if (len(old_data['artist']) < 16):
                framebuffer[0] = old_data['artist']

                for i in range(16 - len(old_data['artist'])):
                    framebuffer[0] += ' '

            elif (len(old_data['artist']) == 16):
                framebuffer[0] = old_data['artist']

            else:
                framebuffer[0] = old_data['artist'][0:16]

            if (len(old_data['title']) < 16):
                framebuffer[1] = old_data['title']

                for i in range(16 - len(old_data['title'])):
                    framebuffer[1] += ' '

            elif (len(old_data['title']) == 16):
                framebuffer[1] = old_data['title']

            else:
                framebuffer[1] = old_data['title'][0:16]

            lcd.set_cursor(0, 0)
            lcd.message(framebuffer[0] + '\n' + framebuffer[1])

            data_changed = False
            vol_screen = False
            vol_count = 0
            counters[1] = scrolling_start
            continue

        if (data_changed_vol == True):
            if (backlight_timeout > 0 and backlight == False):
                GPIO.output(LCD_BACKLIGHT, True)
                backlight = True
                backlight_counter = 0

            vol_screen = True
            vol_count = volume_screen_duration
            data_changed_vol = False

            vol_string = "Volume"
            if (data['volume'] == 100):
                vol_string += "       MAX"
            elif (data['volume'] >= 10):
                vol_string += "      "
                vol_string += `data['volume']`
                vol_string += " %"
            elif (data['volume'] == 0):
                vol_string += "       MIN"
            else:
                vol_string += "       "
                vol_string += `data['volume']`
                vol_string += " %"

            if (data['volume'] == 0):
                vol_string2 = "                "
            elif (data['volume'] == 100):
                vol_string2 = ""
                for i in range(0, 16):
                    vol_string2 += unichr(0)
            else:
                vol_string2 = ""
                pom_num = (data['volume'] / 7) + 1
                for i in range(0, pom_num):
                    vol_string2 += unichr(0)

                for i in range(0, (16 - pom_num)):
                    vol_string2 += " "

            lcd.set_cursor(0, 0)
            lcd.message(vol_string + '\n' + vol_string2)
            continue

        if (vol_screen == True):
            if (vol_count == 0):
                vol_screen = False
                vol_count = 0
                direction = [0, 0]
                counter = [0, 0]
                counters[1] = 0
            else:
                vol_count -= 1
            continue

        if (old_data['state'] == 0):
            framebuffer[0] = '    STOPPED     '
            framebuffer[1] = ''+now+''

            lcd.set_cursor(0, 0)
            lcd.message(framebuffer[0] + '\n' + framebuffer[1])

            if (backlight_timeout > 0 and backlight == True and backlight_counter == 0):
                backlight_counter = backlight_timeout * 10
            continue;


        elif (old_data['state'] == 2):
            framebuffer[0] = '     PAUSED     '
            framebuffer[1] = ''+now+''

            lcd.set_cursor(0, 0)
            lcd.message(framebuffer[0] + '\n' + framebuffer[1])

            if (backlight_timeout > 0 and backlight == True and backlight_counter == 0):
                backlight_counter = backlight_timeout * 10
            continue;

        elif (old_data['state'] == 1):
            if (counters[1] > 0):
                counters[1] -= 1
                continue;

            if (len(old_data['artist']) > 16):
                if (old_data['type'] == 0 or (old_data['type'] == 1 and webradio_scroll == True)):
                    framebuffer[0] = old_data['artist'][counter[0]:counter[0] + 16]

                    if (direction[0] == 0):
                        if (counter[0] == (len(old_data['artist']) - 16)):
                            direction[0] = 1
                        else:
                            counter[0] += 1

                    else:
                        if (counter[0] == 0):
                            direction[0] = 0
                        else:
                            counter[0] -= 1

                elif (old_data['type'] == 1 and webradio_scroll == False):
                    framebuffer[0] = old_data['artist'][0:16]

            elif (len(old_data['artist']) == 16):
                framebuffer[0] = old_data['artist']

            else:
                framebuffer[0] = old_data['artist']

                for i in range(16 - len(old_data['artist'])):
                    framebuffer[0] += ' '

            if (len(old_data['title']) > 16):
                framebuffer[1] = old_data['title'][counter[1]:counter[1] + 16]

                if (direction[1] == 0):
                    if (counter[1] == (len(old_data['title']) - 16)):
                        direction[1] = 1
                    else:
                        counter[1] += 1

                else:
                    if (counter[1] == 0):
                        direction[1] = 0
                    else:
                        counter[1] -= 1

            elif (len(old_data['title']) == 16):
                framebuffer[1] = old_data['title']

            else:
                framebuffer[1] = old_data['title']

                for i in range(16 - len(old_data['title'])):
                    framebuffer[1] += ' '

            lcd.set_cursor(0, 0)
            lcd.message(framebuffer[0] + '\n' + framebuffer[1])
            counters[1] = scrolling_period


def mpd_ping():
    while True:
        time.sleep(50)
        client_cntrl.ping()


def mpdConnect(client, con_id):
    try:
        client.connect(**con_id)
    except SocketError:
        return False
    return True


#
def mpdAuth(client, secret):
    try:
        client.password(secret)
    except CommandError:
        return False
    return True


def play_pressed(channel):
    global client_cntrl
    time.sleep(0.05)
    if (GPIO.input(BUTTON_PLAY) == 0):
        if (data['state'] == 1):
            client_cntrl.pause(1)
        else:
            client_cntrl.play()
            #


def stop_pressed(channel):
    global client_cntrl
    time.sleep(0.05)
    if (GPIO.input(BUTTON_STOP) == 0):
        client_cntrl.stop()


def prev_pressed(channel):
    global client_cntrl
    time.sleep(0.05)
    if (GPIO.input(BUTTON_PREV) == 0):
        client_cntrl.previous()


def next_pressed(channel):
    global client_cntrl
    time.sleep(0.05)
    if (GPIO.input(BUTTON_NEXT) == 0):
        client_cntrl.next()

def vdn_pressed(channel):
    global client_cntrl, client
    time.sleep(0.05)
    if (GPIO.input(BUTTON_VDN) == 0):
        client_cntrl.setvol(data['volume'] - 5)


def vup_pressed(channel):
    global client_cntrl, client
    time.sleep(0.05)
    if (GPIO.input(BUTTON_VUP) == 0):
        client_cntrl.setvol(data['volume'] + 5)


if mpdConnect(client, CON_ID):
    print('MPD Client Connected!')
else:
    print('Fail to connect to MPD server!')
    sys.exit(1)

if PASSWORD:
    if mpdAuth(client, PASSWORD):
        print('Pass auth!')
    else:
        print('Error trying to pass auth.')
        client.disconnect()
        sys.exit(2)

if mpdConnect(client_cntrl, CON_ID):
    print('MPD Client_Cntrl Connected!')
else:
    print('Fail to connect to MPD server!')
    sys.exit(1)

if PASSWORD:
    if mpdAuth(client_cntrl, PASSWORD):
        print('Pass auth!')
    else:
        print('Error trying to pass auth.')
        client_cntrl.disconnect()
        sys.exit(2)
data['volume'] = int(client.status()['volume'])

try:
    station = client.currentsong()['name']
except KeyError:
    station = ''

try:
    title = client.currentsong()['title']
except KeyError:
    title = ''

try:
    artist = client.currentsong()['artist']
except KeyError:
    artist = ''

if (station != ''):
    data['type'] = 1

    lst = [word[0].upper() + word[1:] for word in station.split()]
    data['artist'] = " ".join(lst)

    lst = [word[0].upper() + word[1:] for word in title.split()]
    data['title'] = " ".join(lst)

else:  # file
    data['type'] = 0

    lst = [word[0].upper() + word[1:] for word in artist.split()]
    data['artist'] = " ".join(lst)

    lst = [word[0].upper() + word[1:] for word in title.split()]
    data['title'] = " ".join(lst)

if (client.status()['state'] == 'play'):
    data['state'] = 1

elif (client.status()['state'] == 'stop'):
    data['state'] = 0

elif (client.status()['state'] == 'pause'):
    data['state'] = 2

if (backlight_timeout > 0):
    GPIO.setup(LCD_BACKLIGHT, GPIO.OUT)

lcd_t = threading.Thread(target=update_lcd, args=())
lcd_t.daemon = True
lcd_t.start()

mpdping_t = threading.Thread(target=mpd_ping, args=())
mpdping_t.daemon = True
mpdping_t.start()

data_changed = True

GPIO.setup(BUTTON_PLAY, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(BUTTON_NEXT, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(BUTTON_PREV, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(BUTTON_VUP, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(BUTTON_VDN, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(BUTTON_STOP, GPIO.IN, pull_up_down=GPIO.PUD_UP)

GPIO.add_event_detect(BUTTON_PLAY, GPIO.FALLING, callback=play_pressed, bouncetime=bounce_time)
GPIO.add_event_detect(BUTTON_NEXT, GPIO.FALLING, callback=next_pressed, bouncetime=bounce_time)
GPIO.add_event_detect(BUTTON_PREV, GPIO.FALLING, callback=prev_pressed, bouncetime=bounce_time)
GPIO.add_event_detect(BUTTON_VUP, GPIO.FALLING, callback=vup_pressed, bouncetime=bounce_time)
GPIO.add_event_detect(BUTTON_VDN, GPIO.FALLING, callback=vdn_pressed, bouncetime=bounce_time)
GPIO.add_event_detect(BUTTON_STOP, GPIO.FALLING, callback=stop_pressed, bouncetime=bounce_time)

while (1):
    client.send_idle()
    state = client.fetch_idle()

    if (state[0] == 'mixer'):
        data['volume'] = int(client.status()['volume'])
        data_changed_vol = True

    if (state[0] == 'player'):
        try:
            station = client.currentsong()['name']
        except KeyError:
            station = ''

        try:
            title = client.currentsong()['title']
        except KeyError:
            title = ''

        try:
            artist = client.currentsong()['artist']
        except KeyError:
            artist = ''

        if (station != ''):
            data['type'] = 1

            lst = [word[0].upper() + word[1:] for word in station.split()]
            data['artist'] = " ".join(lst)

            lst = [word[0].upper() + word[1:] for word in title.split()]
            data['title'] = " ".join(lst)

        else:  # file
            data['type'] = 0

            lst = [word[0].upper() + word[1:] for word in artist.split()]
            data['artist'] = " ".join(lst)

            lst = [word[0].upper() + word[1:] for word in title.split()]
            data['title'] = " ".join(lst)

        if (client.status()['state'] == 'play'):
            data['state'] = 1

        elif (client.status()['state'] == 'stop'):
            data['state'] = 0

        elif (client.status()['state'] == 'pause'):
            data['state'] = 2

        data_changed = True

client.disconnect()

lcd_t.join()
mpdping_t.join()

# Exit
sys.exit(0)
