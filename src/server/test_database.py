'''
Created on 24/mag/2015

@author: Simon Mezzomo
'''

from database import DB



def test():
    print DB.getPlaceInfobyID(1)

    class12 = DB.getPlaceInfobyName('Classroom 12')
    print class12['name'], class12['type']

    print DB.getPlaceInfobyName('Studyroom nord')
    
    print DB.getPlaceInfobyType('restroom')
    
    DB.updateRestroomPeopleCount(3, 4)

    print DB.types

    DB.close()


if __name__ == "__main__":
    test()