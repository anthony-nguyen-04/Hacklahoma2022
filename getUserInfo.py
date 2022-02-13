import json
import numpy as np
import cv2
import imutils
import pyzbar.pyzbar as pyzbar

def userSearch(id):
    # userSearch("55f8ba4ce5b34aa211e33648cb0ac367ab7e9ded2c4023a46a1622376d639eb7")
    with open('users.json', 'r') as openfile:
        # Reading from json file
        userDict = json.load(openfile)

    data = userDict.get(id)
    return data
    #print(data)

def readQRPicture(picture):
    image = cv2.imread(picture)
    image = imutils.resize(image, height=1000)

    decoded = pyzbar.decode(image)
    qrCode = (decoded[0].data).decode('utf-8')
    userData = userSearch(qrCode)

    return userData
    #print(userData)

#print(readQRPicture("qrtest.jpg"))