#Install BeautifulSoup and lxml

from bs4 import BeautifulSoup
#from database import DB
import time

address = "http://IP:30003/gateflow.cgi?action=total&id=ID&direction=DIRECTION&begin=BEGIN&end=END&fromReset=value"

while(True):
    markup = BeautifulSoup(open(address), "xml")

    #addressTest = '<total><item total="34" direction="IN" id="0" /><item total="117" direction="OUT" id="0" /></total>'
    #file = BeautifulSoup(markupTest), "xml")

    items = markup.find_all('item')

<<<<<<< HEAD
    for item in items:
        if item['direction'] == "IN":
            inCount = item['total']
            print "IN %s" %(inCount)
        else:
            outCount = item['total']
            print "OUT %s" %(outCount)
            
    time.sleep(5)
=======
for item in items:
    if item['direction'] == "IN":
        inCount = item['total']
        print "IN %s" %(inCount)
    else:
        outCount = item['total']
        print "OUT %s" %(outCount)
        
peopleIN = inCount - outCount
>>>>>>> 6aa8da1d970e4430c2b6dba8f3c4eeef60d16076
