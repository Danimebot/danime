import discord
from discord.ext import commands
import random
from pysaucenao import DailyLimitReachedException, AnimeSource,UnknownStatusCodeException ,GenericSource, InvalidImageException, InvalidOrWrongApiKeyException, MangaSource, SauceNao, SauceNaoException, ShortLimitReachedException, VideoSource
from pysaucenao.containers import ACCOUNT_ENHANCED, AnimeSource, BooruSource, PixivSource
import re
from urllib import parse
from core import danime
from reactionmenu import ButtonsMenu, ComponentsButton
import requests, bs4
from bs4 import BeautifulSoup as soup
from utils import utils
class sauce(commands.Cog, name="Sauce"):
    def __init__(self, Bot):
        self.Bot = Bot
        self.saucenao_keys = self.Bot.saucenao_keys

    async def get_sauce_embeds(self, ctx, url,results):
        embeds = []
        google_url  = f"https://www.google.com/searchbyimage?image_url={url}&safe=off"
        yandex_url  = f"https://yandex.com/images/search?url={url}&rpt=imageview"
        saucenao_url = f"https://saucenao.com/search.php?url={url}"
        for sauce in results:
            try:
                embed = discord.Embed()
                thumbnail = ctx.author.avatar_url if not sauce.thumbnail else sauce.thumbnail
                similarity = 0 if not sauce.similarity else sauce.similarity
                if similarity > 80:
                    review = "Hey found something highly similar to your query. Result seems to be identical."
                if similarity >60 and similarity < 80:
                    review = "Not so sure if this is the correct result."
                if similarity < 60:
                    review = "Probably not the correct result but still take it."

                if isinstance(sauce.urls, list):
                    embed.add_field(name="Sauce(s)", value="\n".join(sauce.urls), inline=False)
                else:
                    if sauce.urls:
                        embed.add_field(name="Sauce", value=f"{sauce.urls}")
                    else:
                        source = "https://saucenao.com/search.php?url={}".format(parse.quote_plus(url))
                        embed.add_field(name="Sauce", value=f"Sauce not given man :(. Still try by going [Here]({source})", inline=False)
                
                if isinstance(sauce, AnimeSource):
                    await sauce.load_ids()
                    embed.add_field(name="Anime Info", value=f"[AniList]({sauce.anilist_url}) "
                                                            f"[MyAnimeList]({sauce.mal_url})")            
                if isinstance(sauce, VideoSource):
                    embed.add_field(name="Episode ", value=sauce.episode)
                    embed.add_field(name= "TimeStamp", value=sauce.timestamp, inline=False) 
                
                if isinstance(sauce, MangaSource):
                    embed.add_field(name="Chapter", value=sauce.chapter if sauce.chapter else "Not given")


                author = "Author not given" if not sauce.author_name else sauce.author_name
                title = "Title not given" if not sauce.title else sauce.title

                index_id = "Index not given" if (sauce.index_id == None) else sauce.index_id
                index_name = "Inxed name not given" if (sauce.index_name == None) else sauce.index_name       

                embed.description=f"Sucessfully found closest image(`{title}`) with the following information."
                embed.add_field(name="Similarity", value = similarity)
                if isinstance(sauce, PixivSource):
                    embed.add_field(name="Author", value=f"[{author}]({sauce.author_url})")
                embed.add_field(name="Author", value = author )
                embed.add_field(name="Index", value=f"ID : `{index_id}` \nName : `{index_name}`", inline = False)
                if not url.startswith(("https://konachan", "https://yan")):
                    embed.add_field(name="Others", value=f"<:google:864001090172354610> [Google]({google_url}) "
                                                        f"<:yandex:864002609466572840> [Yandex]({yandex_url}) "
                                                        f"[SauceNao]({saucenao_url})" ,inline=False)
                embed.add_field(name="Danime says:", value=review)
                embed.set_thumbnail(url=thumbnail)
                embeds.append(embed)


            except :
                continue
        return embeds

    @commands.command(aliases = ['saucenao'], description = "Let's you search for sauce with saucenao, works with image links. You also have the option to just use dh sauce and the bot will auto search the previous 10 messages and give sauce for the first image it finds. You also have the option to attach an image while using the command. Now works with .mp4 formats too.", usage="dh sauce image.jpg \n dh sauce")
    @commands.guild_only()
    @commands.cooldown(1, 60, commands.BucketType.user)
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
            await ctx.send("Couldn't find the url checking for the last message with image url.", delete_after = 5)
            async for message in ctx.channel.history(limit=10):
                check = self.is_url(message.content)
                if check == True:
                    url = message.content
                    break
        if url == None:
            return await ctx.send("No image urls found in the last 10 messages please retry by uploading one.")
        if url.endswith(('.mp4', '.webm', '.mov')):
            if  url.startswith('https://cdn.discordapp.com') or url.startswith('https://media.discordapp.net'):
                url = url.replace("cdn.discordapp.com", "media.discordapp.net") + "?format=jpeg"
            else:
                return await ctx.send("If you are getting a video sauce, please use a discord url. Just download the video from this link and upload it to discord while using `dh sauce`.")

        saucenao_url = f"https://saucenao.com/search.php?url={url}"
        try:
            sauce = SauceNao(api_key = random.choice(self.saucenao_keys), results_limit = 3, priority=[21, 22, 5, 37, 25])
            results = await sauce.from_url(url)
            embeds = await self.get_sauce_embeds(ctx, url,results)
        except SauceNaoException:
            return await self.generic_error(ctx, saucenao_url)
        except DailyLimitReachedException:
            url = saucenao_url
            embeds = utils.get_sauce(url=url, embed=True)
        if embeds:
            menu = ButtonsMenu(ctx, menu_type=ButtonsMenu.TypeEmbed, timeout=90, show_page_director=True)
            for e in embeds:
                menu.add_page(e)
            buttons = [
                ComponentsButton(style=ComponentsButton.style.primary, label = 'Previous Result', custom_id=ComponentsButton.ID_PREVIOUS_PAGE),
                ComponentsButton(style=ComponentsButton.style.primary, label = 'Stop' , custom_id=ComponentsButton.ID_END_SESSION),
                ComponentsButton(style=ComponentsButton.style.primary, label = 'Next Result', custom_id=ComponentsButton.ID_NEXT_PAGE),
            ]
            for button in buttons:
                menu.add_button(button)
            await menu.start()
            
        if not embeds:
            return await self.generic_error(ctx, saucenao_url)
    @commands.command(aliases=['sauceadv'], usage= "dh sauceadv https://danimebot.xyz/image.png",
        description= "The advanced version of the sauce command meant for experienced users who need more sites than the normal version. Less info.")
    @commands.cooldown(1, 15, commands.BucketType.user)
    async def sauceadvanced(self, ctx, url:str=None):
        if url:
           if self.is_url(url) != True:
                return await ctx.send("Your image url doesn't seem to be accurate. An image url should look like `https://danbooru.donmai.us/data/original/a2/d0/a2d093a060757d36d8a9f03bcbfbcd82.jpg`.")

        if url == None:
            await ctx.send("No url found in command, checking for attachments.", delete_after = 5)
            try:
                url = ctx.message.attachments[0].url
            except: 
                url = None
        
        if url == None:
            await ctx.send("Couldn't find the url checking for the last message with image url.", delete_after = 5)
            async for message in ctx.channel.history(limit=10):
                check = self.is_url(message.content)
                if check == True:
                    url = message.content
                    break
        if url == None:
            return await ctx.send("No image urls found in the last 10 messages please retry by uploading one.")
        if url.endswith(('.mp4', '.webm', '.mov')):
            if  url.startswith(('https:cdn.discordapp.com', 'https://media.discordapp.net')):
                url = url.replace("cdn.discordapp.com", "media.discordapp.net") + "?format=jpeg"
            else:
                return await ctx.send("If you are getting a video sauce, please use a discord url. Just download the video from this link and upload it to discord while using `dh sauceadv`.")     

        r = requests.get(f"https://imgops.com/{url}").text
        soup1 = soup(r, 'lxml')
        
        await self.get_advanced_embed(ctx, url,soup1)


    async def get_advanced_embed(self, ctx, url,soup):
        karmadecay = soup.find("a", {"id" : "t87"})['href']
        iqdb = soup.find("a", {"id" : "t78"})['href']
        saucenao = soup.find("a", {"id" : "t82"})['href']
        ascii2d = "https://imgops.com" + soup.find("a", {"id" : "t84"})['href']
        tracemoe = soup.find("a", {"id" : "t201"})['href']
        google_url  = f"https://www.google.com/searchbyimage?image_url={url}&safe=off"
        embed = discord.Embed()
        embed.set_thumbnail(url = url)
        embed.add_field(name="SauceNao", value=f"[Click Here]({saucenao})", inline=False)
        embed.add_field(name="Ascii2d", value=f"[Click Here]({ascii2d})", inline=False)
        embed.add_field(name="Reddit", value = f"[Click Here]({karmadecay})", inline=False)
        embed.add_field(name="Tracemoe", value=f"[Click Here]({tracemoe})", inline=False)
        embed.add_field(name="IQDB", value=f"[Click Here]({iqdb})", inline=False)
        embed.add_field(name="Google", value=f'[Click Here]({google_url})', inline=False)
        embed.set_footer(icon_url = ctx.author.avatar_url, text = "This data is from imageops.com, please refer there for more cool image operaions.")        
        return await ctx.send(embed=embed)
    def is_url(self, message):
        pattern =  re.compile(r"^https?://\S+(\.jpg|\.png|\.jpeg|\.webp|\.gif|\.mp4|\.mov|\.webm)$")
        if not pattern.match(message):
            return False
        return True

    async def generic_error(self, ctx, url):
        url = "https://saucenao.com/search.php?url={}".format(parse.quote_plus(url))
        em = discord.Embed(description =f"Sorry, nothing found you can try [here]({url}) if you'd like.")
        em.set_footer(text="Also, make sure your url ends with an image format.")
        await ctx.send(embed = em)




def setup (Bot: danime.Danime):
    Bot.add_cog(sauce(Bot))
    Bot.logger.info("Sauce cog is working.")