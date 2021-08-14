from discord.ext import commands, tasks
import discord
import pymongo
from pymongo import MongoClient
import json 
import os


path = "/home/ubuntu/danime/src/configs.json"

if not os.path.exists(path):
    path = "/home/vein/Documents/danime/src/configs.json"

with open(path) as jsonfile:
    obj = json.load(jsonfile)
    db1_token = obj['data']['db1']
    db2_token = obj['data']['db2']


class _checks(commands.Cog):

    def __init__(self, Bot):
        self.Bot = Bot
    

premium_guilds = []

@tasks.loop(seconds=60)
async def append_premium():
    db =  MongoClient(db1_token)['AbodeDB']
    collection = db['premium_guilds']
    get_guilds = {
        "$group" : {
            "_id" : "$_id",
            }
    }
    pipeline = [
        get_guilds
    ]
    results = collection.aggregate(pipeline)
    for answer in results:
        guild = answer['_id']
        if guild not in premium_guilds:
            premium_guilds.append(guild)
    print(premium_guilds)

def get_guilds():
    return premium_guilds

def is_premium_guild():
    async def predictate(ctx):
        if ctx.guild.id in get_guilds():
            return True
        else:
            await ctx.send("This command needs your server to have premium activated. `dh premium` for more info.")
            return False
    return commands.check(predictate)   

append_premium.start()

def setup (Bot):
    Bot.add_cog(_checks(Bot))
    print("Checks cog is working.")

