# RoleBot

This discord bot is designed to meet the needs of a Destiny 2 LFG Server. The bot is built to be able to be used by anyone else with heavy use of json files. 


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


config.json: 
```javascript
{
    "activeRole":"Active", //The role name of people who are active
    "prefix":"<Desired prefix goes here>",
    "token":"<Paste bot token here>"

}
```

The userActivity.json file only needs to be initialized to this, nothing else needs to be done to it.

userActivity.json
```javascript
{
    "ActiveRoleExpireTime": 604800, //Number of seconds until the active role expires. Is set to 1 week by default
    "users": {
        
    }
}
```