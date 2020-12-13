from mq4-cal import *
import sys, time


try:
    print("Press CTRL+C to abort.")
    
    mq = MQ();
    while True:
        perc = mq.MQPercentage()
        sys.stdout.write("\r")
        sys.stdout.write("\033[K")
        sys.stdout.write("LPG: %g ppm, CH4: %g ppm" % (perc["GAS_LPG"], perc["CH4"]))
        sys.stdout.flush()
        time.sleep(0.1)


except:
    print("\nAbort by user")
