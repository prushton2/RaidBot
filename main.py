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
grp = __import__("group")

config = jsm.JsonManager(pyc.configPath)
commandJsonClass = jsm.JsonManager(pyc.commandsPath)
allGroups = []
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

    print("--------------------------")
    print(f"Author : {ctx.author}")
    print(f"Content: {ctx.content}")

    prefix = config.load()["prefix"]
    syntaxArray = ctx.content.split(" ")
    syntax = " ".join(syntaxArray[1:])
    commandJson = commandJsonClass.load()

    if(not ctx.content.startswith(prefix)):
        return

    if(ctx.content.startswith(prefix + "help")):
        helpEmbed = discord.Embed(title=f"Commands", color=0x00ff00)
        for i in commandJson: 
            helpEmbed.add_field(name=f"{i.capitalize()} command", value=f"{prefix}{i}")
            helpEmbed.add_field(name="Required Role", value=f"{commandJson[i]['requiredRole']}")
            helpEmbed.add_field(name="Roles ", value=f"{', '.join(commandJson[i]['roles'])}", inline=False)
        await ctx.channel.send(embed=helpEmbed)
        return


    for command in commandNames:
        if(ctx.content.startswith(prefix+command)):
            command = commandJson[command]
            userRoles = ctx.author.roles

            if( not (command["requiredRole"] in [i.name.lower() for i in userRoles])):
                await ctx.channel.send("You dont have permission to use this command")
                return

            roleNeedsRemoval = syntax.lower() in [i.name.lower() for i in userRoles]
            print(f"Role needs removal: {roleNeedsRemoval}")

            if(command["allowedOneRole"]):
                for role in command["roles"]:
                    if(role in [i.name.lower() for i in userRoles]):
                        await ctx.author.remove_roles(getRoleByName(ctx, role))
                        print(f"removed role {role}")

            if(not roleNeedsRemoval):
                await ctx.author.add_roles(getRoleByName(ctx, syntax))
                await ctx.channel.send(f"Added role {syntax}")
                print(f"Added role {syntax}")

            else:
                await ctx.author.remove_roles(getRoleByName(ctx, syntax))
                await ctx.channel.send(f"Removed role {syntax}")
                print(f"Removed role {syntax}")
            return

bot.run(config.load()["token"])
