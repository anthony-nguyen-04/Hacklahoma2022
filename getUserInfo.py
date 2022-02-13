import json
import cv2
import imutils
import os
import base64
import pyzbar.pyzbar as pyzbar

def userSearch(id):

    statuses = ["PENDING", "VALID", "INVALID"]

    # userSearch("55f8ba4ce5b34aa211e33648cb0ac367ab7e9ded2c4023a46a1622376d639eb7")
    with open('users.json', 'r') as openfile:
        # Reading from json file
        statusDict = json.load(openfile)

    #data = userDict.get(id)
    foundStatus, data = None, -1

    for status in statuses:
        dict = statusDict.get(status, -1)

        if (dict == -1):
            continue
        else:
            searchData = dict.get(id, -1)

            if (searchData == -1):
                continue
            else:
                data = searchData
                foundStatus = status
                break

    return (foundStatus, data)
    #print(data)

def readQRPicture(picture):
    image = cv2.imread(picture)
    image = imutils.resize(image, height=1000)

    try:
        decoded = pyzbar.decode(image)
        qrCode = (decoded[0].data).decode('utf-8')
        foundStatus, userData = userSearch(qrCode)
    except:
        foundStatus, userData = None, -1

    return (foundStatus, userData)
    #print(userData)

def IDtoQR(id):
    dir_path = os.path.dirname(os.path.realpath(__file__))

    #qrCode = cv2.imread("%s\\users\\%s\\qr.png" % (dir_path, id))

    with open("%s\\users\\%s\\qr.png" % (dir_path, id), "rb") as img_file:
        my_string = base64.b64encode(img_file.read())
        my_string = my_string.decode('utf-8')

    return my_string

