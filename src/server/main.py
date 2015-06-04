'''
Created on 20/apr/2015

@author: luca
'''

from flask import Flask,render_template, abort
from flask_bootstrap import Bootstrap
from flask.json import jsonify

from database import DB

app = Flask(__name__)
Bootstrap(app)

@app.route('/')
def index():
    #return render_template('index.html')
    return render_template('newtest.html', types = DB.getPlaceTypes())

"""@app.route('/typeRoom/<string:sex>')
def typeRoom(sex):
    return render_template('typeRoom.html', sex=sex)

@app.route('/typeRoom/<string:sex>/numberRoom/<string:type>')
def numberRoom(sex, type):
    return render_template('numberRoom.html', type=type, sex=sex)

@app.route('/typeRoom/<string:sex>/numberRoom/<string:type>/restroomTable/<int:number>')
def restroomTable(sex,type,number):
    return render_template('restroomTable.html', sex=sex, type=type, number=number)"""

@app.route('/placeType/<string:placeType>/')
def placeType(placeType):
    return jsonify(rooms=DB.getPlaceInfoByType(placeType))

@app.route('/place/<int:placeId>/')
def nearRoom(placeId):
    info = DB.getPlaceInfoByID(placeId)
    if info == None:
        abort(404)
    return render_template('place.html', name=info['name'], type=info['type'])

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/contact')
def contact():
    return render_template('contact.html')

if __name__ == '__main__':
    app.run(debug=True)