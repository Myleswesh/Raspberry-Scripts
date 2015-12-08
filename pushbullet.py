# -*- coding: UTF-8 -*-
# Library : https://pypi.python.org/pypi/pushbullet.py

from pushbullet import Pushbullet

api_key = 'MyApiKeyHere'
pb = Pushbullet(api_key)     
device_to  = pb.devices[0]    # 0 = MyPhone, 1 = MyTablet, none = All Devices
                           
def reboot():
    subject = '[Raspberry] Reboot'
    content = 'Reboot in progress !'

    return pb.push_note(subject, content, device=device_to)

reboot()

