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
        embed.add_field(name="Authentication Code: ", value="`"+userID+"`", inline=False)
        embed.add_field(name="Instructions:", value="`Please post this code on the profile you want to verify on, then enter %verify (profile).`", inline=False)
        await client.send_message(message.channel, embed=embed)
    
    if message.content.lower().startswith("%verify"):
        userID = message.author.id
        args = " ".join(message.content.split(" ")[1:])
        if args != "":
            if getCode(args, userID):
                extra = ""
                try:
                    role = get(message.server.roles, name='Verified')
                    await client.add_roles(message.author, role)
                except:
                    extra = " Verified role missing or insufficient permissions."
                embed = discord.Embed(title="Scratch Verify", color=0xffbc05)
                embed.add_field(name="Status: ", value="`Authentication successfully completed."+extra+"`", inline=False)
                await client.send_message(message.channel, embed=embed)
            else:
                embed = discord.Embed(title="Scratch Verify", color=0xffbc05)
                embed.add_field(name="Status: ", value="`Authentication failed, please retry.`", inline=False)
                await client.send_message(message.channel, embed=embed)

    if message.content == "%help":
        embed = discord.Embed(title="Scratch Verify", description="`Always use the % prefix`", color=0xffbc05)
        embed.add_field(name="verifyme", value="`Generate a verification code to use.`", inline=False)
        embed.add_field(name="verify [username]", value="`Use this command to authenticate your account and receive the 'Verified' role.`", inline=False)
        await client.send_message(message.channel, embed=embed)
        
client.run("NDUyODUyNjA4NDI4NjcwOTg2.DfWZpg.bxQeETNk-BAHaG3aqJKORhOOONY")
