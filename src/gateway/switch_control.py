'''
Created on 28/mag/2015

@author: luca
'''

import RPi.GPIO as GPIO
import time
import requests
import json

# Physical pins
ledGreen = 3
ledRed = 5
inputPin = 7

STATUS_FORCEUPDATE = -1
#Switch statuses
STATUS_OPEN = 0
STATUS_CLOSED = 1
# Led statuses
STATUS_GREEN = 2
STATUS_RED = 3


restroomId = 28  # Restroom near class 12 'M'

# host = 'localhost:5000'
host = 'simlt.pythonanywhere.com'
updateUrl = 'http://' + host + '/updatestatus/' + str(restroomId) + '/'
getdataUrl = 'http://' + host + '/restroom/' + str(restroomId) + '/'
headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}

def statusCheck():
    # Setup pins
    GPIO.setmode(GPIO.BOARD)
    GPIO.setup(ledGreen, GPIO.OUT)
    GPIO.setup(ledRed, GPIO.OUT)
    GPIO.setup(inputPin, GPIO.IN, pull_up_down=GPIO.PUD_UP)
    # Turn on both leds to check at start
    GPIO.output(ledGreen, GPIO.HIGH)
    GPIO.output(ledRed, GPIO.HIGH)
    time.sleep(0.5)

    # pull-up resistor on input: when switch is closed input is LOW, otherwise is HIGH
    # Wiring: one end of the switch to GND and the other one to inputPin
    input = STATUS_FORCEUPDATE      # force update at first check
    status = STATUS_FORCEUPDATE     # force update at first check

    while (True):
        input = checkSwitch(input)
        status = checkStatus(status)
        print '.'
        time.sleep(5)

def checkSwitch(lastInput):
    input = GPIO.input(inputPin)
    if (lastInput != input):
        if (input == GPIO.HIGH):
            # Switch closed
            data = { 'status' : STATUS_CLOSED }
        else:
            # Switch open
            data = { 'status' : STATUS_OPEN }
        requests.post(updateUrl, data=json.dumps(data), headers=headers)
        print "Updated status of restroom id: %s \n data = %s" % (restroomId, data)
    return input


def checkStatus(oldStatus):
    try:
        r = requests.get(getdataUrl)
        data = r.json()['data']
    except ConnectionError:
        print "Connection Error"
        return oldStatus

    # Turn on red light if out of service or there are more people than WC available
    if data['status'] == STATUS_CLOSED or data['people_count'] >= data['wc_available']:
        newStatus = STATUS_RED
    # Turn on green light otherwise
    else:
        newStatus = STATUS_GREEN

    if oldStatus != newStatus:
        if newStatus == STATUS_RED:
            GPIO.output(ledRed, GPIO.HIGH)
            GPIO.output(ledGreen, GPIO.LOW)
        elif newStatus == STATUS_GREEN: # if STATUS_GREEN
            GPIO.output(ledGreen, GPIO.HIGH)
            GPIO.output(ledRed, GPIO.LOW)
        print "Updated led status: %s" % (newStatus)
    return newStatus

if __name__ == '__main__':
    statusCheck()
