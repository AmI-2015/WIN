'''
Created on 07/giu/2015

@author: luca
'''

import random

# Status codes
statusCode = {
    0: 'open',
    1: 'closed',
}

# Status codes
STATUS_OPEN = 0
STATUS_CLOSED = 1

def estimateWaitingTime(placeID, restrooms):
    waitingTimeRestrooms = []
    
    for restroom in restrooms:
        waitingTime = 0
        if(restroom['gender'] == "M"):
            minTime = 40  # tempo in secondi
            maxTime = 60
        else:
            minTime = 50
            maxTime = 75

        wc_available = restroom['wc_count'] - restroom['wc_closed_count']
        if(wc_available != 0 and wc_available < restroom['people_count']):
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

        minuti = str(minuti).zfill(2)
        secondi = str(secondi).zfill(2)
        waitingTimeRestrooms.append({'id' : restroom['id'], 'minuti' : minuti, 'secondi' : secondi})
    return waitingTimeRestrooms

def addStatusStrToRestroom(entry, status):
    entry['status_str'] = statusCode[status]

def addInfoToRestroomDict(placeID, restroomDict):
    waitingTimes = estimateWaitingTime(placeID,restroomDict.values())
    for newinfo in waitingTimes:
        entry = restroomDict[newinfo['id']]
        status = entry['status']
        addStatusStrToRestroom(entry, status)
        if(status == STATUS_OPEN):
            entry['waiting_time'] = str(newinfo['minuti'])+":"+str(newinfo['secondi'])
            entry['people_on_wc_available'] = str(entry['people_count'])+'/'+str(entry['wc_available'])
        else:
            entry['waiting_time'] = '--'
            entry['people_on_wc_available'] = '--'

