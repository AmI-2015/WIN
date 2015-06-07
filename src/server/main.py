'''
Created on 20/apr/2015

@author: luca
'''

from flask import Flask,render_template, abort, jsonify
from flask_bootstrap import Bootstrap

from database import DB

app = Flask(__name__)
Bootstrap(app)

@app.route('/')
def index():
    #return render_template('index.html')
    return render_template('newtest.html', types = DB.getPlaceTypes())

@app.route('/placeType/<string:placeType>/')
def placeType(placeType):
    return jsonify(rooms=DB.getPlaceInfoByType(placeType))

@app.route('/place/<int:placeID>/')
def nearRestrooms(placeID):
    place = DB.getPlaceInfoByID(placeID)
    if place == None:
        abort(404)
    restrooms=DB.getPriorityListFromPlace(placeID)
    return render_template('place.html', place=place, restrooms=restrooms)

@app.route('/updatestatus/<int:restId>', methods=['POST'])
def switchControl(restId):
    # get the request body
    status = request.json
    Open=status[restId]
    if (Open==0):
        DB.updateRestroomStatus(restId, 0)
    else:
        DB.updateRestroomStatus(restId, 1)

@app.route('/place/<int:placeID>/<string:gender>/')
def nearRestroomsFilterGender(placeID, gender):
    place = DB.getPlaceInfoByID(placeID)
    if place == None:
        abort(404)
    restrooms=DB.getPriorityListFromPlaceFilterGender(placeID, gender)
    return render_template('place.html', place=place, restrooms=restrooms, gender=gender)

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/contact')
def contact():
    return render_template('contact.html')

if __name__ == '__main__':
    app.run(debug=True)
