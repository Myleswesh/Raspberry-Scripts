from ttrss.client import TTRClient
import RPi.GPIO as GPIO
import time

client = TTRClient('http://raspberry.local', 'YOUR_USERNAME', 'YOUR_PASSWORD')
client.login()

RGB = [17, 27, 22]
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

for pin in RGB:
        GPIO.setup(pin, GPIO.OUT)
        GPIO.output(pin, GPIO.LOW)

try:
    while True:
        count   = client.get_unread_count()
        if count > 0:
            print count
            GPIO.output(17, True)   # Red On
            GPIO.output(27, False)  # Green Off
        else:
            print 'Nothing to read.'
            GPIO.output(17, False)   # Red Off
            GPIO.output(27, True)    # Green On
        time.sleep(3)

except KeyboardInterrupt:
    GPIO.cleanup()

except:
    GPIO.output(17, False)      # Red Off
    GPIO.output(27, False)      # Green Off
    GPIO.output(22, True)       # Blue On
