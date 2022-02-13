import secrets
import json
import cv2
import os
import pyqrcode
import png
from pyqrcode import QRCode
from pictureScanner import scanImage


def makeNewUser(name, monthDOB, dayDOB, yearDOB, email, phone, dose1name, dose1month, dose1day, dose1year,
                dose2name, dose2month, dose2day, dose2year, dose3name, dose3month, dose3day, dose3year, card, id):
    hiddenToken = secrets.token_hex(32)
    print(hiddenToken)

    dataDict = {
        "name" : name,
        "DOB" : (("%s/%s/%s") % (monthDOB, dayDOB, yearDOB)),
        "email" : email,
        "phone" : phone,
        "dose1name" : dose1name,
        "dose1date": (("%s/%s/%s") % (dose1month, dose1day, dose1year)),
        "dose2name": dose2name,
        "dose2date": (("%s/%s/%s") % (dose2month, dose2day, dose2year)),
        "dose3name": dose3name,
        "dose3date": (("%s/%s/%s") % (dose3month, dose3day, dose3year)),
    }

    userDict = {
        hiddenToken : dataDict
    }

    qr = pyqrcode.create(hiddenToken)

    dir_path = os.path.dirname(os.path.realpath(__file__))

    if not os.path.exists("%s/users/%s" % (dir_path, hiddenToken)):
        #os.mkdir("%s/users" % (dir_path))
        os.mkdir("%s/users/%s" % (dir_path, hiddenToken))

    cv2.imwrite("%s\\users\\%s\\card.jpg" % (dir_path, hiddenToken), card)
    cv2.imwrite("%s\\users\\%s\\id.jpg" % (dir_path, hiddenToken), id)
    qr.png("%s\\users\\%s\\qr.png" % (dir_path, hiddenToken), scale=6)

    # Serializing json
    json_object = json.dumps(userDict, indent=4)

    # Writing to sample.json
    with open("users.json", "a") as outfile:
        outfile.write(json_object)

card = scanImage("vaccine.jpg")
id = scanImage("id.jpg")

makeNewUser("Anthony Nguyen", 11, 18, 2004, "anthonynguyenlaas@gmail.com", 5802917814, "Pfizer", 3, 19, 2021,
            "Pfizer", 4, 9, 21, "N/A", -1, -1, -1, card, id)

