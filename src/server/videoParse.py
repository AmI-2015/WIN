'''
This is the parser for information provided by the video server.
You have to install Untangle.
'''

from database import DB
from waiting_time import updateWaitingTime
import time
import untangle

address = "http://IP:30003/gateflow.cgi?action=total&id=6&direction=DIRECTION&begin=BEGIN&end=END&fromReset=value"
#addressTest = '<total><item total="34" direction="IN" id="0" /><item total="117" direction="OUT" id="0" /></total>'

def main():
    restID=28
    while(True):
        markup = untangle.parse(address)
        items = markup.Total.Item
        
        itemIN = items[0]
        inCount = itemIN['Total']
        #print "IN %s" %(inCount)
        
        itemOUT = items[1]
        outCount = itemOUT['Total']
        #print "OUT %s" %(outCount)
        
        peopleIN = int(inCount) - int(outCount)
        
        DB.updateRestroomPeopleCount(restID, peopleIN)
        updateWaitingTime(restID,peopleIN)
        
        time.sleep(5)

if __name__ == '__main__':
    main()
