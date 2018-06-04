#Scratch Search Tools
import requests
import re
#Discord API
import discord
from discord.ext.commands import Bot
from discord.ext import commands
from discord.utils import get
import asyncio

def getCode(user, code):
    page = requests.get("https://scratch.mit.edu/site-api/comments/user/"+user+"/?page=1")
    cleanr = re.compile('<.*?>')
    cleantext = re.sub(cleanr, '', page.text)
    lines = cleantext.split()
    comments = [line for line in cleantext.split('\n') if line.strip() != '']
    for i in range(0, len(comments)):
        comments[i] = " ".join(comments[i].split())
    for i in range(0, len(comments)):
        if comments[i] == user:
            if comments[i+1] == code:
                return True
                break
                
    return False

Client = discord.Client()
client = commands.Bot(command_prefix="%")

@client.event
async def on_ready():
    print("Bot is ready")


@client.event
async def on_message(message):
    if message.content == "%verifyme":
        embed = discord.Embed(title="Tile", description="Desc", color=0x00ff00)
        embed.add_field(name="Field1", value="hi", inline=False)
        embed.add_field(name="Field2", value="hi2", inline=False)
        await client.send_message(message.channel, embed=embed)
        userID = message.author.id
        await client.send_message(message.channel, ("Please post the code {} on the profile you want to verify on, then type %verify (username)").format(userID))

    if message.content.lower().startswith("%verify"):
        userID = message.author.id
        args = " ".join(message.content.split(" ")[1:])
        if args != "":
            if getCode(args, userID):
                role = get(message.server.roles, name='Verified')
                await client.add_roles(message.author, role)
                await client.send_message(message.channel, "Authentication successfully completed")
            else:
                await client.send_message(message.channel, "Authentication failed, please try again")

    if message.content == "%help":
        await client.send_message(message.channel, "```%verifyme: Generates a code to verify\n%verify (username): Authenticates the account ```")
        
client.run("NDUyODUyNjA4NDI4NjcwOTg2.DfWZpg.bxQeETNk-BAHaG3aqJKORhOOONY")
