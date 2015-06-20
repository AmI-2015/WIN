'''
Created on 07/giu/2015

@author: luca
'''

import random
from database import DB

# Status codes
statusCode = {
    0: 'open',
    1: 'closed',
}

# Status codes
STATUS_OPEN = 0
STATUS_CLOSED = 1

def updateWaitingTime(restroomID, people):
    if people<0:
        waitingTime='--'
    else:
        restroom = DB.getRestroomInfoByID(restroomID)
        waitingTime = 0
        if(restroom['gender'] == "M"):
            minTime = 40  # tempo in secondi
            maxTime = 60
        else:
            minTime = 50
            maxTime = 75
        if(restroom['wc_available'] != 0 and restroom['wc_available'] < restroom['people_count']):
            if(restroom['wc_available'] > 3):
                numberPeopleInside = restroom['people_count'] - 1  # probabilmente uno si stara' lavando le mani
            else:
                numberPeopleInside = restroom['people_count']  # dato che il bagno e' piu' piccolo forse non ci sara' sempre uno che                                                    # lava le mani
            peopleWaiting = numberPeopleInside - restroom['wc_available']
            for person in range(0, peopleWaiting):
                waitingTime += random.randint(minTime, maxTime)  # aggiunge il tempo di attesa per le persone in coda
            for person in range(0, restroom['wc_available']):
                waitingTime += random.randint(0, maxTime)  # aggiunge il tempo di attesa per le persone che occupano attualmente il bagno
            
            waitingTime = waitingTime // restroom['wc_available']
            minuti = waitingTime // 60
            secondi = waitingTime % 60
        else:
            minuti = 0
            secondi = 0
            
        minuti = str(minuti).zfill(2)
        secondi = str(secondi).zfill(2)
        waitingTime=minuti+":"+secondi
    DB.updateWaitingTimeRestroom(restroomID, waitingTime)

def addStatusStrToRestroom(entry, status):
    entry['status_str'] = statusCode[status]

def addInfoToRestroomDict(restroomDict):
    for restroom in restroomDict.values():
        status = restroom['status']
        addStatusStrToRestroom(restroom, status)
        if(status == STATUS_OPEN):
            restroom['people_on_wc_available'] = str(restroom['people_count'])+'/'+str(restroom['wc_available'])
        else:
            restroom['people_on_wc_available'] = '--'
            
