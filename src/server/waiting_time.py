'''
Created on 07/giu/2015

@author: luca
'''

import random

def waitingTime(placeID, gender,restrooms):
    waitingTimeRestrooms = []
    if(gender=="M"):
        minTime=40 #tempo in secondi
        maxTime=60
    else:
        minTime=50
        maxTime=75
    for restroom in restrooms:
        waitingTime=0
        wc_avaiable=restroom.pop('wc_count')-restroom.pop('wc_closed_count')
        if(wc_avaiable < restroom.pop('people_count')):
            if(wc_avaiable > 3):
                numberPeopleInside=restroom.pop('people_count')-1 #probabilmente uno si starà lavando le mani
            else:
                numberPeopleInside=restroom.pop('people_count') #dato che il bagno è più piccolo forse non ci sarà sempre uno che 
                                                                #lava le mani
            peopleWaiting=numberPeopleInside-wc_avaiable
            for person in range(0,peopleWaiting):
                waitingTime+=random.randint(minTime,maxTime) #aggiunge il tempo di attesa per le persone in coda
            for person in range(0,wc_avaiable):
                waitingTime+=random.randint(0,maxTime) #aggiunge il tempo di attesa per le persone che occupano attualmente il bagno
            waitingTime=waitingTime//wc_avaiable
            minuti=waitingTime//60
            secondi=waitingTime%60
        else:
            minuti=0
            secondi=0
        waitingTimeRestrooms.append({'id' : restroom.pop('id'), 'minuti' : minuti, 'secondi' : secondi})
    return waitingTimeRestrooms
    