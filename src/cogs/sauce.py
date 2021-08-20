import discord
from discord.ext import commands
import random
from pysaucenao import DailyLimitReachedException, AnimeSource,UnknownStatusCodeException ,GenericSource, InvalidImageException, InvalidOrWrongApiKeyException, MangaSource, SauceNao, SauceNaoException, ShortLimitReachedException, VideoSource
from pysaucenao.containers import ACCOUNT_ENHANCED, AnimeSource, BooruSource
from disputils import BotEmbedPaginator
import re
from urllib import parse
from core import danime

class sauce(commands.Cog, name="Sauce"):
    def __init__(self, Bot):
        self.Bot = Bot
        self.saucenao_keys = self.Bot.saucenao_keys

    @commands.command(aliases = ['saucenao'], description = "Let's you search for sauce with saucenao, works with image links. You also have the option to just use dh sauce and the bot will auto search the previous 10 messages and give sauce for the first image it finds. You also have the option to attach an image while using the command. Now works with .mp4 formats too.", usage="dh sauce image.jpg \n dh sauce")
    @commands.guild_only()
    @commands.cooldown(1, 15, commands.BucketType.user)
    async def sauce(self, ctx, url=None):
        #https://github.com/FujiMakoto/pysaucenao Pray to the lord and savior
        if url!= None:
            if self.is_url(url) != True:
                return await ctx.send("Your image url doesn't seem to be accurate. An image url should look like `https://danbooru.donmai.us/data/original/a2/d0/a2d093a060757d36d8a9f03bcbfbcd82.jpg`.")

        if url == None:
            await ctx.send("No url found in command, checking for attachments.", delete_after = 5)
            try:
                url = ctx.message.attachments[0].url
            except: 
                url = None
        
        if url == None:
            await ctx.send("Couldn't find the url checking for the last message with image.", delete_after = 5)
            async for message in ctx.channel.history(limit=10):
                check = self.is_url(message.content)
                if check == True:
                    url = message.content
                    break
        if url == None:
            return await ctx.send("No image urls found in the last 10 messages please retry by uploading one.")
        if url.endswith(('.mp4', '.webm', '.mov')):
            url = url.replace("cdn.discordapp.com", "media.discordapp.net") + "?format=jpeg"
        try:
            google_url  = f"https://www.google.com/searchbyimage?image_url={url}&safe=off"
            yandex_url  = f"https://yandex.com/images/search?url={url}&rpt=imageview"
            saucenao_url = "https://saucenao.com/search.php?url={}".format(parse.quote_plus(url))
            sauce = SauceNao(api_key = random.choice(self.saucenao_keys), results_limit = 6)
            embed = discord.Embed()
            results = await sauce.from_url(url)
            thumbnail = results[0].thumbnail

            similarity = results[0].similarity if (results[0].similarity != None) else 0
            embed.set_thumbnail(url = thumbnail)

            if isinstance(results[0], AnimeSource):
                await results[0].load_ids()
                embed.add_field(name="Anime Info", value=f"[AniList]({results[0].anilist_url}) "
                                                        f"[MyAnimeList]({results[0].mal_url})")
            if isinstance(results[0], VideoSource):
                embed.add_field(name="Episode ", value=results[0].episode)
                embed.add_field(name= "TimeStamp", value=results[0].timestamp, inline=False)           

            if isinstance(results[0], MangaSource):
                embed.add_field(name="Chapter", value=results[0].chapter)
        
            try:
                source = results[0].urls[0]
            except IndexError:
                source = "https://saucenao.com/search.php?url={}".format(parse.quote_plus(url))
            except TypeError:
                return await ctx.send("Nothing found in you request. Try not using a gif url if possible.")
            try:
                author = results[0].author_name
            except AttributeError:
                author = "Not given"
            try:
                title = results[0].title
            except AttributeError:
                title = "No title"
            index_id = results[0].index_id if (results[0].index_id != None) else "None"
            index_name = results[0].index_name if (results[0].index_name != None) else "None"
            if 50 >  similarity:
                return await ctx.send("Couldn't find any thing for the given query.")

            
            embed.description=f"Sucessfully found closest image(`{title}`) with the following information."
            embed.add_field(name="Similarity", value = similarity)
            embed.add_field(name="Author", value =author )
            embed.add_field(name="Source", value=source, inline=False)
            embed.add_field(name="Index", value=f"ID : `{index_id}` \nName : `{index_name}`")
            embed.add_field(name="Others", value=f"<:google:864001090172354610> [Google]({google_url}) "
                                                f"<:yandex:864002609466572840> [Yandex]({yandex_url}) "
                                                f"[SauceNao]({saucenao_url})"
                                                ,inline=False)
            
            embed.set_footer(text=f"The sauce is found from sauce-nao.net.")
            await ctx.send(embed=embed)

        
        except SauceNaoException:
            url = "https://saucenao.com/search.php?url={}".format(parse.quote_plus(url))
            em = discord.Embed(description =f"Sorry nothing found you can try [here]({url}) if you'd like.")
            em.set_footer(text="Also, make sure your url ends with an image format.")
            await ctx.send(embed = em)

        except InvalidImageException:
            return await ctx.send("Hey, it seems the url has no results. Also it seems your url is not an image url, please retry after checking that.")
    
        except IndexError:
            return await ctx.send("Something went worng, it seems no results from your queries.")
    
    def is_url(self, message):
        pattern =  re.compile(r"^https?://\S+(\.jpg|\.png|\.jpeg|\.webp]|\.gif|\.mp4|\.mov|\.webm)$")
        if not pattern.match(message):
            return False
        return True






def setup (Bot: danime.Danime):
    Bot.add_cog(sauce(Bot))
    Bot.logger.info("Sauce cog is working.")