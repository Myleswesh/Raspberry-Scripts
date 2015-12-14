from apiclient import discovery
from oauth2client import client, tools
import oauth2client
import httplib2

from datetime import datetime
import time, random, os

CALENDAR_ID         = 'lotsofnumbersandletters@group.calendar.google.com'
CLIENT_SECRET_FILE  = 'client_secret_lotsofnumbersandletters.apps.googleusercontent.com.json'
MP3_FOLDER          = 'mp3'

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

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
                mp3_files = random.choice(os.listdir(MP3_FOLDER))
                command = 'afplay \'{}/{}\''.format(MP3_FOLDER, mp3_files) # replace afplay with mpg123 for Raspberry or Linux
                logger.info('Event %s starting. Playing mp3 file %s...', name, mp3_files)
                os.system(command)

                if repeat == False:
                    time.sleep(60)

while True:
    calendar_event_query()
    time.sleep(5)
