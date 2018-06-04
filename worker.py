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
        userID = message.author.id
        embed = discord.Embed(title="Scratch Verify", color=0xffbc05)
        embed.add_field(name="Authentication Code: ", value=userID, inline=True)
        embed.add_field(name="Instructions:", value="Please post this code on the profile you want to verify on, then enter %verify (profile)", inline=False)
        await client.send_message(message.channel, embed=embed)
    
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
