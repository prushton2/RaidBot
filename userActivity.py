import time
jsm = __import__("jsonmanager")


class UserActivityClass:
    def __init__(self, jsonFile, role, bot):
        self.jsonFile = jsonFile
        self.jsonManager = jsm.JsonManager(self.jsonFile)
        self.ExpireTime = self.jsonManager.load()["ActiveRoleExpireTime"]
        self.role = role
        self.bot = bot

    def newUser(self, id, name):
        self.file = self.jsonManager.load()
        self.file["users"][id] = {"name":name, "lastMessageTimestamp":time.time()} 
        self.jsonManager.save(self.file)

    def removeUser(self, id):
        pass

    def updateActivity(self, id, name):
        self.file = self.jsonManager.load()
        try:
            self.file["users"][id]["lastMessageTimestamp"] = time.time()
            self.file["users"][id]["name"] = name
        except:
            self.newUser(id, name)
        self.jsonManager.save(self.file)

        



    