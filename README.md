# RoleBot

This discord bot will be able to give and take away roles at a users command, without admin intervention. The commands will be able to be set in the roles json file,
and the roles each command can access can be set aswell. You can have infinite role commands, and each command can only work for people with a certain role

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


Config.json: 
```javascript
{
  "prefix":"<Desired prefix goes here>",
  "token":"<Paste bot token here>"
}
```