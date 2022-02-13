from flask import Flask
from flask import request
import base64
import os
from makeNewUser import makeNewUser
from getUserInfo import userSearch
from getUserInfo import IDtoQR
from getUserInfo import readQRPicture
from validateUserInfo import changeStatus
from validateUserInfo import generatePending

app = Flask(__name__)

@app.route('/user/new', methods=['GET', 'POST'])
def makeUser():
    if request.method == 'POST':

        card = request.files['vaccine-card']
        card = base64.b64encode(card.read())
        card = card.decode('utf-8')

        ouid = request.files['ou-id']
        ouid = base64.b64encode(ouid.read())
        ouid = ouid.decode('utf-8')

        uid = makeNewUser(request.form['name'], request.form['month'], request.form['day'],
                                   request.form['year'],
                                   request.form['email'], request.form['phone'], request.form['vaccine-one-type'],
                                   request.form['vaccine-one-date'],
                                   request.form['vaccine-two-type'], request.form['vaccine-two-date'],
                                   request.form['vaccine-three-type'],
                                   request.form['vaccine-three-date'], card, ouid)

        results = uid
        return results




@app.route('/user/info', methods=['GET', 'POST'])
def info():
    if request.method == 'POST':
        uid = request.form["id"]

        status, data = userSearch(uid)

        qrB64 = IDtoQR(uid)

        output = {
            "status" : status,
            "info" : data,
            "qrb64" : qrB64
        }

        return output


@app.route('/validator/code', methods=['GET', 'POST'])
def validate():
    if request.method == 'POST':

        frame = request.files['data']
        frame = base64.b64encode(frame.read())
        frame = frame.decode('utf-8')

        uid = readQRPicture(frame)

        return uid

@app.route('/admin/status', methods=['GET', 'POST'])
def adminStatus():
    if request.method == 'POST':

        uid = request.form["id"]
        statusState = request.form["status"]

        changeStatus(uid, statusState)

@app.route('/admin/pending', methods=['GET', 'POST'])
def pending():
    if request.method == 'GET':

        pending = generatePending()

        return pending

@app.route('/admin/data', methods=['GET', 'POST'])
def data():
    if request.method == 'POST':
        uid = request.form["id"]

        status, data = userSearch(uid)

        dir_path = os.path.dirname(os.path.realpath(__file__))

        with open("%s\\users\\%s\\card.jpg" % (dir_path, uid), "rb") as img_file:
            cardb64 = base64.b64encode(img_file.read())

        with open("%s\\users\\%s\\id.jpg" % (dir_path, uid), "rb") as img_file:
            idb64 = base64.b64encode(img_file.read())

        output = {
            "status": status,
            "info": data,
            "cardb64": cardb64,
            "idb64": idb64
        }

if __name__ == '__main__':
   app.run()

#{"name":"Sam Bird","email":"sam.bird@ou.edu","phone":"4057579530","month":"08","day":"29","year":"2002","vaccine-one-type":"pfizer","vaccine-one-date":"02/03/2020","vaccine-two-type":"pfizer","vaccine-two-date":"03/15/2020","vaccine-three-type":"none","vaccine-three-date":"","vaccine-card":"","ou-id":"","username":"sam.bird@ou.edu"}
