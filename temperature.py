import RPi.GPIO as GPIO
import time
import Adafruit_DHT
import urllib.request


temp_pin = 2
GPIO.setmode(GPIO.BCM)

while True:
    temperature,humidity = Adafruit_DHT.read_retry(Adafruit_DHT.DHT11,temp_pin)
    if temperature is not None and humidity is not None:
        print("Temperature={0:0.1f}*C Humidity={1:0.1f}%".format(humidity, temperature))
    else:
        print("Error to read data.Try again!")
        time.sleep(3)
    f = urllib.request.urlopen("https://api.thingspeak.com/update?api_key=PQAOVMZ8LLRYZV3E&field1=%s&field2=%s"%(humidity,temperature))
    print(f.read())
    f.close()