#!/usr/bin/env python
# -*- coding: UTF-8 -*-

from __future__ import print_function
import httplib2

from apiclient import discovery
import oauth2client
from oauth2client import client
from oauth2client import tools

from datetime import datetime
import logging
import time
import random
import os
import argparse

try:

    flags = argparse.ArgumentParser(parents=[tools.argparser]).parse_args()
except ImportError:
    flags = None

CALENDAR_ID = 'YOUR_CALENDAR_ID@group.calendar.google.com'
CLIENT_SECRET_FILE = 'raspi-wake.json'
SCOPE = 'https://www.googleapis.com/auth/calendar.readonly'
MP3_FOLDER = 'mp3'

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def get_credentials():
    home_dir = os.path.expanduser('~')
    credential_dir = os.path.join(home_dir, '.credentials')
    if not os.path.exists(credential_dir):
        os.makedirs(credential_dir)
    credential_path = os.path.join(credential_dir, 'raspberry-wake.json')

    store = oauth2client.file.Storage(credential_path)
    credentials = store.get()
    if not credentials or credentials.invalid:
        flow = client.flow_from_clientsecrets(CLIENT_SECRET_FILE, scope=SCOPE)
        flow.user_agent = 'Raspberry Wake'
        if flags:
            credentials = tools.run_flow(flow, store, flags)
        else:
            credentials = tools.run(flow, store)
        print('Storing credentials to ' + credential_path)

    return credentials


def calendar_event_query():
    credentials = get_credentials()
    http = credentials.authorize(httplib2.Http())
    service = discovery.build('calendar', 'v3', http=http)

    today = datetime.today()
    events = service.events().list(singleEvents=True, calendarId=CALENDAR_ID).execute()

    for i, event in enumerate(events['items']):
        try:
            start = event['start']['dateTime'][:-9]
        except KeyError:
            start = ''

        description = event.get('description', '')
        now = today.strftime('%Y-%m-%dT%H:%M')

        if start >= now and description.lower() == 'wake':
            if start == now:
                mp3_files = random.choice(os.listdir(MP3_FOLDER))
                command = 'mpg123 \'{}/{}\''.format(MP3_FOLDER, mp3_files)
                os.system(command)
                time.sleep(60)

while True:
    calendar_event_query()
    time.sleep(5)
