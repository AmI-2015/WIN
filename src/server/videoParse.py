#Install BeautifulSoup and lxml

from bs4 import BeautifulSoup
from database import DB
from waiting_time import updateWaitingTime
import time

address = "http://IP:30003/gateflow.cgi?action=total&id=6&direction=DIRECTION&begin=BEGIN&end=END&fromReset=value"
#addressTest = '<total><item total="34" direction="IN" id="0" /><item total="117" direction="OUT" id="0" /></total>'

def main():
    restID=28
    while(True):
        markup = BeautifulSoup(open(address), "xml")
        #markup = BeautifulSoup(addressTest, "xml")
        
        items = markup.find_all('item')
        
        for item in items:
            if item['direction'] == "IN":
                inCount = item['total']
                print "IN %s" %(inCount)
            else:
                outCount = item['total']
                print "OUT %s" %(outCount)
        
        peopleIN = inCount - outCount
        
        DB.updateRestroomPeopleCount(restID, peopleIN)
        updateWaitingTime(restID,peopleIN)
        
        time.sleep(5)

if __name__ == '__main__':
    main()
