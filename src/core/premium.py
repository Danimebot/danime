import discord
from discord.ext import commands
import pymongo
from pymongo import MongoClient
import datetime
from utils.utils import Convert, DanimeCommands


premium_mods = [427436602403323905, 755436063828213821, 814953152640974869, 360087319992074251]


class _premium(commands.Cog):

    def __init__(self, Bot):
        self.Bot = Bot

    def mod_check(ctx):
        if ctx.author.id in premium_mods:
            return True
        return False 
    @commands.command()
    async def premium(self, ctx):
        db = self.Bot.db1['AbodeDB']
        collection = db['premium_guilds']
        return await ctx.send("Coming soon...")

    @commands.command()
    @commands.check(mod_check)
    async def add_premium(self, ctx, guild_id:int, ends_at):
        db = self.Bot.db1['AbodeDB']
        collection = db['premium_guilds']
        query = {"_id" : guild_id}
        search = collection.find_one(query)
        now_time = datetime.datetime.now()
        time = await Convert().convert(ctx, ends_at)
        ends_at = now_time + datetime.timedelta(seconds =  int(time))
        if not search:
            data = {"_id" : guild_id, "added_by" : ctx.author.id, "added_by_name" : ctx.author.name,
            "added_time" : now_time, "ends_at" : ends_at, "ends_at_seconds" : time}
            collection.insert_one(data)
            channel = self.Bot.get_channel(875053414546022490)
            em = discord.Embed(timestamp = ends_at)
            em.description = "Premium guild added!"
            em.add_field(name="Guild", value=guild_id)
            em.add_field(name="Added by", value=f"{ctx.author.id} | {ctx.author.mention}")
            em.add_field(name="Ends at ")
            await channel.send(embed=em)
        if search:
            return await ctx.send("Premium already activated.")
    


def setup (Bot):
    Bot.add_cog(_premium(Bot))
    print("Premium cogs is working.")