import discord
from discord.ext import commands
import random
from saucenao_api import SauceNao, VideoSauce
from disputils import BotEmbedPaginator
import re
from urllib import parse

class sauce(commands.Cog, name="Sauce"):
    def __init__(self, Bot):
        self.Bot = Bot

    @commands.command(aliases = ['saucenao'], description = "Let's you search for sauce with saucenao, works with image links. You also have the option to just use dh sauce and the bot will auto search the previous 10 messages and give sauce for the first image it finds. You also have the option to attach an image while using the command.", usage="dh sauce image.jpg \n dh sauce")
    @commands.guild_only()
    @commands.cooldown(1, 15, commands.BucketType.user)
    async def sauce(self, ctx, url=None):
        if url!= None:
            if not url.startswith("https"):
                return await ctx.send("Not a valid url, a url must begin with https.")
        if url == None:
            await ctx.send("No url found in command, checking for attachments.", delete_after = 5)
            try:
                url = ctx.message.attachments[0].url
                print(url)
            except:
                url = None
        
        if url == None:
            await ctx.send("Couldn't find the url checking for the last message with image.", delete_after = 5)
            async for message in ctx.channel.history(limit=10):
                check = self.is_url(message)
                if check == True:
                    url = message.content
                    break
        if url == None:
            return await ctx.send("No image urls found in the last 10 messages please retry by uploading one.")
        try:
            sauce = SauceNao(api_key = "2e2bd7105762f95bf1fdd688b2bbe34e28088873")
            results = sauce.from_url(url)
            thumbnail = results[0].thumbnail if (results[0].thumbnail != None) else "None"
            similarity = results[0].similarity if (results[0].similarity != None) else "None"
            try:
                source = results[0].urls[0]
            except:
                source = "https://saucenao.com/search.php?url={}".format(parse.quote_plus(url))
            try:
                author = results[0].author
            except:
                author = "Not given"
            try:
                title = results[0].title
            except:
                title = "No title"
            index_id = results[0].index_id if (results[0].index_id != None) else "None"
            index_name = results[0].index_name if (results[0].index_name != None) else "None"
            if 70 >  similarity:
                return await ctx.send("Couldn't find any thing for the given query.")

            embed = discord.Embed()
            embed.description=f"Sucessfully found closest image(`{title}`) with the following information."
            embed.add_field(name="Similarity", value = similarity)
            embed.add_field(name="Author", value =author )
            embed.add_field(name="Source", value=source, inline=False)
            embed.add_field(name="Index", value=f"ID : `{index_id}` \nName : `{index_name}`")
            embed.set_thumbnail(url = thumbnail)
            embed.set_footer(text=f"Enjoy!")
            await ctx.send(embed=embed)
        except:
            url = "https://saucenao.com/search.php?url={}".format(parse.quote_plus(url))
            em = discord.Embed(description =f"Sorry nothing found you can try [here]({url}) if you'd like.")
            em.set_footer(text="Also, make sure your url ends with an image format.")
            await ctx.send(embed = em)

    def is_url(self, message):
        pattern = re.compile("(?:([^:/?#]+):)?(?://([^/?#]*))?([^?#]*\.(?:jpg|gif|png))(?:\?([^#]*))?(?:#(.*))?")
        matches = pattern.finditer(message.content)
        for match in matches:
            if match.string.startswith("http"):
                return True
            return False







def setup (Bot):
    Bot.add_cog(sauce(Bot))
    print("Sauce cog is working.")