'''
Created on 21/mag/2015

@author: Simon Mezzomo
'''

import ConfigParser
import mysql.connector

configParser = ConfigParser.RawConfigParser()


# Prepared statements
stmt_placeID = "SELECT `id`, `name`, `type` FROM `place` WHERE `id` = %s"
stmt_placeName = "SELECT `id`, `name`, `type` FROM `place` WHERE `name` = %s"
stmt_placeType = "SELECT `id`, `name`, `type` FROM `place` WHERE `type` = %s"

stmt_restroomID = "SELECT `id`, `people_count`, `wc_count`, `status`, `wc_closed_count` FROM `restroom` WHERE `id` = %s"
stmt_restroomUpdate = "UPDATE `restroom` SET `people_count` = %s WHERE `id` = %s"

#stmt_distanceRestroomFromPlace = "SELECT `priority` FROM `distance` WHERE `restroom` = %s AND `place` = %s"
stmt_distanceRestroomList = "SELECT `restroom`, `priority` FROM `distance` WHERE `place` = %s"


class Database(object):

    def __init__(self, cfgFilename):
        """Create a DB object.
        :cfgFilename filename for database connection configuration
        """
        configParser.read(cfgFilename)
        user = configParser.get('Database', 'user')
        password = configParser.get('Database', 'password')
        host = configParser.get('Database', 'host')
        database = configParser.get('Database', 'database')
        self.conn = mysql.connector.connect(user=user, password=password, host=host, database=database)
    
    def close(self):
        self.conn.close()

    """
    Place queries
    """
    def getPlaceInfobyID(self, placeID):
        if isinstance(placeID, int) == False:
            raise TypeError("argument must be of int type")

        cur = self.conn.cursor()
        cur.execute(stmt_placeID, (placeID,))
        r = cur.fetchone()
        if r == None:
            print 'Warning: getPlaceInfobyID no entry found for place ID "' + str(placeID) + '"' 
        cur.close()
        
        return {'id': r[0], 'name': r[1], 'type': r[2]}
    
    def getPlaceInfobyName(self, name):
        cur = self.conn.cursor()
        cur.execute(stmt_placeName, (name,))
        r = cur.fetchone()
        if r == None:
            print 'Warning: getPlaceInfobyName no entry found for name "' + name + '"'
        cur.close()
        
        return {'id': r[0], 'name': r[1], 'type': r[2]}
    
    def getPlaceInfobyType(self, typestr):
        cur = self.conn.cursor()
        cur.execute(stmt_placeType, (typestr,))
        r = cur.fetchall()
        if len(r) == 0:
            print 'Warning: getPlaceInfobyType no entry found for type "' + typestr + '"'
        cur.close()
        
        #places = []
        # TODO for row in r:
        return r # {'id': r[0], 'name': r[1], 'type': r[2]}

    """
    Restrooom queries
    """
    def getRestroomInfobyID(self, restroomID):
        if isinstance(restroomID, int) == False:
            raise TypeError("argument must be of int type")

        cur = self.conn.cursor()
        cur.execute(stmt_restroomID, (restroomID,))
        r = cur.fetchone()
        if r == None:
            print 'Warning: getRestroomInfobyID no entry found for restroom ID "' + str(restroomID) + '"'
        cur.close()
        
        return {'id': r[0], 'peopleCount': r[1], 'wcCount': r[2], 'status': r[3], 'wcClosedCount': r[4]}
    
    def updateRestroomPeopleCount(self, restroomID, newCount):
        if isinstance(restroomID, int) == False:
            raise TypeError("argument must be of int type")

        cur = self.conn.cursor()
        cur.execute(stmt_restroomUpdate, (newCount, restroomID))
        self.conn.commit()
        cur.close()

    """
    Distance queries
    """
    def getPriorityListFromPlace(self, placeID):
        if isinstance(placeID, int) == False:
            raise TypeError("argument must be of int type")

        cur = self.conn.cursor()
        cur.execute(stmt_restroomID, (placeID,))
        r = cur.fetchall()
        if len(r) == 0:
            print 'Warning: getPriorityListFromPlace no entry found for place ID "' + str(placeID) + '"' 
        cur.close()
        
        return r
    
""" Instance of Database class to be used.
Avoid creating other instances of the class, otherwise each class will create a new connection!
"""
DB = Database('db.cfg')
