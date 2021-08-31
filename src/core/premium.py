import discord
from discord.ext import commands, tasks
import pymongo
from pymongo import MongoClient
import datetime
from utils.utils import Convert, DanimeCommands
import string 
import random

premium_mods = [427436602403323905, 755436063828213821, 814953152640974869, 360087319992074251]

letters = string.ascii_lowercase 
class _premium(commands.Cog):

    def __init__(self, Bot):
        self.Bot = Bot
        self.update_codes.start()

    def mod_check(ctx):
        if ctx.author.id in premium_mods:
            return True
        return False 
    @commands.command()
    async def premium(self, ctx):
        db = self.Bot.db1['AbodeDB']
        collection = db['premium_guilds']
        em = discord.Embed(color = random.choice(self.Bot.color_list))
        search = collection.find_one({"_id" : ctx.guild.id})
        message = "Your guild isn't a premium server"
        if search:
            message = "Your guild is a premium server"
            em.add_field(name="Activated by ", value= f"{search['added_by']} | {search['added_by_name']}")
            em.timestamp = search['ends_at']
            em.set_footer(text="Your premium ends at ")
        em.description = f"{message}, You can learn more about premium **[Here](https://www.danimebot.xyz/premium)**"
        await ctx.send(embed=em)

            

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
            "added_time" : now_time, "ends_at" : ends_at, "ends_at_seconds" : time, "added_type" : "power_abooz"}
            collection.insert_one(data)
            channel = self.Bot.get_channel(875053414546022490)
            em = discord.Embed(timestamp = ends_at)
            em.description = "Premium guild added!"
            em.add_field(name="Guild", value=guild_id)
            em.add_field(name="Added by", value=f"{ctx.author.id} | {ctx.author.mention}")
            em.set_footer(name="Ends at ")
            await channel.send(embed=em)
            await ctx.send("Premium activated! `dh premium` for more information.")
        if search:
            return await ctx.send("Premium already activated.")
    
    @commands.command()
    async def enable_premium(self, ctx, code:str):
        guild_id = ctx.guild.id
        db = self.Bot.db1['AbodeDB']
        collection = db['premium_guilds']
        query = {"_id" : guild_id}
        search = collection.find_one(query)
        now_time = datetime.datetime.now()
        ends_at = "30d"
        time = await Convert().convert(ctx, ends_at)
        ends_at = now_time + datetime.timedelta(seconds =  int(time))
        search2 = db['premium_codes'].find_one({"_id" : code})
        if not search :
            if search2:
                data = {"_id" : guild_id, "added_by" : ctx.author.id, "added_by_name" : ctx.author.name,
                "added_time" : now_time, "ends_at" : ends_at, "ends_at_seconds" : time, "added_type" : "chad_premoim"}
                collection.insert_one(data)
                channel = self.Bot.get_channel(875053414546022490)
                em = discord.Embed(timestamp = ends_at)
                em.description = "Premium guild added!"
                em.add_field(name="Guild", value=guild_id)
                em.add_field(name="Added by", value=f"{ctx.author.id} | {ctx.author.mention}")
                em.add_field(name="Ends at ")
                await channel.send(embed=em)
            else:
                return await ctx.send("Wrong code dude lol!")
        if search:
            return await ctx.send("Premium already activated.")


    @commands.command()
    @commands.check(mod_check)
    async def create_premium_code(self, ctx, ends_at:str=None):
        db = self.Bot.db1['AbodeDB']
        collection = db['premium_codes']
        if not ends_at:
            ends_at = "3d"
        now_time = datetime.datetime.now()
        time = await Convert().convert(ctx, ends_at)
        ends_at = now_time + datetime.timedelta(seconds=  int(time))
        code = (''.join(random.choice(letters) for i in range(16)))
        collection.insert_one({"_id" : code, "end_time" : ends_at, "created_by" : f"{ctx.author.id} | {ctx.author.name}"})
        channel = self.Bot.get_channel(875053414546022490)
        em = discord.Embed()
        em.description = "Premium Code created, lasts for 3 days."
        em.add_field(name="Created by : ", value=f"{ctx.author.id} | {ctx.author.mention}")
        em.add_field(name="Code", value = code)
        await channel.send(embed=em)
        await ctx.send(f"Code is {code}", delete_after=20)


    @tasks.loop(seconds=360)
    async def update_codes(self):
        if self.Bot.DEFAULT_PREFIX == "&":
            return
        now = datetime.datetime.now()
        db = self.Bot.db1['AbodeDB']
        collection = db['premium_codes']
        search = collection.find()
        for result in search:
            if now >= result['end_time']:
                collection.delete_one({"_id" : result['_id']})
                channel = self.Bot.get_channel(875053414546022490)
                em = discord.Embed()
                em.description = "Premium code Expired, wasn't used in 3 days."
                em.add_field(name="Code", value = result['_id'])
                await channel.send(embed=em)
                collection.delete_one({"_id" : result['_id']})




def setup (Bot):
    Bot.add_cog(_premium(Bot))
    print("Premium cogs is working.")