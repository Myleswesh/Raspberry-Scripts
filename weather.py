# -*- coding: UTF-8 -*-
# Doc : http://openweathermap.org/api

import json
import urllib2


api     = 'YourApi'
city    = 'YourCity'
units   = 'Units' #metrics or imperial
lang    = 'en'

jsonWeather = urllib2.urlopen('http://api.openweathermap.org/data/2.5/forecast?q='+ city +'&units='+ units +'&lang='+ lang +'&appid='+ api +'&mode=json')
weather = json.load(jsonWeather)


print weather
