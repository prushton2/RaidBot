# RoleBot

This discord bot will be able to give and take away roles at a users command, without admin intervention. The commands will be able to be set in the roles json file,
and the roles each command can access can be set aswell. You can have infinite role commands, and each command can only work for people with a certain role

```javascript
{
    "colors" : {
        "command":"Color", //Command Name
        "requiredRole":"@everyone" //Role required to use the command
        "maxAllowedRoles":1, //Maximum roles allowed at a time from the list. ie: ?color Red; ?color Green; will remove the Red role from the user, as they can only have one role 
        "colors": ["Red", "Blue", "Green"] //Roles this bot can access
    },
    "chatAccess": {
        "command":"chat",
        "requiredRole":"@everyone"
        "maxAllowedRoles":0,
        "roles":["spreadsheets", "lfg", "spam"]
    }
}

```
