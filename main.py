import discord
import asyncio
import pafy

from discord.ext import commands
from discord.ext import tasks
import os
import colorama
import time


intents = discord.Intents.default() #Gotta setup intents so I can get a member list. Discord requires this for privacy or something, its weird
intents.members = True

def getRoleByName(ctx, name): #Turns a role name into a role ID
    allServerRoles = ctx.guild.roles
    for i in allServerRoles:
        if(i.name.lower() == name.lower()):
            return i

def fetchMemberFromId(ctx, id):
    member = ctx.guild.get_member(id)
    return(member)


pyc = __import__("pyconfig")
jsm = __import__("jsonmanager")
ua  = __import__("userActivity")

config = jsm.JsonManager(pyc.configPath)

bot = commands.Bot(command_prefix= config.load()["prefix"], intents=intents)

commandJsonClass = jsm.JsonManager(pyc.commandsPath)
userActivity = ua.UserActivityClass(pyc.userActivityPath, None, bot)

allGroups = []
commandNames = []

tempcommandJson = commandJsonClass.load() #This is me being lazy. Aything with "temp" in it wont be used after like 20 lines at most
tempcommandJson = tempcommandJson['commands']

userActivity.updateFileFormat() #This makes my life SO MUCH EASIER. It automatically updates the format of the userActivity file so I DONT HAVE TO. THAT FILE IS GIANT! 

needRoleUpdate = True

for key in tempcommandJson: #Should probably rework this. This prevents users adding a whole command without rebooting the bot. Users can modify commands and see them change live, but not add or remove. Low priority, but would be nice to improve
    commandNames.append(key)

print(commandNames)

@tasks.loop(hours=24)
async def remove_score():
    print("Daily Reset")
    global needRoleUpdate
    needRoleUpdate = True
    userActivity.addScore(-.5)
    userActivity.pruneUsers()


@bot.event
async def on_ready():
    await bot.change_presence(activity=discord.Game(name=config.load()["prefix"]+"help"))
    remove_score.start()
    userActivity.addScore(.5)
    print("Bot is ready")

@bot.event
async def on_message(ctx):    
    if(ctx.author == bot.user): 
        return           


    print("--------------------------")
    print(f"Author : {ctx.author}")
    print(f"Content: {ctx.content}")


    print("----------")

    userActivity.role = getRoleByName(ctx, config.load()["activeRole"])
    
    userActivity.file = userActivity.jsonManager.load()["users"]
    userActivity.now = time.time()
    
    member = ctx.guild.get_member(int(ctx.author.id))

    if(userActivity.updateActivity(ctx.author.id, ctx.author.name)): #Updates the user's activity score. Returns true if the user'a activity score is above the "active" threshold
        print("adding active role")
        await member.add_roles(userActivity.role)
    else:
        print("removing active role")
        await member.remove_roles(userActivity.role)

    global needRoleUpdate

    if(needRoleUpdate): #so this block adds or removes the active role. My only issue with this is the code only updates YOUR role when YOU send a message. This means active people need to send a message to be deemed "not active". Bad idea but I dont have a better way of doing this so whatever for now
        print("Role doesnt need updating")
        needRoleUpdate = False
        for i in ctx.guild.members:
            try:
                print("User:", i, userActivity.file["users"][str(i.id)])
                if(userActivity.file["users"][str(i.id)]["points"] > 5):
                    print("attempting to add roles")
                    await i.add_roles(userActivity.role)
                    print("adding roles")
                else:
                    print("attempting to remove roles")
                    await i.remove_roles(userActivity.role)
                    print("removing roles")
            except:
                print("User:", i)




    prefix = config.load()["prefix"]
    syntaxArray = ctx.content.split(" ")
    syntax = " ".join(syntaxArray[1:])
    commandJson = commandJsonClass.load()
    commandJson = commandJson['commands']

    if(not ctx.content.startswith(prefix)):
        return

    if(ctx.content.startswith(prefix + "help")): #Iteratively adds all commands and parameters from commands.json to an embed and sends it
        helpEmbed = discord.Embed(title=f"Commands", color=0x00ff00)
        for i in commandJson:
            helpEmbed.add_field(name=f"{i.capitalize()} command", value=f"{prefix}{i}")
            helpEmbed.add_field(name="Required Role", value=f"{commandJson[i]['requiredRole']}")
            helpEmbed.add_field(name="Roles ", value=f"{', '.join(commandJson[i]['roles'])}", inline=False)
        await ctx.channel.send(embed=helpEmbed)
        return #Exits to prevent further commands, so you cannot make a command called help

    if(ctx.content.startswith(prefix + "setName")):
        name = syntax[0]


    if(ctx.content.startswith(prefix + "update")):
        pass

    for command in commandNames: #Iterate through each command to see if the user entered a valid command
        if(ctx.content.startswith(prefix+command)):
            commandObject = commandJson[command]
            userRoles = ctx.author.roles

            if( not (commandObject["requiredRole"] in [i.name.lower() for i in userRoles])): #checks if the user has the required role to perform the command
                await ctx.channel.send("You dont have permission to use this command")
                return

            roleNeedsRemoval = syntax.lower() in [i.name.lower() for i in userRoles] #A clean way of determining if the user has the role or not. Entering the same command will add or remove the role.
            print(f"Role needs removal: {roleNeedsRemoval}")

            if(commandObject["allowedOneRole"]): #This will remove all roles the command can grant. The role the user asked for is added in the next block. There is a parameter to decide if the command should only allow the user to hold one of the roles at a time
                for role in commandObject["roles"]:
                    if(role in [i.name.lower() for i in userRoles]):
                        await ctx.author.remove_roles(getRoleByName(ctx, role))
                        print(f"removed role {role}")

            if(not roleNeedsRemoval): #If the role needs to be added
                await ctx.author.add_roles(getRoleByName(ctx, syntax))
                await ctx.channel.send(f"Added {command} {syntax}")
                print(f"Added role {syntax}")

            else: #If the role needs to be removed
                await ctx.author.remove_roles(getRoleByName(ctx, syntax))
                await ctx.channel.send(f"Removed {command} {syntax}")
                print(f"Removed role {syntax}")
            return

bot.run(config.load()["token"])
