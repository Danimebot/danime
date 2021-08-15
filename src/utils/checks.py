from discord.ext import commands, tasks
import discord
import pymongo

def is_premium_guild():
    async def predictate(ctx):
        if ctx.guild.id in ctx.bot.premium_guilds:
            return True
        else:
            await ctx.send("This command needs your server to have premium activated. `dh premium` for more info.")
            return False
    return commands.check(predictate)


class _checks(commands.Cog):

    def __init__(self, Bot):
        self.Bot = Bot
        self.append_premium.start()
    

    @tasks.loop(seconds=60)
    async def append_premium(self):
        await self.Bot.wait_until_ready()
        db =  self.Bot.db1['AbodeDB']
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
            if guild not in self.Bot.premium_guilds:
                self.Bot.premium_guilds.append(guild)
        
def setup (Bot):
    Bot.add_cog(_checks(Bot))
    print("Checks cog is working.")