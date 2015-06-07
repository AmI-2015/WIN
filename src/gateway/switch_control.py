'''
Created on 28/mag/2015

@author: luca
'''

import RPi.GPIO as GPIO
import time
import requests

def switchcontrol():
	GPIO.setmode(GPIO.BOARD)
	Id=28
	serverUrl='http://localhost:5000/updatestatus/'+Id
	last=GPIO.LOW
	flag=False
	while (True):
		GPIO.output(15,GPIO.HIGH)
		time.sleep(0.1)
		Input=GPIO.input(13)
		if (last != Input and flag):
			if(Input==GPIO.LOW):
				#lo stato basso, cioe uscita in cortocircuito con l'ingresso, indica bagno chiuso (1)
				data={ Id : 1}
				requests.post(serverUrl, data)
			else:
				data={ Id : 0}
				requests.post(serverUrl, data)
		last=GPIO.input(13)
		flag=True
		GPIO.output(15,GPIO.LOW)
		time.sleep(2.3)
