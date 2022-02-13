import json
from twilio.rest import Client
from getUserInfo import userSearch

def sendMessage(id, statusState):

    account_sid = 'AC320a7205b268171cf65303da30aab4a1'
    auth_token = '8e7ace7baaeb747d23fe40621dfab7fe'
    client = Client(account_sid, auth_token)

    _, data = userSearch(id)
    name = data.get("name")
    phone = data.get("phone")

    if statusState:
        text = "%s, your passport has been deemed valid." % (name)
    else:
        text = "%s, your passport has been deemed invalid." % (name)

    message = client.messages \
        .create(
        body=text,
        from_='+18455529513',
        to=str('+1'+phone)
    )

def generatePending():
    with open('users.json', 'r') as openfile:
        # Reading from json file
        userDict = json.load(openfile)

    pendingDict = userDict.get("PENDING", -1)

    try:
        pendingList = list(pendingDict.keys())
    except:
        pendingList = []

    return pendingList

def changeStatus(id, statusState):
    # status state is true for valid, false for invalid

    with open('users.json', 'r') as outfile:
        # Reading from json file
        statusDict = json.load(outfile)

        pendingDict = statusDict.get("PENDING")

        data = pendingDict.get(id)
        pendingDict.pop(id)

        userDict = {
            id : data
        }

        if statusState:
            validDict = {}
            validDict.update(userDict)

            validStatusDict = {
                "VALID" : validDict
            }

            # create new VALID tag
            if statusDict.get("VALID") == None:

                statusDict.update(validStatusDict)

            # append to pre-existing VALID entries
            else:
                statusDict.get("VALID").update(userDict)


        else:
            invalidDict = {}
            invalidDict.update(userDict)

            invalidStatusDict = {
                "INVALID": invalidDict
            }

            # create new INVALID tag
            if statusDict.get("INVALID") == None:

                statusDict.update(invalidStatusDict)

            # append to pre-existing INVALID entries
            else:
                statusDict.get("INVALID").update(userDict)


    with open('users.json', 'w') as outfile:
        outfile.seek(0)
        json.dump(statusDict, outfile, indent=4)

    sendMessage(id, statusState)

#changeStatus("b02e73b9168ac391623a7ad05704a4d8e2fc6d66295c7ae234ea6179c22fc100", False)