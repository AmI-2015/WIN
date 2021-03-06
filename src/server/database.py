'''
In this file there are the functions to communicate with the database.
You have to install MySQL and Flask-MySQL.
'''

import os
import ConfigParser
import mysql.connector
from collections import OrderedDict


configParser = ConfigParser.RawConfigParser()

# Prepared statements
stmt_placeID = "SELECT `id`, `name`, `type` FROM `place` WHERE `id` = %s"
stmt_placeName = "SELECT `id`, `name`, `type` FROM `place` WHERE `name` = %s"
stmt_placeType = "SELECT `id`, `name` FROM `place` WHERE `type` = %s ORDER BY `name` ASC"
stmt_placeTypeList = "SELECT DISTINCT `type` FROM `place` WHERE `type` <> 'Restroom'"

stmt_restroomID = "SELECT R.`id`, `people_count`, `wc_count`, `status`, `wc_closed_count`, `gender`, `name`, `type` FROM `restroom` R, `place` P WHERE R.`id` = %s AND R.`id` = P.`id`"
stmt_restroomUpdatePeopleCount = "UPDATE `restroom` SET `people_count` = %s WHERE `id` = %s"
stmt_restroomUpdateStatus = "UPDATE `restroom` SET `status` = %s WHERE `id` = %s"
stmt_restroomUpdateWaitingTime = "UPDATE `restroom` SET `waiting_time` = %s WHERE `id` = %s"

stmt_distanceRestroomList = "SELECT `restroom`, `priority`, `people_count`, `wc_count`, `status`, `wc_closed_count`, `lat`, `long`, `name`, `gender` \
                            FROM `distance`, `restroom` R, `place` P WHERE `place` = %s AND `restroom` = R.`id` AND R.`id` = P.`id` ORDER BY `priority` ASC"
stmt_distanceRestroomListFilterGender = "SELECT `restroom`, `priority`, `people_count`, `wc_count`, `status`, `wc_closed_count`, `lat`, `long`, `name`, `gender`, `waiting_time` \
                            FROM `distance`, `restroom` R, `place` P WHERE `place` = %s AND `gender` = %s AND `restroom` = R.`id` AND R.`id` = P.`id` ORDER BY `priority` ASC"


