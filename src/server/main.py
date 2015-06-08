'''
Created on 20/apr/2015

@author: luca
'''

from flask import Flask, render_template, abort, jsonify, request
from flask_bootstrap import Bootstrap

from database import DB
from waiting_time import waitingTime

app = Flask(__name__)
Bootstrap(app)

# Status codes
STATUS_OPEN = 0
STATUS_CLOSED = 1

@app.route('/')
def index():
    return render_template('index.html', types = DB.getPlaceTypes())

@app.route('/placeType/<string:placeType>/')
def placeType(placeType):
    return jsonify(rooms=DB.getPlaceInfoByType(placeType))

@app.route('/place/<int:placeID>/')
def nearRestrooms(placeID):
    place = DB.getPlaceInfoByID(placeID)
    if place == None:
        abort(404)
    restrooms=DB.getPriorityListFromPlace(placeID)
    return render_template('restroom.html', place=place, restrooms=restrooms)

@app.route('/updatestatus/<int:restroomId>/', methods=['POST'])
def switchControl(restroomId):
    # get the request body
    data = request.json
    status = data['status']
    if status == STATUS_CLOSED or status == STATUS_OPEN:
        DB.updateRestroomStatus(restroomId, status)
    else:
        abort(400) # BAD_REQUEST
    # Send a response back for confirmation
    return 'Updated restroom %s status: %s' % (restroomId, status)

@app.route('/place/<int:placeID>/<string:gender>/')
def nearRestroomsFilterGender(placeID, gender):
    place = DB.getPlaceInfoByID(placeID)
    if place == None:
        abort(404)
    restrooms = DB.getPriorityListFromPlaceFilterGender(placeID, gender)
    waiting_time = waitingTime(placeID,gender,restrooms)
    return render_template('restroom.html', place=place, restrooms=restrooms, gender=gender, waitingTime=waiting_time)

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/contact')
def contact():
    return render_template('contact.html')

if __name__ == '__main__':
    app.run(debug=True)
