import discord
from discord.ext import commands, tasks
import datetime
import random
from random import randint
import asyncio
import traceback
import aiohttp
from aiohttp import ClientSession
import requests
import urllib
from discord.ext.commands import command, cooldown
import json
import nekos
from TextToOwO.owo import text_to_owo as owoConvert
import hmtai
from cogs.autonsfw import DanimeAPI
from pygicord import Paginator

#This cog also contains many sfw things :


class vein3(commands.Cog, name="APIs"):
    def __init__(self, Bot):
        self.Bot = Bot
        self.danime_api = DanimeAPI(self.Bot.api_url)

    async def notnsfw(self, ctx):
        embed = discord.Embed(color=random.choice(self.Bot.color_list))
        embed.title = f"Non-NSFW channel detected!"
        embed.add_field(name="Why should you care?", value=f"Discord forbids the use of NSFW content outside the NSFW-option enabled channels. [More here](https://discord.com/guidelines#:~:text=You%20must%20apply%20the%20NSFW,sexualize%20minors%20in%20any%20way.)", inline=False)
        embed.add_field(name="How can I enable the NSFW channel option?", value=f"** **", inline=False)
        embed.set_image(url=f"https://cdn.discordapp.com/attachments/802518639274229800/802936914054610954/nsfw.gif")
        embed.set_footer(text=f"Pro tip: {self.Bot.DEFAULT_PREFIX}set_nsfw can do the work for you.")
        return await ctx.send(embed=embed)

    @commands.command(description='Get quick info about an API')
    @commands.guild_only()
    async def api(self, ctx, *, url=None):
        if url == None:
            return await ctx.send("Please pass in an URL")
        else:
            req = requests.get(f"{url}").json()
            req_1 = json.dumps(req, indent=4)
            embed = discord.Embed(color=self.Bot.color,
                                  timestamp=datetime.datetime.utcnow())
            embed.set_author(name="API response to ", url=f"{url}", icon_url=ctx.me.avatar_url)
            embed.description = f"```json\n{req_1}```"

            await ctx.send(embed=embed)

    @commands.command(description=f"Gets a random waifu.\nThe categories are SFW and NSFW while the types can be seen through <https://waifu.pics/docs>.")
    @commands.guild_only()
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def waifu(self, ctx, category=None, type_=None):

        if category == None and type_ == None:
            url = f"https://api.waifu.pics/sfw/waifu"
            data = requests.get(f"{url}").json()
            link = data['url']
            await self.waifu_embed(ctx=ctx, link=link)
        if category == "sfw" and type_ != None:
            type_ = type_.lower()
            category = category.lower()
            url = f"https://api.waifu.pics/{category}/{type_}"
            data = requests.get(f"{url}").json()
            link = data['url']
            await self.waifu_embed(ctx=ctx, link=link)
        if category == "nsfw" and type_ != None:
            type_ = type_.lower()
            category = category.lower()
            if not ctx.channel.is_nsfw():
                await self.notnsfw(ctx=ctx)
                return

            url = f"https://api.waifu.pics/{category}/{type_}"
            data = requests.get(f"{url}").json()
            link = data['url']
            await self.waifu_embed(ctx=ctx, link=link)

    @commands.command(description=f"Sends blowjob images ig", aliases=['bj'])
    @commands.guild_only()
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def blowjob(self, ctx, amount: int = 0):
        if not ctx.channel.is_nsfw():
            await self.notnsfw(ctx=ctx)
            return
        if amount != 0:
            return await self.send_image(ctx, "blowjob", amount)
        if guess == 0:
            r = requests.get(f"{self.Bot.api_url}blowjob").json()['url']
            em = discord.Embed()
            em.description = f"Bad image? [Report it]({self.Bot.support})"
            em.set_image(url=r)
            await ctx.send(embed=em)

    @commands.command(description=f"Sends cute anime fox girls your way")
    @commands.guild_only()
    @commands.cooldown(1, 15, commands.BucketType.user
                       )
    async def foxgirl(self, ctx):
        url = nekos.img(target="fox_girl")
        await self.waifu_embed(ctx=ctx, link=url)

    @commands.command(description='Sends a random doggo picture.')
    @commands.guild_only()
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def dog(self, ctx):
        try:
            async with ctx.channel.typing():
                async with aiohttp.ClientSession() as cs:
                    async with cs.get("https://dog.ceo/api/breeds/image/random") as r:
                        data = await r.json()
                        await cs.close()
                        embed = discord.Embed(title="Woof", colour=0x529dff)
                        embed.set_image(url=data['message'])
                        embed.set_footer(text=f"Requested by {ctx.author}, Source: Thedogapi", icon_url=ctx.author.avatar_url)

                        await ctx.send(embed=embed)
        except:
            await ctx.send(f'Command on cooldown for some seconds.', delete_after=5)

    @commands.command(description='Echos\' words from clyde')
    @commands.guild_only()
    @commands.has_permissions(manage_messages=True)
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def clyde(self, ctx, *, text):
        async with aiohttp.ClientSession() as cs:
            async with cs.get(f"https://nekobot.xyz/api/imagegen?type=clyde&text={text}") as r:
                res = await r.json()
                await cs.close()
                embed = discord.Embed(
                    color=0x529dff

                )
                embed.set_image(url=res['message'])
                embed.set_footer(text=f'Requested by {ctx.author.name}, Source : Nekobot.xyz', icon_url=ctx.author.avatar_url)

                await ctx.send(embed=embed)
                await ctx.message.delete()

    @commands.command(description='Sends a random year fact.')
    @commands.guild_only()
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def yearfact(self, ctx):

        async with aiohttp.ClientSession() as cs:

            async with cs.get(f"http://numbersapi.com/random/year?json") as r:
                data = await r.json()
                await cs.close()

                embed = discord.Embed(
                    title=data['number'], description=data['text'], colour=0x529dff)

                embed.set_footer(text=f"Requested by {ctx.author}, Fact from numbersapi.com", icon_url=ctx.author.avatar_url)
                await ctx.send(embed=embed)

    @commands.command(description='Sends a random panda fact :heart:')
    @commands.guild_only()
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def pandafact(self, ctx):
        async with ctx.channel.typing():
            async with aiohttp.ClientSession() as cs:
                async with cs.get("https://some-random-api.ml/facts/panda") as r:
                    data = await r.json()
                    await cs.close()

                    embed = discord.Embed(title="Panda fact", colour=0x529dff)
                    embed.set_author(name=data['fact'])
                    embed.set_footer(text=f"Requested by {ctx.author}, Source: Some-random-api", icon_url=ctx.author.avatar_url)

                    await ctx.send(embed=embed)

    @commands.command(description='Sends a random cat fact.')
    @commands.guild_only()
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def catfact(self, ctx):
        async with ctx.channel.typing():
            async with aiohttp.ClientSession() as cs:
                async with cs.get("https://some-random-api.ml/facts/cat") as r:
                    data = await r.json()
                    await cs.close()

                    embed = discord.Embed(title="Cat fact :D", colour=0x529dff)
                    embed.set_author(name=data['fact'])
                    embed.set_footer(text=f"Requested by {ctx.author}, Source : Some-random-api", icon_url=ctx.author.avatar_url)
                    await ctx.send(embed=embed)

    @commands.command(description='Sends a random doggo fact.')
    @commands.guild_only()
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def dogfact(self, ctx):
        async with ctx.channel.typing():
            async with aiohttp.ClientSession() as cs:
                async with cs.get("https://some-random-api.ml/facts/dog") as r:
                    data = await r.json()
                    await cs.close()
                    embed = discord.Embed(title="Dog fact :D", colour=0x529dff)
                    embed.set_author(name=data['fact'])
                    embed.set_footer(text=f"Requested by {ctx.author}, Source : Some-random-api", icon_url=ctx.author.avatar_url)

                    await ctx.send(embed=embed)

    @commands.command(description='Sends a random panda picture :heart:')
    @commands.guild_only()
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def panda(self, ctx):

        async with aiohttp.ClientSession() as cs:
            async with cs.get("https://some-random-api.ml/img/panda") as r:
                data = await r.json()
                await cs.close()
                embed = discord.Embed(title="Pandasound :P", colour=0x529dff)
                embed.set_image(url=data['link'])
                embed.set_footer(text=f"Requested by {ctx.author}, Source : Some-random-api", icon_url=ctx.author.avatar_url)

                await ctx.send(embed=embed)

    @commands.command(description='Nevermind the koala is sleeping.')
    @commands.guild_only()
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def koala(self, ctx):

        async with aiohttp.ClientSession() as cs:
            async with cs.get("https://some-random-api.ml/img/koala") as r:
                data = await r.json()
                await cs.close()
                embed = discord.Embed(title="Koala sound :P", colour=0x529dff)
                embed.set_image(url=data['link'])
                embed.set_footer(text=f"Requested by {ctx.author}, Source : Some-random-api", icon_url=ctx.author.avatar_url)

                await ctx.send(embed=embed)

    @commands.command(description='*Pikachu open mouth*')
    @commands.guild_only()
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def pikachu(self, ctx):

        async with aiohttp.ClientSession() as cs:
            async with cs.get("https://some-random-api.ml/img/pikachu") as r:
                data = await r.json()
                await cs.close()
                embed = discord.Embed(title="Pika pika", colour=0x529dff)
                embed.set_image(url=data['link'])
                embed.set_footer(text=f"Requested by {ctx.author}, source some random api", icon_url=ctx.author.avatar_url)
                await ctx.send(embed=embed)

    @commands.command(description='Sends a random numberfact.')
    @commands.guild_only()
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def numberfact(self, ctx):
        async with aiohttp.ClientSession() as cs:
            async with cs.get(f"http://numbersapi.com/random?json") as r:
                data = await r.json()
                await cs.close()
                embed = discord.Embed(
                    title=data['number'], description=data['text'], colour=0x529dff)
                embed.set_footer(text=f"Requested by {ctx.author}, Fact from numbersapi.com", icon_url=ctx.author.avatar_url)
                await ctx.send(embed=embed)

    @commands.command(description='Advices for you.')
    @commands.guild_only()
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def advice(self, ctx):
        r = requests.get("https://api.adviceslip.com/advice").json()
        advice = r["slip"]["advice"]
        embed = discord.Embed(title=advice, colour=0x529dff)
        embed.set_footer(text=f"Requested by {ctx.author}, adviceslip.com", icon_url=ctx.author.avatar_url)
        await ctx.send(embed=embed)

    @commands.command(description='Anime quotes :)')
    @commands.guild_only()
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def aquote(self, ctx):
        async with aiohttp.ClientSession() as cs:
            async with cs.get(f'https://some-random-api.ml/animu/quote') as r:

                data = await r.json()
                await cs.close()
                by = data['characther']
                anime = data['anime']
                quote = data['sentence']

                embed = discord.Embed(title=f'"{quote}"', colour=0x529dff)
                embed.set_author(name=f'By {by} from {anime}')
                embed.set_footer(text=f'Requested by {ctx.author}, Quote from some-random-api')
                await ctx.send(embed=embed)

    @commands.command(description='Give a headpat to someone.', aliases=['pat'])
    @commands.guild_only()
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def headpat(self, ctx, user: discord.Member = None):
        r = requests.get("https://some-random-api.ml/animu/pat").json()['link']
        em = discord.Embed(color=0x26fcff)
        if user != None:
            em.description = f"**{ctx.author.name} pats {user.name}, Kawaiii**"
        em.set_image(url=r)
        await ctx.send(embed=em)

    @commands.command(description=';)')
    @commands.guild_only()
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def wink(self, ctx, user: discord.Member = None):
        r = requests.get(
            "https://some-random-api.ml/animu/wink").json()['link']
        em = discord.Embed(color=0x529dff)
        if user != None:
            em.description = f"{ctx.author.name} winked at {user.name}, Kawaiii"
        em.set_image(url=r)
        await ctx.send(embed=em)

    @commands.command(description='Huggggggggggg.....')
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def hug(self, ctx, user: discord.Member = None):
        r = requests.get("https://some-random-api.ml/animu/hug").json()['link']
        em = discord.Embed(color=0x26fcff)
        if user != None:
            em.description = f"{ctx.author.name} hugs {user.name}, Kawaiii!!"
        em.set_image(url=r)
        await ctx.send(embed=em)

        
    @commands.guild_only()
    @commands.command(description="Do lewd things....", usage = "dh sex @user", aliases=['handhold'])
    async def sex (self, ctx, user:discord.Member= None):
        url = requests.get(f"{self.Bot.api_url}handhold").json()['url']
        em = discord.Embed(color = 0x529dff)
        if user != None:
            em.description = f" {ctx.author.name} and {user.name} do lewd things >m<"
        em.set_image(url = url)
        await ctx.send(embed = em)

    @commands.command(description='Palm to the face')
    @commands.guild_only()
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def facepalm(self, ctx):
        r = requests.get(
            "https://some-random-api.ml/animu/face-palm").json()['link']
        em = discord.Embed(color=0x26fcff)
        em.description = "Palm to the face"
        em.set_image(url=r)
        await ctx.send(embed=em)

    @commands.command(description=f"All bullies shall be punished!")
    @commands.guild_only()
    @commands.cooldown(1, 10, commands.BucketType.user)
    async def bully(self, ctx, user: discord.Member = None):
        url = f"https://api.waifu.pics/sfw/bully"
        data = requests.get(f"{url}").json()
        link = data['url']
        if user == None:
            await self.waifu_embed(ctx=ctx, link=link)

        elif user != None:
            embed = discord.Embed(color=random.choice(self.Bot.color_list))

            embed.set_image(url=f"{link}")
            embed.description = f"{user.mention} You bully! Stop hurting {ctx.author.mention}"
            await ctx.send(embed=embed)

    @commands.command()
    @commands.guild_only()
    @commands.cooldown(1, 50, commands.BucketType.user)
    async def cuddle(self, ctx, user: discord.Member = None):
        url = f"https://api.waifu.pics/sfw/cuddle"
        data = requests.get(f"{url}").json()
        link = data['url']
        if user == None:
            await self.waifu_embed(ctx=ctx, link=link)

        elif user != None:
            embed = discord.Embed(color=random.choice(self.Bot.color_list))

            embed.set_image(url=f"{link}")
            embed.description = f"{ctx.author.mention} cuddles {user.mention}!"
            await ctx.send(embed=embed)

    @commands.command()
    @commands.guild_only()
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def kiss(self, ctx, user: discord.Member = None):
        url = f"https://api.waifu.pics/sfw/kiss"
        data = requests.get(f"{url}").json()
        link = data['url']
        if user == None:
            await self.waifu_embed(ctx=ctx, link=link)

        elif user != None:
            embed = discord.Embed(color=random.choice(self.Bot.color_list))

            embed.set_image(url=f"{link}")
            embed.description = f"{ctx.author.mention} kissed {user.mention}!!!!"
            await ctx.send(embed=embed)

    @commands.command()
    @commands.guild_only()
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def smug(self, ctx, user: discord.Member = None):
        url = f"https://api.waifu.pics/sfw/smug"
        data = requests.get(f"{url}").json()
        link = data['url']
        if user != None:
            await self.waifu_embed(ctx=ctx, link=link)

        elif user == None:
            embed = discord.Embed(color=random.choice(self.Bot.color_list))

            embed.set_image(url=f"{link}")
            embed.description = f"Smug moment heh"
            await ctx.send(embed=embed)

    @commands.command()
    @commands.guild_only()
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def bonk(self, ctx, user: discord.Member = None):
        url = f"https://api.waifu.pics/sfw/bonk"
        data = requests.get(f"{url}").json()
        link = data['url']
        if user == None:
            await self.waifu_embed(ctx=ctx, link=link)

        elif user != None:
            embed = discord.Embed(color=random.choice(self.Bot.color_list))

            embed.set_image(url=f"{link}")
            embed.description = f"{ctx.author.mention} bonked {user.mention}!!!!"
            await ctx.send(embed=embed)

    @commands.command()
    @commands.guild_only()
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def kill(self, ctx, user: discord.Member = None):
        url = f"https://api.waifu.pics/sfw/kill"
        data = requests.get(f"{url}").json()
        link = data['url']
        if user == None:
            await self.waifu_embed(ctx=ctx, link=link)

        elif user != None:

            embed = discord.Embed(color=random.choice(self.Bot.color_list))

            embed.set_image(url=f"{link}")
            embed.description = f"{ctx.author.mention} killed {user.mention}!!!!"
            await ctx.send(embed=embed)

    @commands.command()
    @commands.guild_only()
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def slap(self, ctx, user: discord.Member = None):
        url = f"https://api.waifu.pics/sfw/slap"
        data = requests.get(f"{url}").json()
        link = data['url']
        if user == None:
            await self.waifu_embed(ctx=ctx, link=link)

        elif user != None:

            embed = discord.Embed(color=random.choice(self.Bot.color_list))

            embed.set_image(url=f"{link}")
            embed.description = f"{ctx.author.mention} slaped {user.mention}"
            await ctx.send(embed=embed)

    @commands.command()
    @commands.guild_only()
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def cringe(self, ctx, user: discord.Member = None):
        url = f"https://api.waifu.pics/sfw/slap"
        data = requests.get(f"{url}").json()
        link = data['url']
        if user == None:
            await self.waifu_embed(ctx=ctx, link=link)

        elif user != None:

            embed = discord.Embed(color=random.choice(self.Bot.color_list))

            embed.set_image(url=f"{link}")
            embed.description = f"{user.mention} Bruh that was cringe asf"
            await ctx.send(embed=embed)

    @commands.command()
    @commands.guild_only()
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def blush(self, ctx, user: discord.Member = None):
        url = f"https://api.waifu.pics/sfw/blush"
        data = requests.get(f"{url}").json()
        link = data['url']
        if user == None:
            await self.waifu_embed(ctx=ctx, link=link)

        elif user != None:

            embed = discord.Embed(color=random.choice(self.Bot.color_list))

            embed.set_image(url=f"{link}")
            embed.description = f"OWO blushy blushy {user.mention}"
            await ctx.send(embed=embed)

    @commands.command()
    @commands.guild_only()
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def highfive(self, ctx, user: discord.Member = None):
        url = f"https://api.waifu.pics/sfw/highfive"
        data = requests.get(f"{url}").json()
        link = data['url']
        if user == None:
            await self.waifu_embed(ctx=ctx, link=link)

    @commands.command(aliases=['define'])
    @commands.guild_only()
    async def urban(self, ctx, *, terms):
        if not ctx.channel.is_nsfw():
            await self.notnsfw(ctx=ctx)
            return
        embeds = []
        try:
            async with aiohttp.ClientSession() as cs:
                async with cs.get(f"http://api.urbandictionary.com/v0/define", params={'term': terms}) as r:
                    data = await r.json()
                items = data['list']
                for item in items:
                    embed = discord.Embed(color=0x26fcff)
                    embed.title = item['word']
                    embed.set_author(name=item['author'],
                                     icon_url="https://images-ext-1.discordapp.net/external/Gp2DBilGEcbI2YR0qkOGVkivomBLwmkW_7v3K8cD1mg/https/cdn.discordapp.com/emojis/734991429843157042.png")
                    embed.description = hyper_replace(
                        str(item['definition']), old=['[', ']'], new=['', ''])
                    embed.add_field(name="Example",
                                    value=hyper_replace(str(item['example']), old=['[', ']'], new=['', '']))
                    embed.add_field(name="Votes", value=f"\n👍 **{item['thumbs_up']:,}** 👎 **{item['thumbs_down']}**", inline=False)
                    embeds.append(embed)
                paginator = Paginator(pages=embeds, timeout=90.0)
                await paginator.start(ctx)
        except IndexError:
            raise commands.BadArgument(f"Your search terms gave no results.")

    # @commands.command(description=f"Tch weakness")
    # @commands.guild_only()
    # async def lewd(self, ctx, user: discord.Member = None):
    #     embed = discord.Embed(color= random.choice(self.Bot.color_list))
    #     if user != None:
    #       embed.description=f"{user.name} Yu-ouu are very lwedddd!!"
    #     url = await self.lewd_gifs()
    #     embed.set_image(url=f"{url}")

    #     await ctx.send(embed=embed)

    @commands.command(description=f"Returns ecchi gifs that won't be nsfw :)")
    @commands.guild_only()
    async def ecchi(self, ctx):
        r = requests.get(f"{self.Bot.api_url}ecchi").json()['url']
        em = discord.Embed()
        em.description = f"Bad image? [Report it]({self.Bot.support})"
        em.set_image(url=r)
        await ctx.send(embed=em)

    @commands.command(description=f"Sends an ero picture")
    @commands.guild_only()
    @commands.cooldown(1, 15, commands.BucketType.user)
    async def ero(self, ctx):
        if not ctx.channel.is_nsfw():
            await self.notnsfw(ctx=ctx)
            return
        no = random.randint(0, 1)
        if no == 0:
            url = nekos.img(target="ero")
            embed = discord.Embed(color=random.choice(self.Bot.color_list))

            embed.set_image(url=f"{url}")
            await ctx.send(embed=embed)
        if no == 1:
            url = hmtai.useHM("v2", "ero")
            await self.waifu_embed(ctx=ctx, link=url)

    @commands.command(description=f"Sends a cumm picture.")
    @commands.guild_only()
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def cum(self, ctx, amount:int=0):

        if not ctx.channel.is_nsfw():
            await self.notnsfw(ctx=ctx)
            return
        if amount != 0:
            return await self.send_image(ctx, "cum", amount)
        r = requests.get(f"{self.Bot.api_url}cum").json()['url']
        em = discord.Embed()
        em.description = f"Bad image? [Report it]({self.Bot.support})"
        em.set_image(url=r)
        await ctx.send(embed=em)
        
    @commands.command(description=f"Sends a futanari picture.")
    @commands.guild_only()
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def futanari(self, ctx, amount:int = 0):

        if not ctx.channel.is_nsfw():
            await self.notnsfw(ctx=ctx)
            return
        if amount != 0:
            return await self.send_image(ctx, "futanari", amount)
        r = requests.get(f"{self.Bot.api_url}futanari").json()['url']
        em = discord.Embed()
        em.description = f"Bad image? [Report it]({self.Bot.support})"
        em.set_image(url=r)
        await ctx.send(embed=em)

    @commands.command(description=f"Sends a femdom picture.", usage = "dh femdom 5")
    @commands.guild_only()
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def femdom(self, ctx, amount: int = 0):

        if not ctx.channel.is_nsfw():
            await self.notnsfw(ctx=ctx)
            return
        if amount != 0:
            return await self.send_image(ctx, "femdom", amount)
        r = requests.get(f"{self.Bot.api_url}femdom").json()['url']
        em = discord.Embed()
        em.description = f"Bad image? [Report it]({self.Bot.support})"
        em.set_image(url=r)
        await ctx.send(embed=em)

    @commands.command(description=f"Sends a yuri picture.", usage="dh yuri 9")
    @commands.guild_only()
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def yuri(self, ctx, amount: int = 0):

        if not ctx.channel.is_nsfw():
            await self.notnsfw(ctx=ctx)
            return
        if amount != 0:
            return await self.send_image(ctx, "yuri", amount)

        r = requests.get(f"{self.Bot.api_url}yuri").json()['url']
        em = discord.Embed()
        em.description = f"Bad image? [Report it]({self.Bot.support})"
        em.set_image(url=r)
        await ctx.send(embed=em)

    @commands.command(description=f"Sends a ass picture.", usage="dh ass 10")
    @commands.guild_only()
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def ass(self, ctx, amount: int = 0):

        if not ctx.channel.is_nsfw():
            await self.notnsfw(ctx=ctx)
            return
        if amount != 0:
            return await self.send_image(ctx, "ass", amount)
        r = requests.get(f"{self.Bot.api_url}ass").json()['url']
        em = discord.Embed()
        em.description = f"Bad image? [Report it]({self.Bot.support})"
        em.set_image(url=r)
        await ctx.send(embed=em)

    @commands.command(description=f"Sends a creampie picture.")
    @commands.guild_only()
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def creampie(self, ctx, amount: int = 0):
        if not ctx.channel.is_nsfw():
            await self.notnsfw(ctx=ctx)
            return
        if amount != 0:
            return await self.send_image(ctx, "creampie", amount)
        r = requests.get(f"{self.Bot.api_url}creampie").json()['url']
        em = discord.Embed()
        em.description = f"Bad image? [Report it]({self.Bot.support})"
        em.set_image(url=r)
        await ctx.send(embed=em)

    @commands.command(description=f"Weird fetish ok!", usage= "dh cuckold 2", aliases=['netorare'])
    @commands.guild_only()
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def cuckold(self, ctx, amount:int = 0):
        if not ctx.channel.is_nsfw():
            await self.notnsfw(ctx=ctx)
            return
        if amount != 0:
            return await self.send_image(ctx, "cuckold", amount)
        r = requests.get(f"{self.Bot.api_url}cuckold").json()['url']
        em = discord.Embed()
        em.description = f"Bad image? [Report it]({self.Bot.support})"
        em.set_image(url=r)
        await ctx.send(embed=em)

    @commands.command(description=f"5vs1", usage= "dh gangbang 4")
    @commands.guild_only()
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def gangbang(self, ctx, amount:int = 0):
        if not ctx.channel.is_nsfw():
            await self.notnsfw(ctx=ctx)
            return
        # no = random.randint(0,1)
        if amount != 0:
            return await self.send_image(ctx, "gangbang", amount)
        r = requests.get(f"{self.Bot.api_url}gangbang").json()['url']
        em = discord.Embed()
        em.description = f"Bad image? [Report it]({self.Bot.support})"
        em.set_image(url=r)
        await ctx.send(embed=em)

    @commands.command(description=f"OwO")
    @commands.guild_only()
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def boobjob(self, ctx, amount: int = 0):
        if not ctx.channel.is_nsfw():
            await self.notnsfw(ctx=ctx)
            return
        if amount != 0:
            return await self.send_image(ctx, "boobjob", amount)

        r = requests.get(f"{self.Bot.api_url}boobjob").json()['url']
        em = discord.Embed()
        em.description = f"Bad image? [Report it]({self.Bot.support})"
        em.set_image(url=r)
        await ctx.send(embed=em)

    @commands.command(description=f"Owo")
    @commands.guild_only()
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def ahegao(self, ctx):
        if not ctx.channel.is_nsfw():
            await self.notnsfw(ctx=ctx)
            return

        await ctx.send((hmtai.useHM("v2-4", "ahegao")))

    @commands.command(description=f"OwO")
    @commands.guild_only()
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def public(self, ctx, amount: int = 0):
        if not ctx.channel.is_nsfw():
            await self.notnsfw(ctx=ctx)
            return
        if amount != 0:
            return await self.send_image(ctx, "public", amount)
        r = requests.get(f"{self.Bot.api_url}public").json()['url']
        em = discord.Embed()
        em.description = f"Bad image? [Report it]({self.Bot.support})"
        em.set_image(url=r)
        await ctx.send(embed=em)

    @commands.command()
    @commands.guild_only()
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def solo(self, ctx, amount: int = 1):
        if not ctx.channel.is_nsfw():
            await self.notnsfw(ctx=ctx)
            return
        if amount != 0:
            return await self.send_image(ctx, "solo", amount)

        r = requests.get(f"{self.Bot.api_url}solo").json()['url']
        em = discord.Embed()
        em.description = f"Bad image? [Report it]({self.Bot.support})"
        em.set_image(url=r)
        await ctx.send(embed=em)

    @commands.command(aliases= ["erofeet"])
    @commands.guild_only()
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def feet(self, ctx, amount: int = 0):
        if not ctx.channel.is_nsfw():
            await self.notnsfw(ctx=ctx)
            return

        if amount != 0:
            return await self.send_image(ctx, "feet", amount)
        r = requests.get(f"{self.Bot.api_url}feet").json()['url']
        em = discord.Embed()
        em.description = f"Bad image? [Report it]({self.Bot.support})"
        em.set_image(url=r)
        await ctx.send(embed=em)

    @commands.command(description=f"Sends a trap picture.")
    @commands.guild_only()
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def trap(self, ctx, amount : int = 0):
        if not ctx.channel.is_nsfw():
            await self.notnsfw(ctx=ctx)
            return
        if amount != 0:
            return await self.send_image(ctx, "trap", amount)

        r = requests.get(f"{self.Bot.api_url}trap").json()['url']
        em = discord.Embed()
        em.description = f"Bad image? [Report it]({self.Bot.support})"
        em.set_image(url=r)
        await ctx.send(embed=em)

    @commands.command(description=f"Glasses lady yay!")
    @commands.guild_only()
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def glasses(self, ctx, amount: int = 0):
        if not ctx.channel.is_nsfw():
            await self.notnsfw(ctx=ctx)
            return
        if amount != 0:
            return await self.send_image(ctx, "glasses", amount)
        r = requests.get(f"{self.Bot.api_url}glasses").json()['url']
        em = discord.Embed()
        em.description = f"Bad image? [Report it]({self.Bot.support})"
        em.set_image(url=r)
        await ctx.send(embed=em)


    @commands.command(description=f"Sends a cat pic :kek:")
    @commands.guild_only()
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def pussy(self, ctx, amount: int = 0):
        if not ctx.channel.is_nsfw():
            await self.notnsfw(ctx=ctx)
            return
        if amount != 0:
            return await self.send_image(ctx, "pussy", amount)
        r = requests.get(f"{self.Bot.api_url}pussy").json()['url']
        em = discord.Embed()
        em.description = f"Bad image? [Report it]({self.Bot.support})"
        em.set_image(url=r)
        await ctx.send(embed=em)

    @commands.command(description=f"Sends a NSFW picture where the lead is in a formal uniform.")
    @commands.guild_only()
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def uniform(self, ctx, amount:int = 0):
        if not ctx.channel.is_nsfw():
            await self.notnsfw(ctx=ctx)
            return
        if amount != 0:

            return await self.send_image(ctx, "uniform", amount)
        r = requests.get(f"{self.Bot.api_url}uniform").json()['url']
        em = discord.Embed()
        em.description = f"Bad image? [Report it]({self.Bot.support})"
        em.set_image(url=r)
        await ctx.send(embed=em)

    @commands.command(description=f"Thicc")
    @commands.guild_only()
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def thighs(self, ctx, amount: int = 0):
        if not ctx.channel.is_nsfw():
            await self.notnsfw(ctx=ctx)
            return
        if amount != 0:
            return await self.send_image(ctx, "thighs", amount)

        r = requests.get(f"{self.Bot.api_url}thighs").json()['url']
        em = discord.Embed()
        em.description = f"Bad image? [Report it]({self.Bot.support})"
        em.set_image(url=r)
        await ctx.send(embed=em)

    @commands.command(description=f"Returns anal images and gifs.")
    @commands.guild_only()
    async def anal(self, ctx, amount: int = 0):
        if not ctx.channel.is_nsfw():
            await self.notnsfw(ctx=ctx)
            return
        if amount != 0:
            return await self.send_image(ctx, "anal", amount)

        r = requests.get(f"{self.Bot.api_url}anal").json()['url']
        em = discord.Embed()
        em.description = f"Bad image? [Report it]({self.Bot.support})"
        em.set_image(url=r)
        await ctx.send(embed=em)

    async def send_image(self, ctx, tag: str, amount: int):
        if amount > 10:
            return await ctx.send("Can't go higher than 10.")
        i = 1
        urls = requests.get(f"{self.Bot.api_url}{tag}/{amount}").json()['urls']
        try:
            if amount <= 5:
                await ctx.send("\n".join(urls[:amount]))
            if amount > 5:
                await ctx.send("\n".join(urls[:5]))
                await ctx.send("\n".join(urls[5:amount]))
        except:
            return await ctx.send("ERROR!")

    @commands.command(usage=f"dh nsfw 10 ",
                      description="From a collection of more than 25000+ images and gifs sends a random one.")
    @commands.guild_only()
    async def nsfw(self, ctx, amount: int = 0):
        if not ctx.channel.is_nsfw():
            await self.notnsfw(ctx=ctx)
            return

        if amount != 0:
            return await self.send_image(ctx, "nsfw", amount)

        r = requests.get(f"{self.Bot.api_url}nsfw").json()['url']
        em = discord.Embed()
        em.description = f"Bad image? [Report it]({self.Bot.support})"
        em.set_image(url=r)
        await ctx.send(embed=em)

    async def waifu_embed(self, ctx, link, dl=None):
        embed = discord.Embed(color=random.choice(self.Bot.color_list))
        if dl != None:
            embed.description = f"[Link]({dl})"

        embed.set_image(url=f"{link}")
        await ctx.send(embed=embed)
        return

    @commands.command()
    @commands.guild_only()
    @commands.cooldown(1, 10, commands.BucketType.user)
    async def megumin(self, ctx):
        url = f"https://api.waifu.pics/sfw/megumin"
        data = requests.get(f"{url}").json()
        link = data['url']
        await self.waifu_embed(ctx=ctx, link=link)

    @commands.command(aliases=['tits' , 'boobs'])
    @commands.guild_only()
    @commands.cooldown(1, 10, commands.BucketType.user)
    async def oppai(self, ctx, amount: int = 0):
        if not ctx.channel.is_nsfw():
            await self.notnsfw(ctx=ctx)
            return
        if amount != 0:
            return await self.send_image(ctx, "oppai", amount)

        r = requests.get(f"{self.Bot.api_url}oppai").json()['url']
        em = discord.Embed()
        em.set_image(url=r)
        await ctx.send(embed=em)

    @commands.command()
    @commands.guild_only()
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def neko(self, ctx, user: discord.Member = None):
        if not ctx.channel.is_nsfw():
            await self.notnsfw(ctx=ctx)
            return
        no = random.randint(0, 2)
        if no == 0:

            url = f"https://api.waifu.pics/nsfw/neko"
            data = requests.get(f"{url}").json()
            link = data['url']
            if user == None:
                await self.waifu_embed(ctx=ctx, link=link)

            elif user != None:

                embed = discord.Embed(color=random.choice(self.Bot.color_list))

                embed.set_image(url=f"{link}")
                embed.description = f"{ctx.author.mention} lewds {user.mention}"
                await ctx.send(embed=embed)
        if no == 1:
            url = nekos.img(target="nsfw_neko_gif")
            await self.waifu_embed(ctx=ctx, link=url)
        if no == 2:
            url = hmtai.useHM("v2-4", "nsfwNeko")
            await self.waifu_embed(ctx=ctx, link=url)

    @commands.command()
    @commands.guild_only()
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def cat(self, ctx):
        embed = discord.Embed(color=random.choice(self.Bot.color_list))
        embed.description = f"Neko!"
        embed.set_footer(text=f"Requested by {ctx.author.name}")
        embed.set_image(url=nekos.cat())
        await ctx.send(embed=embed)

    @commands.command()
    @commands.guild_only()
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def wallpaper(self, ctx):

        if ctx.channel.is_nsfw():
            embed = discord.Embed(color=random.choice(self.Bot.color_list))
            embed.set_footer(text=f"Requested by {ctx.author.name}")
            embed.set_image(url=nekos.img(target="wallpaper"))
            await ctx.send(embed=embed)
        else:
            url = "https://memes.blademaker.tv/api/animewallpaper"
            data = requests.get(f"{url}").json()
            if data["nsfw"] == False:
                link = (data['image'])
                await self.waifu_embed(ctx=ctx, link=link, dl=link)

    @commands.command()
    @commands.guild_only()
    async def owofy(self, ctx, *, YourText):
        owo = owoConvert(YourText)
        await ctx.send(owo)

    @commands.command()
    @commands.guild_only()
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def tickle(self, ctx, user: discord.Member = None):
        url = nekos.img(target="tickle")
        if user is None:

            await self.waifu_embed(ctx=ctx, link=url)

        else:
            embed = discord.Embed(color=random.choice(self.Bot.color_list))

            embed.set_image(url=f"{url}")
            embed.description = f"{ctx.author.mention} tickles {user.mention}"
            await ctx.send(embed=embed)

    @commands.command()
    @commands.guild_only()
    @commands.cooldown(1, 10, commands.BucketType.user)
    async def baka(self, ctx, user: discord.Member = None):
        url = nekos.img(target="baka")
        if user is None:

            await ctx.send(f"No you are not a baka {ctx.author.name}.")

        else:
            embed = discord.Embed(color=random.choice(self.Bot.color_list))

            embed.set_image(url=f"{url}")
            embed.description = f"{user.mention} BAKA!"
            await ctx.send(embed=embed)

    @commands.command()
    @commands.guild_only()
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def animefood(self, ctx):
        await self.get_nekobot(ctx=ctx, query="food")

    async def get_nekobot(self, ctx, query):
        url = f"https://nekobot.xyz/api/image?type={query}"
        data = requests.get(f"{url}").json()
        image = data['message']
        embed = discord.Embed(color=random.choice(self.Bot.color_list))

        embed.set_image(url=f"{image}")
        return await ctx.send(embed=embed)

    @commands.command(usage = "dh reddit anime",
        description = "Sends a random picture from the given subreddit, no need to include `r/`."
        )
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def reddit(self, ctx, subreddit):
            url = f"https://memes.blademaker.tv/api/{subreddit}"
            data = requests.get(f"{url}").json()
            if data["nsfw"] == False:
                link = (data['image'])
                await self.waifu_embed(ctx=ctx, link=link, dl=link)

            else:
                if not ctx.channel.is_nsfw():
                    return self.notnsfw(self, ctx = ctx)
                link = data['image']
                await self.waifu_embed(ctx=ctx, link=link, dl=link)
                
def setup(Bot):
    Bot.add_cog(vein3(Bot))
    print("APIs cog is working.")
