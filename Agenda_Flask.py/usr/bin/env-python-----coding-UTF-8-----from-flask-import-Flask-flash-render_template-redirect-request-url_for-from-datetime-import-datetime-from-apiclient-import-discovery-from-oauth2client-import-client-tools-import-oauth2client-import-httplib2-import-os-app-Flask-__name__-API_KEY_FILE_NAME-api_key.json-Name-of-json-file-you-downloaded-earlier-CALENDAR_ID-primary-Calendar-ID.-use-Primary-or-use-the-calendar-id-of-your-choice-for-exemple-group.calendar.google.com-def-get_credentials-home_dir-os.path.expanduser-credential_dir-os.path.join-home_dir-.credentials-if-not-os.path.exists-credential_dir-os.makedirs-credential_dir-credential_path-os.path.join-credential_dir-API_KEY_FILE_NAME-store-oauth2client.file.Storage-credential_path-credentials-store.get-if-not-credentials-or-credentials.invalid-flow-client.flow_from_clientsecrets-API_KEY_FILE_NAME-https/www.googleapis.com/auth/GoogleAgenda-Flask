#!/usr/bin/env python
# -*- coding: UTF-8 -*-

from flask import Flask, flash, render_template, redirect, request, url_for
from datetime import datetime

from apiclient import discovery
from oauth2client import client, tools
import oauth2client
import httplib2

import os

app = Flask(__name__)

API_KEY_FILE_NAME = 'api_key.json'   # Name of json file you downloaded earlier
CALENDAR_ID = 'primary'     # Calendar ID. use Primary or use the calendar id of your choice (for exemple
                            # @group.calendar.google.com)


def get_credentials():
    home_dir = os.path.expanduser('~')
    credential_dir = os.path.join(home_dir, '.credentials')
    if not os.path.exists(credential_dir):
        os.makedirs(credential_dir)
    credential_path = os.path.join(credential_dir, API_KEY_FILE_NAME)

    store = oauth2client.file.Storage(credential_path)
    credentials = store.get()
    if not credentials or credentials.invalid:
        flow = client.flow_from_clientsecrets(API_KEY_FILE_NAME, 'https://www.googleapis.com/auth/calendar')
        flow.user_agent = 'Raspberry Flask Calendar'
        flags = tools.argparser.parse_args(args=[])
        credentials = tools.run_flow(flow, store, flags)
        print('Storing credentials to ' + credential_path)
    return credentials


@app.route('/')
def index():
    credentials = get_credentials()
    http = credentials.authorize(httplib2.Http())
    service = discovery.build('calendar', 'v3', http=http)
    now = datetime.utcnow().isoformat() + 'Z'  # 'Z' indicates UTC time
    events = service.events().list(calendarId=CALENDAR_ID, timeMin=now, maxResults=10, singleEvents=True,
                                   orderBy='startTime').execute()

    templateData = {
        'agenda': events['items']
    }

    return render_template('index.html', **templateData)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80)
