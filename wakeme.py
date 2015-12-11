from apiclient import discovery
from oauth2client import client, tools
import oauth2client
import httplib2

from datetime import datetime
import time, random, os

CALENDAR_ID         = 'lotsofnumbersandletters@group.calendar.google.com'
CLIENT_SECRET_FILE  = 'client_secret_lotsofnumbersandletters.apps.googleusercontent.com.json'
MP3_FOLDER          = 'mp3'

def get_credentials():
    home_dir = os.path.expanduser('~')
    credential_dir = os.path.join(home_dir, '.credentials')
    if not os.path.exists(credential_dir):
        os.makedirs(credential_dir)
    credential_path = os.path.join(credential_dir,'calendar-python-quickstart.json')

    store = oauth2client.file.Storage(credential_path)
    credentials = store.get()
    if not credentials or credentials.invalid:
        flow = client.flow_from_clientsecrets(CLIENT_SECRET_FILE, 'https://www.googleapis.com/auth/calendar')
        flow.user_agent = 'Google Calendar API Python Quickstart'
        credentials = tools.run(flow, store)
        print('Storing credentials to ' + credential_path)
    return credentials

def calendar_event_query():
    credentials = get_credentials()
    http        = credentials.authorize(httplib2.Http())
    service     = discovery.build('calendar', 'v3', http=http)
    today       = datetime.today()
    events      = service.events().list(singleEvents=True, calendarId=CALENDAR_ID).execute()
    now         = today.strftime('%Y-%m-%dT%H:%M')
    songfile    = random.choice(os.listdir(MP3_FOLDER))

    for i, event in enumerate(events['items']):
        try:
            start = event['start']['dateTime'][:-9]
        except KeyError:
            start = ''
        if start == now:
            command     =  'mpg123 \'{}/{}\''.format(MP3_FOLDER, songfile) # mpg123 = Raspberry/Linux or afplay = MacOSX
            os.system(command)

while True:
    calendar_event_query()
    time.sleep(5)
