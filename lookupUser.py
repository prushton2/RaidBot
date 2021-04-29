from lxml import html
import requests
import json
import os



HEADERS = {"X-API-Key" : "d16ea396820e48e7bfec254ab512eec4"}


root_url = "https://www.bungie.net/Platform"

#Items I care about
importantItems = {"Anarchy":"2220014607", "Divinity":"1988948484", "Eyes of Tomorrow":"753200559", "Legend of Acrius":"199171389", "One Thousand Voices":"199171385", "Tarrabah":"2329697053"}
#Enum of what the "state" key means
collectibleState = {0:"Acquired", 1:"Not Acquired", 2:"Obscured", 4:"Invisible", 8:"Cannot Afford Material Requirements", 16:"Inventory Space Unavailable", 32:"Uniqueness Violation", 64:"Purchase Disabled"}


#This is the location of the collections menu incase I forget
# collections = json.loads(res.text)["Response"]["profileCollectibles"]["data"]["collectibles"]

def getUsername(username): #This might seem redundant, but its important: You can enter a profile name into the api, and it will return a username. 
                           #Usernames dont change, profile names do. This simply gets the username from a profile name so it can be saved and referenced  
    url = f"/Destiny2/SearchDestinyPlayer/-1/{username}" 
    res = requests.get(root_url+url, headers=HEADERS)
    print(res.text)
    username = json.loads(res.text)["Response"][0]["displayName"]
    return username


def getCollections(username):
    ## Get the players membershipId
    url = f"/Destiny2/SearchDestinyPlayer/-1/{username}" 
    res = requests.get(root_url+url, headers=HEADERS)
    userInfo = json.loads(res.text)["Response"][0]


    #Get more data from the membershipId and Type
    url = f"/Destiny2/{userInfo['membershipType']}/Profile/{userInfo['membershipId']}/?components=100" 
    res = requests.get(root_url+url, headers=HEADERS)

    userInfo = json.loads(res.text)["Response"]

    #Condense the JSON into variables for ease of use
    membershipType = userInfo['profile']['data']['userInfo']['membershipType']
    destinyMembershipId = userInfo['profile']['data']['userInfo']['membershipId']

    #Get the users collections info
    url = f"/Destiny2/{membershipType}/Profile/{destinyMembershipId}/?components=800"
    res = requests.get(root_url+url, headers=HEADERS)

    return json.loads(res.text)["Response"]

def getImportantItemStatus(username):
    
    collections = getCollections(username)["profileCollectibles"]["data"]["collectibles"]

    collectionsState = {} #Holds the status of the collections state of the items I care about. This is returned to the user 

    for i in importantItems:
        j = importantItems[i]
        collectionsState[i] = not (collections[j]["state"] in [1, 2, 4])

    return collectionsState

print(getImportantItemStatus("Akirro"))