import time
jsm = __import__("jsonmanager")


class UserActivityClass:
    def __init__(self, jsonFile, role, bot):
        self.jsonFile = jsonFile
        self.jsonManager = jsm.JsonManager(self.jsonFile)
        self.ExpireTime = self.jsonManager.load()["ActiveRoleExpireTime"]
        self.role = role
        self.bot = bot
        self.version = 2.0

    def newUser(self, id, name):
        self.file = self.jsonManager.load()
        self.file["users"][id] = {"name":name, "points":0, "lastMessageTimestamp":time.time()} 
        self.jsonManager.save(self.file)

    def removeUser(self, id):
        pass

    def updateFileFormat(self):
        self.file = self.jsonManager.load()
        print("reading version")
        if(self.file["version"] != self.version):
            print("needs version update")
            for i in self.file["users"]:
                self.file["users"][i]["points"] = 0
        else:
            print("file doesnt need updating")
        self.file["version"] = self.version
        self.jsonManager.save(self.file)
        

    def removeScore(self): # removes 1 point from everyone.
        self.file = self.jsonManager.load()
        
        for i in self.file["users"]:
            self.file["users"][id]["points"] -= 1
            self.file["users"][id]["points"] = max(self.file["users"][id]["points"], 0)
        
        self.jsonManager.save(self.file)
        


    def updateActivity(self, id, name):
        self.file = self.jsonManager.load()
        id = str(id)
        messageSpamTimeout = 60 #in seconds, used to not add points while a user is spamming
        try:
            self.file["users"][id]["name"] = name
            self.file["users"][id]["lastMessageTimestamp"] = time.time()

            if(self.file["users"][id]["lastMessageTimestamp"] < time.time() - 60): #prevent message spam to add up points too quickly
                self.file["users"][id]["points"] += 1

            self.file["users"][id]["points"] = min(self.file["users"][id]["points"], 10) #max a users points at 10
        except:
            self.newUser(id, name)
        self.jsonManager.save(self.file)

        return self.file["users"][id]["points"] >= 5

        



    