class Database(object):
    """ String list of place types available """
    types = []

    def __init__(self, cfgFilename):
        """Create a DB object.
        :cfgFilename filename for database connection configuration
        """
        cfgFilename = os.path.join(os.path.dirname(os.path.abspath(__file__)), cfgFilename)
        configParser.read(cfgFilename)
        user = configParser.get('Database', 'user')
        password = configParser.get('Database', 'password')
        host = configParser.get('Database', 'host')
        database = configParser.get('Database', 'database')

        self.conn = mysql.connector.connect(user=user, password=password, host=host, database=database, autocommit=True)
        self.loadInitialData();
    
    def close(self):
        self.conn.close()

    def loadInitialData(self):
        cur = self.conn.cursor()
        # fetch available types for user UI (Exclude restroom)
        cur.execute(stmt_placeTypeList)
        r = cur.fetchall()
        for row in r:
            self.types.append(row[0])
        cur.close()

    def query(self, stmt, params):
        """Return a usable cursor. Remember to close it.
        Reconnect to server if connection times out.
        """
        try:
            cur = self.conn.cursor()
            cur.execute(stmt, params)
        except (AttributeError, mysql.connector.OperationalError):
            self.conn.ping(True)
            cur = self.conn.cursor()
            cur.execute(stmt, params)
        return cur


    """
    Place queries
    """
    def getPlaceInfoByID(self, placeID):
        if isinstance(placeID, int) == False:
            raise TypeError("argument must be of int type")

        cur = self.query(stmt_placeID, (placeID,))
        r = cur.fetchone()
        cur.close()

        if r == None:
            print "Warning: getPlaceInfobyID no entry found for place ID '%s'" %(str(placeID))
            return None

        return {'id': r[0], 'name': r[1], 'type': r[2]}
    
    def getPlaceInfoByName(self, name):
        cur = self.query(stmt_placeName, (name,))
        r = cur.fetchone()
        cur.close()

        if r == None:
            print "Warning: getPlaceInfobyName no entry found for '%s'" %(name)
            return None
        
        return {'id': r[0], 'name': r[1], 'type': r[2]}
    
    def getPlaceInfoByType(self, typestr):
        """ Return a list of places as dictionary { id: 'id', name: 'name' }
        (id, name)
        """
        cur = self.query(stmt_placeType, (typestr,))
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

        cur = self.query(stmt_restroomID, (restroomID,))
        r = cur.fetchone()
        cur.close()

        if r == None:
            print "Warning: getRestroomInfobyID no entry found for restroom ID '%s'" %(str(restroomID))
            return None
        
        return {'id': r[0], 'people_count': r[1], 'wc_count': r[2], 'status': r[3], 'wc_closed_count': r[4],
                'gender': r[5], 'name': r[6], 'type': r[7], 'wc_available' : r[2] - r[4]}
    
    def updateRestroomPeopleCount(self, restroomID, newCount):
        if isinstance(restroomID, int) == False:
            raise TypeError("argument must be of int type")

        cur = self.query(stmt_restroomUpdatePeopleCount, (newCount, restroomID))
        cur.close()

    def updateRestroomStatus(self, restroomID, status):
        if (isinstance(restroomID, int) == False) or (isinstance(restroomID, int) == False):
            raise TypeError("argument must be of int type")

        cur = self.query(stmt_restroomUpdateStatus, (status, restroomID))
        cur.close()

    def updateWaitingTimeRestroom(self, restroomID, waitingTime):
        if(isinstance(restroomID, int) == False):
            raise TypeError("restroomID must be of int type")
        
        cur = self.query(stmt_restroomUpdateWaitingTime, (waitingTime,restroomID))
        cur.close()
        
    """
    Distance queries
    """
    def getPriorityListFromPlace(self, placeID):
        """ Return a dictionary of restrooms having as key the restroomID and as value a dictionary of properties """
        if isinstance(placeID, int) == False:
            raise TypeError("argument must be of int type")

        cur = self.query(stmt_distanceRestroomList, (placeID,))
        r = cur.fetchall()
        cur.close()
        if len(r) == 0:
            print "Warning: getPriorityListFromPlace no entry found for place ID '%s'" %(str(placeID))
        
        restrooms = OrderedDict()
        for rest in r:
            # `restroom`, `priority`, `people_count`, `wc_count`, `status`, `wc_closed_count`, `lat`, `long`
            restrooms[rest[0]] = ({'id': rest[0], 'priority': rest[1], 'people_count': rest[2], 'wc_count': rest[3], 'status': rest[4],
                              'wc_closed_count': rest[5], 'lat': rest[6], 'long': rest[7], 'name': rest[8], 'gender': rest[9],
                              'wc_available' : rest[3] - rest[5]})
        return restrooms
    
    def getPriorityListFromPlaceFilterGender(self, placeID, gender):
        """ Return a dictionary of restrooms filtered by gender having as key the restroomID and as value a dictionary of properties """
        if isinstance(placeID, int) == False:
            raise TypeError("argument must be of int type")

        cur = self.query(stmt_distanceRestroomListFilterGender, (placeID, gender))
        r = cur.fetchall()
        cur.close()
        if len(r) == 0:
            print "Warning: getPriorityListFromPlace no entry found for place ID '%s' and gender '%s'" %(str(placeID),gender)

        restrooms = OrderedDict()
        for rest in r:
            # `restroom`, `priority`, `people_count`, `wc_count`, `status`, `wc_closed_count`, `lat`, `long`, `name`, `gender`
            restrooms[rest[0]] = ({'id': rest[0], 'priority': rest[1], 'people_count': rest[2], 'wc_count': rest[3], 'status': rest[4],
                              'wc_closed_count': rest[5], 'lat': rest[6], 'long': rest[7], 'name': rest[8], 'gender': rest[9],
                              'wc_available' : rest[3] - rest[5], 'waiting_time' : rest[10]})
        return restrooms


""" Instance of Database class to be used.
Avoid creating other instances of the class, otherwise each class will create a new connection!
"""
DB = Database('db.cfg')
