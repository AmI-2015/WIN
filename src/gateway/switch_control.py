'''
Created on 28/mag/2015

@author: luca
'''

import RPi.GPIO as GPIO
import time
from database import DB

def switchcontrol():
	GPIO.setmode(GPIO.BOARD)
    while (True):
        GPIO.output(15,GPIO.HIGH)
        time.sleep(0.1)
        if(GPIO.input(13)==GPIO.LOW):
            #lo stato basso, cioè uscita in cortocircuito con l'ingresso, indica bagno chiuso (1)
            updateRestroomStatus(ID, 1) 
        else
            updateRestroomStatus(ID, 0)
        GPIO.output(15,GPIO.LOW)
        time.sleep(4.9)
