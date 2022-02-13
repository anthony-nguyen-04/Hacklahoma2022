from flask import Flask
from flask import request
from makeNewUser import makeNewUser

app = Flask(__name__)

@app.route('/user/new', methods='POST')
def makeUser():
    if request.method == 'POST':
        id, username = makeNewUser(request.form['name'], request.form['month'], request.form['day'], request.form['year'],
                        request.form['email'], request.form['phone'], request.form['vaccine-one-type'], request.form['vaccine-one-date'],
                        request.form['vaccine-two-type'], request.form['vaccine-two-date'], request.form['vaccine-three-type'],
                        request.form['vaccine-three-date'], request.form['vaccine-card'], request.form['ou-id'], request.form['username'])

        results = {"id" : id, "username" : username}
        return results


if __name__ == '__main__':
   app.run()

#{"name":"Sam Bird","email":"sam.bird@ou.edu","phone":"4057579530","month":"08","day":"29","year":"2002","vaccine-one-type":"pfizer","vaccine-one-date":"02/03/2020","vaccine-two-type":"pfizer","vaccine-two-date":"03/15/2020","vaccine-three-type":"none","vaccine-three-date":"","vaccine-card":"","ou-id":"","username":"sam.bird@ou.edu"}