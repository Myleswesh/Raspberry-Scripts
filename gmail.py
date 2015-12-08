# -*- coding: UTF-8 -*-
# Library : https://github.com/charlierguo/gmail/

import gmail
import time

username = 'MyAdresseMail'  #   Username (without @gmail.com)
password = 'MyPassword'     #   Password

check = gmail.login(username, password)


print('Mail Checker in progress...')
while True :
    inbox = check.inbox().mail(unread=True, prefetch=True)
    if len(inbox) > 0 :
        for mail in inbox :
            print mail.fr           # From
            print mail.sent_at      # At
            print mail.subject      # Subject
    time.sleep(300)                 # Check Every 300 secondes (5 minutes)
