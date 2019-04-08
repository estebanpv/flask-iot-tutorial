from flask import Blueprint, request
from gpiozero import DistanceSensor
import datetime
import time
import urllib


publisher = Blueprint('publisher', __name__)


@publisher.route('/')
def publisher_home():
    return 'This application *sends* data to a Flask in Google Cloud'


@publisher.route('/proximity')
def publisher_proximity():

    sensor = DistanceSensor(trigger=23, echo=24)
    distance = sensor.distance * 100
    sensor = None
    
    distanceStr = '%.1f' % distance
    datetimeStr = datetime.datetime.now().strftime('%Y-%m-%d+%H:%M:%S')

    queryUrl = 'https://esteban-233722.appspot.com/raspberry/proximity/' + datetimeStr + "/" + distanceStr
    return urllib.request.urlopen(queryUrl).read(1000)



'''

### EXAMPLE USING LIBRARY RPi.GPIO

import RPi.GPIO as GPIO
GPIO.setmode(GPIO.BCM)
GPIO.cleanup()

@publisher.route("/proximity")
def publisher_proximity():

    # set GPIO Pins
    pinTrigger = 23
    GPIO.setup(pinTrigger, GPIO.OUT)
    pinEcho = 24
    GPIO.setup(pinEcho, GPIO.IN)

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

    distanceStr = "%.0f" % distance
    datetimeStr = datetime.datetime.now().strftime('%Y-%m-%d+%H:%M:%S')

    queryUrl = "https://esteban-233722.appspot.com/raspberry/proximity/" + datetimeStr + "/" + distanceStr
    return urllib.request.urlopen(queryUrl).read(1000)

'''
