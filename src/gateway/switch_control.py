'''
Created on 28/mag/2015

@author: luca
'''

import RPi.GPIO as GPIO
import time
import requests

inputPin = 13
#outputPin = 15
STATUS_OPEN = 0
STATUS_CLOSED = 1

host = 'localhost:5000'
restroomId = 28
serverUrl = 'http://' + host + '/updatestatus/' + str(restroomId)

def switchcontrol():
	GPIO.setmode(GPIO.BOARD)
	GPIO.setup(inputPin, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
	# GPIO.setup(outputPin, GPIO.OUT)
	# GPIO.output(outputPin, GPIO.HIGH)

	# pulldown resistor on input: when switch is closed input is HIGH, otherwise is LOW
	# Wiring: one end of the switch to VCC and the other one to inputPin
	lastInput = -1  # force update at first loop

	while (True):
		input = GPIO.input(inputPin)
		if (lastInput != input):
			if (input == GPIO.HIGH):
				# Switch closed
				data = { restroomId : STATUS_CLOSED }
			else:
				# Switch open
				data = { restroomId : STATUS_OPEN }
			requests.post(serverUrl, data)
			print "Updated status of restroom id: %s \n data = %s" % (restroomId, data) 
			lastInput = input

		time.sleep(2.3)
