import time
import sys
import urllib.request

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

hx = HX711(5, 6)
hx.set_reading_format("MSB", "MSB")

hx.set_reference_unit(0.055)
hx.set_reference_unit(referenceUnit)

hx.reset()

hx.tare()

print("Add weight now...")



while True:
    try:
        val = hx.get_weight(5)
        print(val)

        hx.power_down()
        hx.power_up()
        time.sleep(3)
        weightz = urllib.request.urlopen("https://api.thingspeak.com/update?api_key=PQAOVMZ8LLRYZV3E&field3=%s"%(val))
        print(weightz.read())
        weightz.close()

    except (KeyboardInterrupt, SystemExit):
        cleanAndExit()