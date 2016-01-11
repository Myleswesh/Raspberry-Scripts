import os
import MySQLdb as mdb
import time
from datetime import datetime


con = mdb.connect('HOST', 'USERNAME', 'PASSWORD', 'DATABASE')
cur = con.cursor()


def tempformat(value):
    return value.replace("temp=", "").replace("'C\n", "")

with con:
    while True:
        value = os.popen('/opt/vc/bin/vcgencmd measure_temp').readline()
        created = str(datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
        print 'Save '+created+': Temp CPU : '+tempformat(value)+''

        cur.execute("INSERT INTO cpu(temp, created) VALUES ('" + tempformat(value) + "', now() ) ")
        con.commit()
        time.sleep(5)
