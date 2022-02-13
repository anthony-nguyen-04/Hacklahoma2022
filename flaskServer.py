from flask import Flask
from flask import request
import base64
from makeNewUser import makeNewUser

app = Flask(__name__)

@app.route('/user/new', methods=['GET', 'POST'])
def makeUser():
    if request.method == 'POST':

        card = request.files['vaccine-card']
        print(card)
        card = base64.b64encode(card.read())
        card = card.decode('utf-8')

        ouid = request.files['ou-id']
        ouid = base64.b64encode(ouid.read())
        ouid = ouid.decode('utf-8')

        uid, username = makeNewUser(request.form['name'], request.form['month'], request.form['day'],
                                   request.form['year'],
                                   request.form['email'], request.form['phone'], request.form['vaccine-one-type'],
                                   request.form['vaccine-one-date'],
                                   request.form['vaccine-two-type'], request.form['vaccine-two-date'],
                                   request.form['vaccine-three-type'],
                                   request.form['vaccine-three-date'], card, ouid, request.form['username'])

        results = {"id" : uid, "username" : username}
        return results


if __name__ == '__main__':
   app.run()

#{"name":"Sam Bird","email":"sam.bird@ou.edu","phone":"4057579530","month":"08","day":"29","year":"2002","vaccine-one-type":"pfizer","vaccine-one-date":"02/03/2020","vaccine-two-type":"pfizer","vaccine-two-date":"03/15/2020","vaccine-three-type":"none","vaccine-three-date":"","vaccine-card":"","ou-id":"","username":"sam.bird@ou.edu"}
