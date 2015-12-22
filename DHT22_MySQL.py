import Adafruit_DHT as dht
import MySQLdb as mdb
import time
from datetime import datetime

con = mdb.connect('YOUR_HOST','YOUR_USERNAME', 'YOUR_PASSWORD', 'YOUR_DATABASE')
cur = con.cursor()

while True:
	with con:
		humidity, temperature = dht.read_retry(dht.DHT22, 4)
		created = str(datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
		print 'Save '+created+': Humidity: '+format(humidity)+' Temperature: '+format(temperature)+''
		cur.execute("INSERT INTO sensors(temp, humidity, created) VALUES ('" + format(temperature) + "', '" + format(humidity) + "', now() ) ")
	time.sleep(50)

# TABLE `sensors` (
#  `id` int(11) NOT NULL AUTO_INCREMENT,
#  `temp` int(11) DEFAULT NULL,
#  `humidity` int(11) DEFAULT NULL,
#  `created` datetime DEFAULT NULL,
#  PRIMARY KEY (`id`)
#) ENGINE=InnoDB AUTO_INCREMENT=354 DEFAULT CHARSET=latin1;
