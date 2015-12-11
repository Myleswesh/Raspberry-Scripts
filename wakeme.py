from __future__ import print_function
import httplib2
import os

from apiclient import discovery
import oauth2client
from oauth2client import client
from oauth2client import tools

from datetime import datetime
import logging, os, platform, re, time

try:
    import argparse
    flags = argparse.ArgumentParser(parents=[tools.argparser]).parse_args()
except ImportError:
    flags = None

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
APPLICATION_NAME = 'Google Calendar API Python Quickstart'
API_KEY = '123456789qwertyuiop987654321asdfghjkl54321'
CALENDAR_ID = 'lotsofnumbersandletters@group.calendar.google.com'
SCOPES = 'https://www.googleapis.com/auth/calendar'
CLIENT_SECRET_FILE = 'client_secret_againlotsofnumbersandletters.apps.googleusercontent.com.json'
FREQUENCY_CHECK = 5 # in seconds
MP3_FOLDER = 'mp3'

class Alarm():
    def get_credentials(self):
        home_dir = os.path.expanduser('~')
        credential_dir = os.path.join(home_dir, '.credentials')
        if not os.path.exists(credential_dir):
            os.makedirs(credential_dir)
        credential_path = os.path.join(credential_dir,
                                       'calendar-python-quickstart.json')

        store = oauth2client.file.Storage(credential_path)
        credentials = store.get()
        if not credentials or credentials.invalid:
            flow = client.flow_from_clientsecrets(CLIENT_SECRET_FILE, SCOPES)
            flow.user_agent = APPLICATION_NAME
            if flags:
                credentials = tools.run_flow(flow, store, flags)
            else: # Needed only for compatibility with Python 2.6
                credentials = tools.run(flow, store)
            print('Storing credentials to ' + credential_path)
        return credentials

    def calendar_event_query(self):
        credentials = self.get_credentials()
        http = credentials.authorize(httplib2.Http())
        service = discovery.build('calendar', 'v3', http=http)

        today = datetime.today()
        events = service.events().list(singleEvents=True, calendarId=CALENDAR_ID).execute()

        for i, event in enumerate(events['items']):
            name = event['summary'].lower()
            try:
                start = event['start']['dateTime'][:-9]
            except KeyError:
                start = ''

            description = event.get('description', '')
            repeat = True if description.lower() == 'repeat' else False
            now = today.strftime('%Y-%m-%dT%H:%M')

            if start >= now:
                logger.debug('Event #%s, Name: %s, Start: %s', i, name, start)

                if start == now:
                    mp3_files = os.listdir(MP3_FOLDER)
                    mp3_name = 'default.mp3'
                    command = 'afplay \'{}/{}\''.format(MP3_FOLDER, mp3_name) # mpg123 = Raspberry/Linux and afplay = MacOSX
                    logger.info('Event %s starting. Playing mp3 file %s...', name, mp3_name)
                    os.system(command)
                    if repeat == False:
                        time.sleep(60)

    def poll(self):
        logger.info('Polling calendar for events...')
        self.calendar_event_query()

while True:
    a = Alarm()
    a.poll()
    time.sleep(FREQUENCY_CHECK)
