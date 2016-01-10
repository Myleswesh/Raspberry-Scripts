#!/usr/bin/env python
# -*- coding: UTF-8 -*-

from __future__ import print_function
import httplib2
import os

from apiclient import discovery
import oauth2client
from oauth2client import client
from oauth2client import tools

import time
import argparse
import RPi.GPIO as GPIO


RG = [20, 21]
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

for pin in RG:
    GPIO.setup(pin, GPIO.OUT)
    GPIO.output(pin, GPIO.LOW)

try:
    flags = argparse.ArgumentParser(parents=[tools.argparser]).parse_args()
except ImportError:
    flags = None

CLIENT_SECRET_FILE = 'google_notif.json'


def get_credentials():
    home_dir = os.path.expanduser('~')
    credential_dir = os.path.join(home_dir, '.credentials')
    if not os.path.exists(credential_dir):
        os.makedirs(credential_dir)
    credential_path = os.path.join(credential_dir, 'raspberry-gmail.json')

    store = oauth2client.file.Storage(credential_path)
    credentials = store.get()
    if not credentials or credentials.invalid:
        flow = client.flow_from_clientsecrets(CLIENT_SECRET_FILE, 'https://www.googleapis.com/auth/gmail.readonly')
        flow.user_agent = 'Raspberry Gmail'
        if flags:
            credentials = tools.run_flow(flow, store, flags)
        else:
            credentials = tools.run(flow, store)
        print('Storing credentials to ' + credential_path)
    return credentials


def main():
    credentials = get_credentials()
    http = credentials.authorize(httplib2.Http())
    service = discovery.build('gmail', 'v1', http=http)

    results = service.users().messages().list(userId='me', labelIds='UNREAD').execute()

    messages = results.get('messages', [])

    if not messages:
        GPIO.output(20, True)   # Red On
        GPIO.output(21, False)  # Green Off

    else:
        GPIO.output(20, False)  # Red Off
        GPIO.output(21, True)   # Green On

try:
    while True:
        main()
        time.sleep(5)   # Google allows minimum 5 requests per second
except KeyboardInterrupt:
        GPIO.cleanup()
