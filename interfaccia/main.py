'''
Created on 20/apr/2015

@author: luca
'''

from flask import Flask,render_template,url_for
from flask_bootstrap import Bootstrap

app = Flask(__name__)
Bootstrap(app)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/typeRoom/<string:sex>')
def typeRoom(sex):
    return render_template('typeRoom.html', sex=sex)

@app.route('/typeRoom/<string:sex>/numberRoom/<string:type>')
def numberRoom(sex, type):
    return render_template('numberRoom.html', type=type, sex=sex)

@app.route('/typeRoom/<string:sex>/numberRoom/<string:type>/restroomTable/<int:number>')
def restroomTable(sex,type,number):
    return render_template('restroomTable.html', sex=sex, type=type, number=number)

if __name__ == '__main__':
    app.run(debug=True)