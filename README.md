# RaidBot

This discord bot is designed to meet the needs of a Destiny 2 LFG Server. The bot is built to be able to be used by anyone else with heavy use of json files. 
<br>Activity role is automatically applied and removed. Users gain points for messages sent. 5 points grants the active role, and a user can have 10 points maximum. one point is removed every 24 hours.
<br>Users can acquire roles of certain weapons from the Bungie.net API  that can be found <a href="https://bungie-net.github.io/multi/index.html">here</a>. Users can enter their name and the bot will save their name.

commands.json
```javascript


{
    "color" : { //Command Name
        "requiredRole":"@everyone", //Role required to use the command
        "allowedOneRole":true , //if the user can only have one role from the list at a time. Bot will remove all roles then add the requested role
        "colors": ["Red", "Blue", "Green"] //Roles this bot can access
    },
    "chat": {
        "requiredRole":"@everyone",
        "allowedOneRole":false,
        "roles":["spreadsheets", "lfg", "spam"]
    }
}

```

pyconfig.py
```python


commandsPath = "path-to-commands.json"
configPath = "path-to-config.json"
userDataPath = "path-to-userData.json"
seperator = "\\"

```

config.json: 
```javascript
{
    "activeRole":"Active", //The role name of people who are active
    "prefix":"<Desired prefix goes here>",
    "token":"<Paste bot token here>"

}
```

The userActivity.json file only needs to be initialized to this, nothing else needs to be done to it.

userData.json
```javascript
{
    "ActiveRoleExpireTime": 604800, //Number of seconds until the active role expires. Is set to 1 week by default
    "version": 1.0,
    "users": {
        
    }
}
```

<br><br>
TODO:
* Delete inactive users from userActivity.json
* Add the base username to the userActivity.json file
* Restructure command setup to allow built in commands