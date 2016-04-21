import RPi.GPIO as GPIO, time, os
import time

DEBUG = 1
GPIO.setmode(GPIO.BCM)

def RCtime(RCpin):
    reading = 0
    GPIO.setup(RCpin, GPIO.OUT)
    GPIO.output(RCpin, GPIO.LOW)
    time.sleep(0.1)

    GPIO.setup(RCpin, GPIO.IN)
    while (GPIO.input(RCpin) == GPIO.LOW):
        reading += 1
    return reading
while True:
    if RCtime(18) > 1000:
        print ("person walkin")
        time.sleep(3)
