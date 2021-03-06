'''
This is the main page that runs the server.
You have to install Flask and Flask Bootstrap.
'''

from flask import Flask, render_template, abort, jsonify, request
from flask_bootstrap import Bootstrap

from database import DB
from waiting_time import addInfoToRestroomDict, addStatusStrToRestroom, updateWaitingTime

app = Flask(__name__)
Bootstrap(app)

# Status codes
STATUS_OPEN = 0
STATUS_CLOSED = 1

@app.route('/')
def index():
    # Get a list of all restrooms, the priority order doesn't matter
    defaultPlaceID = 1;
    return render_template('index.html', types = DB.getPlaceTypes(), restrooms=DB.getPriorityListFromPlace(defaultPlaceID).values())

@app.route('/placeType/<string:placeType>/')
def placeType(placeType):
    return jsonify(rooms=DB.getPlaceInfoByType(placeType))

@app.route('/restroom/<int:restroomID>/')
def restroomData(restroomID):
    return jsonify(data=DB.getRestroomInfoByID(restroomID))

'''@app.route('/place/<int:placeID>/')
def nearRestrooms(placeID):
    place = DB.getPlaceInfoByID(placeID)
    if place == None:
        abort(404) # Invalid place ID
    restroomDict = DB.getPriorityListFromPlace(placeID)
    addInfoToRestroomDict(placeID, restroomDict)
    return render_template('restroom.html', place=place, restrooms=restroomDict.values())'''

@app.route('/place/<int:placeID>/<string:gender>/')
def nearRestroomsFilterGender(placeID, gender):
    place = DB.getPlaceInfoByID(placeID)
    if place == None:
        abort(404) # Invalid place ID
    restroomDict = DB.getPriorityListFromPlaceFilterGender(placeID, gender)
    addInfoToRestroomDict(restroomDict)
    return render_template('restroom.html', place=place, restrooms=restroomDict.values())

@app.route('/updatestatus/<int:restroomId>/', methods=['POST'])
def switchControl(restroomId):
    if DB.getRestroomInfoByID(restroomId) == None:
        abort(404) # Invalid restroom ID
    # get the request body
    data = request.json
    status = data['status']
    if status == STATUS_CLOSED:
        DB.updateRestroomStatus(restroomId, status)
        DB.updateRestroomPeopleCount(restroomId, 0)
        updateWaitingTime(restroomId,-1)
    elif status == STATUS_OPEN:
        DB.updateRestroomStatus(restroomId, status)
        DB.updateRestroomPeopleCount(restroomId, 0)
        updateWaitingTime(restroomId, 0)
    else:
        abort(400) # BAD_REQUEST
    # Send a response back for confirmation
    return 'Updated restroom %s status: %s' % (restroomId, status)

@app.route('/monitorRestroom/<int:restID>/')
def nearRestroomsInsideOtherRestroom(restID):
    restroom = DB.getRestroomInfoByID(restID)
    if restroom == None:
        abort(404) # Invalid place ID
    addStatusStrToRestroom(restroom, restroom['status'])
    restroomDict = DB.getPriorityListFromPlaceFilterGender(restID, restroom['gender'])
    addInfoToRestroomDict(restroomDict)
    return render_template('restroomInside.html', restroom=restroom, restrooms=restroomDict.values())

@app.route('/about')
def about():
    return render_template('about.html')

if __name__ == '__main__':
    app.run(debug=True)
