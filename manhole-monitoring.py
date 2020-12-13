#integration code comes here - for all sensors together#
#program for the temperature and distance sensors together uptil now#
import RPi.GPIO as GPIO
import time
import Adafruit_DHT
import urllib.request
import signal
import sys

# set GPIO Pins
pinTrigger = 18
pinEcho = 24
temp_pin = 2


GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

# set GPIO input and output channels
GPIO.setup(pinTrigger, GPIO.OUT)
GPIO.setup(pinEcho, GPIO.IN)

threshold_water_level = 10 #water threshold level in cm

EMULATE_HX711=False

referenceUnit = 1

if not EMULATE_HX711:
    import RPi.GPIO as GPIO
    from hx711 import HX711
else:
    from emulated_hx711 import HX711

def cleanAndExit():
    print("Cleaning...")

    if not EMULATE_HX711:
        GPIO.cleanup()

    print("Bye!")
    sys.exit()

hx = HX711(5, 6) #asssigning the hx711 pins
hx.set_reading_format("MSB", "MSB")
hx.set_reference_unit(0.055)
hx.set_reference_unit(referenceUnit)
#0.044
#-0.045
#0.055
hx.reset()

hx.tare()

print("Add weight now...")

def weight_Sensor():
    val = hx.get_weight(5)
    print(val)
    hx.power_down()
    hx.power_up()
    time.sleep(3)
    weightz = urllib.request.urlopen("https://api.thingspeak.com/update?api_key=PQAOVMZ8LLRYZV3E&field3=%s"%(val))
    print(weightz.read())
    weightz.close()

#######ultrasonic start#########

def close(signal, frame):
    print("\nTurning off ultrasonic distance detection...\n")
    GPIO.cleanup()
    sys.exit(0)
signal.signal(signal.SIGINT, close)


#######ultrasonic end#########

#temperature#
def temp_monitoring():
	temperature,humidity = Adafruit_DHT.read_retry(Adafruit_DHT.DHT11,temp_pin)
	if temperature is not None and humidity is not None:
		print("Temperature={0:0.1f}*C Humidity={1:0.1f}%".format(temperature,humidity))
		print("Agaya yahan")
	else:
	    print("Error to read data.Try again!")
	    time.sleep(3)
	f = urllib.request.urlopen("https://api.thingspeak.com/update?api_key=PQAOVMZ8LLRYZV3E&field1=%s&field2=%s"%(temperature,humidity))
	print(f.read())
	f.close()


def distance_ultrasonic():
    # set Trigger to HIGH
    GPIO.output(pinTrigger, True)
    # set Trigger after 0.01ms to LOW
    time.sleep(0.00001)
    GPIO.output(pinTrigger, False)
    startTime = time.time()
    stopTime = time.time()
    # save start time
    while 0 == GPIO.input(pinEcho):
        startTime = time.time()
        # save time of arrival
    while 1 == GPIO.input(pinEcho):
        stopTime = time.time()
    # time difference between start and arrival
    TimeElapsed = stopTime - startTime
    # multiply with the sonic speed (34300 cm/s)
    # and divide by 2, because there and back
    distance = (TimeElapsed * 34300) / 2
    g = urllib.request.urlopen("https://api.thingspeak.com/update?api_key=PQAOVMZ8LLRYZV3E&field4=%s"%(distance))
    print(g.read())
    g.close()
    print ("Distance: %.1f cm" % distance)

while True:
	temp_monitoring()
	distance_ultrasonic()
	weight_Sensor()