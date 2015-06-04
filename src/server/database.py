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
stmt_placeType = "SELECT `id`, `name` FROM `place` WHERE `type` = %s ORDER BY `name` ASC"
stmt_placeTypeList = "SELECT DISTINCT `type` FROM `place`"

stmt_restroomID = "SELECT `id`, `people_count`, `wc_count`, `status`, `wc_closed_count` FROM `restroom` WHERE `id` = %s"
stmt_restroomUpdatePeopleCount = "UPDATE `restroom` SET `people_count` = %s WHERE `id` = %s"
stmt_restroomUpdateStatus = "UPDATE `restroom` SET `status` = %s WHERE `id` = %s"

#stmt_distanceRestroomFromPlace = "SELECT `priority` FROM `distance` WHERE `restroom` = %s AND `place` = %s"
stmt_distanceRestroomList = "SELECT `restroom`, `priority` FROM `distance` WHERE `place` = %s ORDER BY `priority` ASC"
stmt_distanceRestroomListFilterGender = "SELECT `restroom`, `priority` FROM `distance`, `restroom` WHERE `place` = %s AND `gender` = %s ORDER BY `priority` ASC"


class Database(object):
    """ String list of place types available """
    types = []

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
        
        self.loadInitialData();
    
    def close(self):
        self.conn.close()

    def loadInitialData(self):
        cur = self.conn.cursor()
        # fetch available types
        cur.execute(stmt_placeTypeList)
        r = cur.fetchall()
        for row in r:
            self.types.append(row[0])
        cur.close()

    """
    Place queries
    """
    def getPlaceInfoByID(self, placeID):
        if isinstance(placeID, int) == False:
            raise TypeError("argument must be of int type")

        cur = self.conn.cursor()
        cur.execute(stmt_placeID, (placeID,))
        r = cur.fetchone()
        cur.close()

        if r == None:
            print "Warning: getPlaceInfobyID no entry found for place ID '%s'" %(str(placeID))
            return None

        return {'id': r[0], 'name': r[1], 'type': r[2]}
    
    def getPlaceInfoByName(self, name):
        cur = self.conn.cursor()
        cur.execute(stmt_placeName, (name,))
        r = cur.fetchone()
        cur.close()

        if r == None:
            print "Warning: getPlaceInfobyName no entry found for '%s'" %(name)
            return None
        
        return {'id': r[0], 'name': r[1], 'type': r[2]}
    
    def getPlaceInfoByType(self, typestr):
        """ Return a list of places as dictionary { id: 'id', name: 'name' }
        (id, name, type)
        """
        cur = self.conn.cursor()
        cur.execute(stmt_placeType, (typestr,))
        r = cur.fetchall()
        if len(r) == 0:
            print "Warning: getPlaceInfobyType no entry found for type '%s'" %(typestr)
        cur.close()
        
        places = []
        for item in r:
            places.append({'id': item[0], 'name': item[1]})
        return places
    
    def getPlaceTypes(self):
        """Return a list of place types available"""
        return self.types

    """
    Restrooom queries
    """
    def getRestroomInfoByID(self, restroomID):
        if isinstance(restroomID, int) == False:
            raise TypeError("argument must be of int type")

        cur = self.conn.cursor()
        cur.execute(stmt_restroomID, (restroomID,))
        r = cur.fetchone()
        cur.close()

        if r == None:
            print "Warning: getRestroomInfobyID no entry found for restroom ID '%s'" %(str(restroomID))
            return None
        
        return {'id': r[0], 'peopleCount': r[1], 'wcCount': r[2], 'status': r[3], 'wcClosedCount': r[4]}
    
    def updateRestroomPeopleCount(self, restroomID, newCount):
        if isinstance(restroomID, int) == False:
            raise TypeError("argument must be of int type")

        cur = self.conn.cursor()
        cur.execute(stmt_restroomUpdatePeopleCount, (newCount, restroomID))
        self.conn.commit()
        cur.close()

    def updateRestroomStatus(self, restroomID, status):
        if (isinstance(restroomID, int) == False) or (isinstance(restroomID, int) == False):
            raise TypeError("argument must be of int type")

        cur = self.conn.cursor()
        cur.execute(stmt_restroomUpdateStatus, (status, restroomID))
        self.conn.commit()
        cur.close()

    """
    Distance queries
    """
    def getPriorityListFromPlace(self, placeID):
        if isinstance(placeID, int) == False:
            raise TypeError("argument must be of int type")

        cur = self.conn.cursor()
        cur.execute(stmt_distanceRestroomList, (placeID,))
        r = cur.fetchall()
        if len(r) == 0:
            print "Warning: getPriorityListFromPlace no entry found for place ID '%s'" %(str(placeID)) 
        cur.close()
        
        return r
    
    def getPriorityListFromPlaceFilterGender(self, placeID, gender):
        if isinstance(placeID, int) == False:
            raise TypeError("argument must be of int type")

        cur = self.conn.cursor()
        cur.execute(stmt_distanceRestroomListFilterGender, (placeID, gender))
        r = cur.fetchall()
        if len(r) == 0:
            print "Warning: getPriorityListFromPlace no entry found for place ID '%s' and gender '%s'" %(str(placeID),gender) 
        cur.close()
        
        return r


""" Instance of Database class to be used.
Avoid creating other instances of the class, otherwise each class will create a new connection!
"""
DB = Database('db.cfg')
