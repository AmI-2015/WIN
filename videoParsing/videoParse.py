#Install BeautifulSoup and lxml

from bs4 import BeautifulSoup
#from database import DB

address = "http://IP:30003/gateflow.cgi?action=total&id=ID&direction=DIRECTION&begin=BEGIN&end=END&fromReset=value"

markup = BeautifulSoup(open(address), "xml")

#addressTest = '<total><item total="34" direction="IN" id="0" /><item total="117" direction="OUT" id="0" /></total>'
#file = BeautifulSoup(markupTest), "xml")

items = markup.find_all('item')

for item in items:
    if item['direction'] == "IN":
        inCount = item['total']
        print "IN %s" %(inCount)
    else:
        outCount = item['total']
        print "OUT %s" %(outCount)