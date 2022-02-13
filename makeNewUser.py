import secrets
import json
import cv2
import os
import pyqrcode
import png
from pyqrcode import QRCode
from pictureScanner import scanImage


def makeNewUser(name, monthDOB, dayDOB, yearDOB, email, phone, dose1name, dose1date, dose2name, dose2date,
                dose3name, dose3date, username, card, id):
    hiddenToken = secrets.token_hex(32)
    print(hiddenToken)

    dataDict = {
        "name" : name,
        "DOB" : (("%s/%s/%s") % (monthDOB, dayDOB, yearDOB)),
        "email" : email,
        "phone" : phone,
        "vaccine-one-type" : dose1name,
        "vaccine-one-date" : dose1date,
        "vaccine-two-type": dose2name,
        "vaccine-two-date": dose2date,
        "vaccine-three-type": dose3name,
        "vaccine-three-date": dose3date,
        "username" : username
    }

    userDict = {
        hiddenToken : dataDict
    }

    pendingDict = {}
    pendingDict.update(userDict)

    statusDict = {
        "PENDING" : pendingDict
    }


    qr = pyqrcode.create(hiddenToken)

    dir_path = os.path.dirname(os.path.realpath(__file__))

    if not os.path.exists("%s/users" % (dir_path)):
        os.mkdir("%s/users" % (dir_path))

    if not os.path.exists("%s/users/%s" % (dir_path, hiddenToken)):
        os.mkdir("%s/users/%s" % (dir_path, hiddenToken))

    cv2.imwrite("%s\\users\\%s\\card.jpg" % (dir_path, hiddenToken), card)
    cv2.imwrite("%s\\users\\%s\\id.jpg" % (dir_path, hiddenToken), id)
    qr.png("%s\\users\\%s\\qr.png" % (dir_path, hiddenToken), scale=8)

    # Writing to users.json
    with open("users.json", "r+") as outfile:
        #outfile.write(json_object)
        try:
            data = json.load(outfile)

            # if no PENDING entries, create one
            if data.get("PENDING") == None:
                data.update(statusDict)

            # append to pre-existing PENDING entries
            else:
                data.get("PENDING").update(userDict)

            outfile.seek(0)
            json.dump(data, outfile, indent=4)
        except json.decoder.JSONDecodeError:
            outfile.write(json.dumps(statusDict, indent=4))

    return (hiddenToken, username)

card = scanImage("vaccine.jpg")
id = scanImage("id.jpg")

token, name = makeNewUser("Anthony Nguyen", 11, 18, 2004, "anthonynguyenlaas@gmail.com", "5802917814", "Pfizer", "03/19/2021",
                          "Pfizer", "04/09/2021", "N/A", "N/A", "anthonynguyenlaas@gmail.com", card, id)

#print(token)