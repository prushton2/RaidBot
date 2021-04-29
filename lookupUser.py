from lxml import html
import requests
import json
import os

jsonmanager = __import__("JsonManager")

HEADERS = {"X-API-Key" : "d16ea396820e48e7bfec254ab512eec4"}

workingFilejson = jsonmanager.JsonManager("C:\\Users\\Peter\\Documents\\code\\py\\Bungie net api\\workingFile.json")
outputjson = jsonmanager.JsonManager("C:\\Users\\Peter\\Documents\\code\\py\\Bungie net api\\output.json")

membershipType = -1
root_url = "https://www.bungie.net/Platform"
displayName = "Soul2956"

importantItems = {"Anarchy":"2220014607", "Divinity":"1988948484", "Eyes of Tomorrow":"753200559", "Legend of Acrius":"199171389", "One Thousand Voices":"199171385", "Tarrabah":"2329697053"}
collectibleState = {0:"Acquired", 1:"Not Acquired", 2:"Obscured", 4:"Invisible", 8:"Cannot Afford Material Requirements", 16:"Inventory Space Unavailable", 32:"Uniqueness Violation", 64:"Purchase Disabled"}

## Get the players membershipId
url = f"/Destiny2/SearchDestinyPlayer/{membershipType}/{displayName}" 
res = requests.get(root_url+url, headers=HEADERS)
userInfo = json.loads(res.text)["Response"][0]

#Get more data from the membershipId
url = f"/Destiny2/{userInfo['membershipType']}/Profile/{userInfo['membershipId']}/?components=100" 
res = requests.get(root_url+url, headers=HEADERS)

##save data in userInfo
userInfo = json.loads(res.text)["Response"]

characterId = userInfo['profile']['data']['characterIds'][0]
membershipType = userInfo['profile']['data']['userInfo']['membershipType']
destinyMembershipId = userInfo['profile']['data']['userInfo']['membershipId']

# print(membershipType, des)

url = f"/Destiny2/{membershipType}/Profile/{destinyMembershipId}/?components=800"
res = requests.get(root_url+url, headers=HEADERS)

outputjson.save(json.loads(res.text))

collections = json.loads(res.text)["Response"]["profileCollectibles"]["data"]["collectibles"]


for i in importantItems:
    j = importantItems[i]
    print(f"{i}: ", end="")
    print(collectibleState[collections[j]["state"]])