'''
Created on 24/mag/2015

@author: Simon Mezzomo
'''

from database import DB


def test():
    print DB.getPlaceInfoByID(1)

    class12 = DB.getPlaceInfoByName('12')
    print class12['id'], class12['name'], class12['type']

    print DB.getPlaceInfoByName('Studyroom nord')
    
    print DB.getPlaceInfoByType('restroom')
    
    DB.updateRestroomPeopleCount(3, 4)

    print DB.types
    
    print DB.getPriorityListFromPlace(class12['id'])
    print DB.getPriorityListFromPlaceFilterGender(class12['id'], 'M')

    DB.close()


if __name__ == "__main__":
    test()