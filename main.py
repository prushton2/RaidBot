import discord
import asyncio
import pafy

from discord.ext import commands
import os
import colorama
import time


def getRoleByName(ctx, name):
    allServerRoles = ctx.guild.roles
    for i in allServerRoles:
        if(i.name.lower() == name.lower()):
            return i

pyc = __import__("pyconfig")
jsm = __import__("jsonmanager")

config = jsm.JsonManager(pyc.configPath)
commandJsonClass = jsm.JsonManager(pyc.commandsPath)

commandNames = []

for key in commandJsonClass.load():
    commandNames.append(key)

bot = commands.Bot(command_prefix= config.load()["prefix"])

@bot.event
async def on_ready():
    await bot.change_presence(activity=discord.Game(name=config.load()["prefix"]+"help"))
    print("Bot is ready")

@bot.event
async def on_message(ctx):
    if(ctx.author == bot.user): 
        return

    prefix = config.load()["prefix"]
    syntaxArray = ctx.content.split(" ")
    syntax = " ".join(syntaxArray[1:])
    commandJson = commandJsonClass.load()

    if(not ctx.content.startswith(prefix)):
        return


    for command in commandNames:
        if(ctx.content.startswith(prefix+command)):
            command = commandJson[command]
            userRoles = ctx.author.roles

            if( not (command["requiredRole"] in [i.name.lower() for i in userRoles])):
                await ctx.channel.send("You dont have permission to use this command")
                return

            roleNeedsRemoval = syntax in [i.name.lower() for i in userRoles]
            
            if(command["allowedOneRole"]):
                for role in command["roles"]:
                    if(role in [i.name.lower() for i in userRoles]):
                        await ctx.author.remove_roles(getRoleByName(ctx, role))

            if(not roleNeedsRemoval):
                await ctx.author.add_roles(getRoleByName(ctx, syntax))
            else:
                await ctx.author.remove_roles(getRoleByName(ctx, syntax))


            return
bot.run(config.load()["token"])
