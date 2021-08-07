import discord
from discord.ext import commands
import pymongo
from pymongo import MongoClient




class _premium(commands.Cog):

    def __init__(self, Bot):
        self.bot = Bot




def setup (Bot):
    Bot.add_cog(_premium(Bot))
    print("Premium cogs is working.")