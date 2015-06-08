'''
Created on 07/giu/2015

@author: luca
'''

import random

def waitingTime(placeID, gender, restrooms):
    waitingTimeRestrooms = []
    if(gender == "M"):
        minTime = 40  # tempo in secondi
        maxTime = 60
    else:
        minTime = 50
        maxTime = 75
    for restroom in restrooms:
        waitingTime = 0
        wc_available = restroom['wc_count'] - restroom['wc_closed_count']
        if(wc_available < restroom['people_count']):
            if(wc_available > 3):
                numberPeopleInside = restroom['people_count'] - 1  # probabilmente uno si stara' lavando le mani
            else:
                numberPeopleInside = restroom['people_count']  # dato che il bagno e' piu' piccolo forse non ci sara' sempre uno che
                                                                # lava le mani
            peopleWaiting = numberPeopleInside - wc_available
            for person in range(0, peopleWaiting):
                waitingTime += random.randint(minTime, maxTime)  # aggiunge il tempo di attesa per le persone in coda
            for person in range(0, wc_available):
                waitingTime += random.randint(0, maxTime)  # aggiunge il tempo di attesa per le persone che occupano attualmente il bagno
            waitingTime = waitingTime // wc_available
            minuti = waitingTime // 60
            secondi = waitingTime % 60
        else:
            minuti = 0
            secondi = 0
        waitingTimeRestrooms.append({'id' : restroom['id'], 'minuti' : minuti, 'secondi' : secondi})
    return waitingTimeRestrooms
