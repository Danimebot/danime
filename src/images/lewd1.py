
import discord
import random
from random import randint
import requests
from discord.ext import commands


class api2(commands.Cog, name="api2"):
	def __init__(self, Bot):
		self.Bot = Bot
	async def send_image(self, ctx, tag:str, amount:int):
		if amount > 10:
			return await ctx.send("Can't go higher than 10.")
		urls = requests.get(f"{self.Bot.api_url}{tag}/{amount}").json()['urls']
		a = 0 
		b = 5
		while len(urls) >= a:
			try:
				await ctx.send(content = f"```Images powered by https://danimebot.xyz/```" + f"\n".join(urls[a:b]))
			except Exception:
				break
			a += 5
			b += 5

	async def notnsfw(self, ctx):
		embed = discord.Embed(color = random.choice(self.Bot.color_list))
		embed.title= f"Non-NSFW channel detected!"
		embed.add_field(name="Why should you care?", value=f"Discord forbids the use of NSFW content outside the NSFW-option enabled channels. [More here](https://discord.com/guidelines#:~:text=You%20must%20apply%20the%20NSFW,sexualize%20minors%20in%20any%20way.)", inline=False)
		embed.add_field(name="How can I enable the NSFW channel option?", value=f"** **", inline=False)
		embed.set_image(url=f"https://cdn.discordapp.com/attachments/802518639274229800/802936914054610954/nsfw.gif")
		embed.set_footer(text=f"Pro tip: {self.Bot.DEFAULT_PREFIX}set_nsfw can do the work for you.")
		await ctx.send(embed=embed)

	async def waifu_embed(self, ctx, link, dl = None):
		embed = discord.Embed(color =random.choice(self.Bot.color_list))
		embed.description = f"Bad image? [Report it]({self.Bot.support})"
		if dl != None:
			embed.description=f"[Link]({dl})"

		embed.set_image(url=f"{link}")
		await ctx.send(embed=embed)
		

	async def getreddit(self, sub):
		r = requests.get(f"https://meme-api.herokuapp.com/gimme/{sub}").json()
		return r['url']

	async def danimeapi(self, tag):
		data = requests.get(f"{self.Bot.api_url}{tag}").json()
		image = data['url']
		return image

	@commands.command(description="Get multiple tag relat images, 2 tags are available for free usage with 10 images at a time.", usage="dh multiple nsfw+oppai 10")
	@commands.guild_only()
	@commands.cooldown(1, 5, commands.BucketType.user)
	async def multiple(self, ctx, tags:str, amount:int=1):
		url = f"{self.Bot.api_url}multiple/{tags}/{amount}"
		tags = tags.split("+")
		if len(tags) > 2:
			return await ctx.send("Sorry you can't request more than two tags, `dh premium` if you do want to.")
		if amount > 10:
			return await ctx.send("Sorry you can't request more than 10 images at a time, `dh premium` if you do want to.")
		urls = requests.get(url).json()['urls']
		a = 0 
		b = 5
		while len(urls) >= a:
			try:
				await ctx.send("```py\nMultiple tagged images.``` "+"\n".join(urls[a:b]))
			except Exception:
				break
			a += 5
			b += 5		




	@commands.command()
	@commands.guild_only()
	@commands.cooldown(1, 5, commands.BucketType.user)
	async def zerotwo(self, ctx, amount:int=0):
		if not ctx.channel.is_nsfw():
			await self.notnsfw(ctx=ctx)
			return
		if  amount != 0:
			return await self.send_image(ctx, "zerotwo", amount)

		random1 = random.randint(0,1)
		pages = ['ZeroTwoHentai']
		if random1 ==0:
			url = await self.getreddit(sub = f"{random.choice(pages)}")
			await self.waifu_embed(ctx=ctx, link = url)
		if random1 == 1:
			url = await self.danimeapi(tag="zerotwo")
			await self.waifu_embed(ctx=ctx, link = url)
		

	@commands.command()
	@commands.guild_only()
	@commands.cooldown(1, 5, commands.BucketType.user)
	async def konosuba(self, ctx, amount:int=0):
		if not ctx.channel.is_nsfw():
			await self.notnsfw(ctx=ctx)
			return
		if  amount != 0:
			return await self.send_image(ctx, "konosuba", amount)			
		url = await self.danimeapi(tag = "konosuba")
		await self.waifu_embed(ctx=ctx, link =url)

	@commands.command()
	@commands.guild_only()
	@commands.cooldown(1, 5, commands.BucketType.user)
	async def bdsm(self, ctx, amount:int=0):
		if not ctx.channel.is_nsfw():
			await self.notnsfw(ctx=ctx)
			return
		if  amount != 0:
			return await self.send_image(ctx, "bdsm", amount)			
		url = await self.danimeapi(tag="bdsm")
		await self.waifu_embed(ctx=ctx, link=url)


	@commands.command()
	@commands.guild_only()
	@commands.cooldown(1, 5, commands.BucketType.user)
	async def panties(self, ctx, amount:int=0):
		if not ctx.channel.is_nsfw():
			await self.notnsfw(ctx=ctx)
			return
		if  amount != 0:
			return await self.send_image(ctx, "panties", amount)			
		url = await self.danimeapi(tag="panties")
		await self.waifu_embed(ctx=ctx, link=url)	
	

	@commands.command(usage = "dh milf 4")
	@commands.guild_only()
	@commands.cooldown(1, 5, commands.BucketType.user)
	async def elves(self, ctx, amount:int=0):
		if not ctx.channel.is_nsfw():
			await self.notnsfw(ctx=ctx)
			return
		if  amount != 0:
			return await self.send_image(ctx, "elves", amount)			
		url = await self.danimeapi(tag="elves")
		await self.waifu_embed(ctx=ctx, link=url)	

	@commands.command(usage = "dh milf 2")
	@commands.cooldown(1, 5, commands.BucketType.user)
	async def milf(self, ctx, amount:int=0):
		if not ctx.channel.is_nsfw():
			await self.notnsfw(ctx=ctx)
			return
		if  amount != 0:
			return await self.send_image(ctx, "milf", amount)			
		url = await self.danimeapi(tag="milf")
		await self.waifu_embed(ctx=ctx, link=url)

	@commands.command(usage = "dh rem 5")
	@commands.cooldown(1, 5, commands.BucketType.user)
	async def rem(self, ctx, amount:int=0):
		if not ctx.channel.is_nsfw():
			await self.notnsfw(ctx=ctx)
			return
		if  amount != 0:
			return await self.send_image(ctx, "rem", amount)			
		url = await self.danimeapi(tag="rem")
		await self.waifu_embed(ctx=ctx, link=url)
		
	@commands.command(usage=f"dh tsunade 9")
	@commands.cooldown(1, 5, commands.BucketType.user)
	async def tsunade(self, ctx, amount:int=0):
		if not ctx.channel.is_nsfw():
			await self.notnsfw(ctx=ctx)
			return
		if  amount != 0:
			return await self.send_image(ctx, "tsunade", amount)			
		url = await self.danimeapi(tag="tsunade")
		await self.waifu_embed(ctx=ctx, link=url)

	@commands.command(usage=f"dh naruto 9")
	@commands.cooldown(1, 5, commands.BucketType.user)
	async def naruto(self, ctx, amount:int=0):
		if not ctx.channel.is_nsfw():
			await self.notnsfw(ctx=ctx)
			return
		if  amount != 0:
			return await self.send_image(ctx, "naruto", amount)			
		url = await self.danimeapi(tag="naruto")
		await self.waifu_embed(ctx=ctx, link=url)

	@commands.command(usage=f"dh fate 3")
	@commands.cooldown(1, 5, commands.BucketType.user)
	async def fate(self, ctx, amount:int=0):
		if not ctx.channel.is_nsfw():
			await self.notnsfw(ctx=ctx)
			return
		if  amount != 0:
			return await self.send_image(ctx, "fate", amount)			
		url = await self.danimeapi(tag="fate")
		await self.waifu_embed(ctx=ctx, link=url)

	@commands.command(usage=f"dh dragonball 9")
	@commands.cooldown(1, 5, commands.BucketType.user)
	async def dragonball(self, ctx, amount:int=0):
		if not ctx.channel.is_nsfw():
			await self.notnsfw(ctx=ctx)
			return
		if  amount != 0:
			return await self.send_image(ctx, "dragonball", amount)			
		url = await self.danimeapi(tag="dragonball")
		await self.waifu_embed(ctx=ctx, link=url)

	@commands.command(usage="dh furry 6")
	@commands.cooldown(1, 5, commands.BucketType.user)
	async def furry(self, ctx, amount:int=0):
		if not ctx.channel.is_nsfw():
			await self.notnsfw(ctx=ctx)
			return
		if  amount != 0:
			return await self.send_image(ctx, "furry", amount)			
		url = await self.danimeapi(tag="furry")
		await self.waifu_embed(ctx=ctx, link=url)

	@commands.command(usage = "dh pantyhose 5")
	@commands.cooldown(1, 5, commands.BucketType.user)
	async def pantyhose(self, ctx, amount:int=0):
		if not ctx.channel.is_nsfw():
			await self.notnsfw(ctx=ctx)
			return
		if  amount != 0:
			return await self.send_image(ctx, "pantyhose", amount)			
		url = await self.danimeapi(tag="pantyhose")
		await self.waifu_embed(ctx=ctx, link=url)

	@commands.command(usage = "dh stockings 5", description="Damm them stockings")
	@commands.cooldown(1, 5, commands.BucketType.user)
	async def stockings(self, ctx, amount:int=0):
		if not ctx.channel.is_nsfw():
			await self.notnsfw(ctx=ctx)
			return
		if  amount != 0:
			return await self.send_image(ctx, "stockings", amount)			
		url = await self.danimeapi(tag="stockings")
		await self.waifu_embed(ctx=ctx, link=url)

	@commands.command(usage = "dh bunnygirl 5")
	@commands.cooldown(1, 5, commands.BucketType.user)
	async def bunnygirl(self, ctx, amount:int=0):
		if not ctx.channel.is_nsfw():
			await self.notnsfw(ctx=ctx)
			return
		if  amount != 0:
			return await self.send_image(ctx, "bunnygirl", amount)			
		url = await self.danimeapi(tag="bunnygirl")
		await self.waifu_embed(ctx=ctx, link=url)

	@commands.command(usage = "dh quintuplets 5", aliases=['gotobun']
		, description="Gives out images from the anime The Quintessential Quintuplets.")
	@commands.cooldown(1, 5, commands.BucketType.user)
	async def quintuplets(self, ctx, amount:int=0):
		if not ctx.channel.is_nsfw():
			await self.notnsfw(ctx=ctx)
			return
		if  amount != 0:
			return await self.send_image(ctx, "quintuplets", amount)			
		url = await self.danimeapi(tag="quintuplets")
		await self.waifu_embed(ctx=ctx, link=url)

	@commands.command(usage = "dh hairy 5", aliases=['hairy']
		, description="Bush? Please don't trim them :pleading_face:")
	@commands.cooldown(1, 5, commands.BucketType.user)
	async def bush(self, ctx, amount:int=0):
		if not ctx.channel.is_nsfw():
			await self.notnsfw(ctx=ctx)
			return
		if  amount != 0:
			return await self.send_image(ctx, "bush", amount)			
		url = await self.danimeapi(tag="bush")
		await self.waifu_embed(ctx=ctx, link=url)

	@commands.command(usage = "dh thicc 5"
		, description="THICCCCCCCCCCCCCCCCCCCC")
	@commands.cooldown(1, 5, commands.BucketType.user)
	async def thicc(self, ctx, amount:int=0):
		if not ctx.channel.is_nsfw():
			await self.notnsfw(ctx=ctx)
			return
		if  amount != 0:
			return await self.send_image(ctx, "thicc", amount)			
		url = await self.danimeapi(tag="thicc")
		await self.waifu_embed(ctx=ctx, link=url)

	@commands.command(usage = "dh league 5"
		, description="League Of Legends")
	@commands.cooldown(1, 5, commands.BucketType.user)
	async def league(self, ctx, amount:int=0):
		if not ctx.channel.is_nsfw():
			await self.notnsfw(ctx=ctx)
			return
		if  amount != 0:
			return await self.send_image(ctx, "league", amount)			
		url = await self.danimeapi(tag="league")
		await self.waifu_embed(ctx=ctx, link=url)

	@commands.command(usage = "dh fitness 5"
		, description="Girls that you are afraid of.")
	@commands.cooldown(1, 5, commands.BucketType.user)
	async def fitness(self, ctx, amount:int=0):
		if not ctx.channel.is_nsfw():
			await self.notnsfw(ctx=ctx)
			return
		if  amount != 0:
			return await self.send_image(ctx, "fitness", amount)			
		url = await self.danimeapi(tag="fitness")
		await self.waifu_embed(ctx=ctx, link=url)



	@commands.command(usage = "dh gifs 5"
		, description="Animated gifs at your door.")
	@commands.cooldown(1, 5, commands.BucketType.user)
	async def gifs(self, ctx, amount:int=0):
		if not ctx.channel.is_nsfw():
			await self.notnsfw(ctx=ctx)
			return
		if  amount != 0:
			return await self.send_image(ctx, "gifs", amount)			
		url = await self.danimeapi(tag="gifs")
		await self.waifu_embed(ctx=ctx, link=url)


	@commands.command(usage = "dh genshin 5"
		, description="Images related to your fav game, chad.")
	@commands.cooldown(1, 5, commands.BucketType.user)
	async def genshin(self, ctx, amount:int=0):
		if not ctx.channel.is_nsfw():
			await self.notnsfw(ctx=ctx)
			return
		if  amount != 0:
			return await self.send_image(ctx, "genshin", amount)			
		url = await self.danimeapi(tag="genshin")
		await self.waifu_embed(ctx=ctx, link=url)



	@commands.command(usage = "dh monstergirl 5"
		, description=":eyes:")
	@commands.cooldown(1, 5, commands.BucketType.user)
	async def monstergirl(self, ctx, amount:int=0):
		if not ctx.channel.is_nsfw():
			await self.notnsfw(ctx=ctx)
			return
		if  amount != 0:
			return await self.send_image(ctx, "monstergirl", amount)			
		url = await self.danimeapi(tag="monstergirl")
		await self.waifu_embed(ctx=ctx, link=url)


	@commands.command(usage = "dh maid 5"
		, description="WELCOME BACK MASTER!!!!!!!")
	@commands.cooldown(1, 5, commands.BucketType.user)
	async def maid(self, ctx, amount:int=0):
		if not ctx.channel.is_nsfw():
			await self.notnsfw(ctx=ctx)
			return
		if  amount != 0:
			return await self.send_image(ctx, "maid", amount)			
		url = await self.danimeapi(tag="maid")
		await self.waifu_embed(ctx=ctx, link=url)


	@commands.command(usage = "dh succubus 5"
		, description="Don't let her seduce you :eyes:")
	@commands.cooldown(1, 5, commands.BucketType.user)
	async def succubus(self, ctx, amount:int=0):
		if not ctx.channel.is_nsfw():
			await self.notnsfw(ctx=ctx)
			return
		if  amount != 0:
			return await self.send_image(ctx, "succubus", amount)			
		url = await self.danimeapi(tag="succubus")
		await self.waifu_embed(ctx=ctx, link=url)

	@commands.command(usage = "dh videos 5"
		, description="Sends hentai videos. ")
	@commands.cooldown(1, 5, commands.BucketType.user)
	async def videos(self, ctx, amount:int=0):
		if not ctx.channel.is_nsfw():
			await self.notnsfw(ctx=ctx)
			return
		if  amount != 0:
			return await self.send_image(ctx, "videos", amount)			
		url = await self.danimeapi(tag="videos")
		await self.waifu_embed(ctx=ctx, link=url)

	@commands.command(usage = "dh azurlane 5"
		, description="Images fom Azur Lane universe.")
	@commands.cooldown(1, 5, commands.BucketType.user)
	async def azurlane(self, ctx, amount:int=0):
		if not ctx.channel.is_nsfw():
			await self.notnsfw(ctx=ctx)
			return
		if  amount != 0:
			return await self.send_image(ctx, "azurlane", amount)			
		url = await self.danimeapi(tag="azurlane")
		await self.waifu_embed(ctx=ctx, link=url)

	@commands.command(usage = "dh albedo 5"
		, description="Albedo the besto succubus")
	@commands.cooldown(1, 5, commands.BucketType.user)
	async def albedo(self, ctx, amount:int=0):
		if not ctx.channel.is_nsfw():
			await self.notnsfw(ctx=ctx)
			return
		if  amount != 0:
			return await self.send_image(ctx, "albedo", amount)			
		url = await self.danimeapi(tag="albedo")
		await self.waifu_embed(ctx=ctx, link=url)

	@commands.command(usage = "dh lingerie 5"
		, description="You know the thing and so do I")
	@commands.cooldown(1, 5, commands.BucketType.user)
	async def lingerie(self, ctx, amount:int=0):
		if not ctx.channel.is_nsfw():
			await self.notnsfw(ctx=ctx)
			return
		if  amount != 0:
			return await self.send_image(ctx, "lingerie", amount)			
		url = await self.danimeapi(tag="lingerie")
		await self.waifu_embed(ctx=ctx, link=url)

	@commands.command(usage = "dh foreplay 5"
		, description="Things you will never do.")
	@commands.cooldown(1, 5, commands.BucketType.user)
	async def foreplay(self, ctx, amount:int=0):
		if not ctx.channel.is_nsfw():
			await self.notnsfw(ctx=ctx)
			return
		if  amount != 0:
			return await self.send_image(ctx, "foreplay", amount)			
		url = await self.danimeapi(tag="foreplay")
		await self.waifu_embed(ctx=ctx, link=url)

	@commands.command(usage = "dh handjob 5"
		, description="It's not much but honest work.")
	@commands.cooldown(1, 5, commands.BucketType.user)
	async def handjob(self, ctx, amount:int=0):
		if not ctx.channel.is_nsfw():
			await self.notnsfw(ctx=ctx)
			return
		if  amount != 0:
			return await self.send_image(ctx, "handjob", amount)			
		url = await self.danimeapi(tag="handjob")
		await self.waifu_embed(ctx=ctx, link=url)

	@commands.command(usage = "dh masturbation 5"
		, description="Oh yea")
	@commands.cooldown(1, 5, commands.BucketType.user)
	async def masturbation(self, ctx, amount:int=0):
		if not ctx.channel.is_nsfw():
			await self.notnsfw(ctx=ctx)
			return
		if  amount != 0:
			return await self.send_image(ctx, "masturbation", amount)			
		url = await self.danimeapi(tag="masturbation")
		await self.waifu_embed(ctx=ctx, link=url)

	@commands.command(usage = "dh swimsuit 5"
		, description="Your fav cloth!!")
	@commands.cooldown(1, 5, commands.BucketType.user)
	async def swimsuit(self, ctx, amount:int=0):
		if not ctx.channel.is_nsfw():
			await self.notnsfw(ctx=ctx)
			return
		if  amount != 0:
			return await self.send_image(ctx, "swimsuit", amount)			
		url = await self.danimeapi(tag="swimsuit")
		await self.waifu_embed(ctx=ctx, link=url)


	@commands.command(usage = "dh armpits 5"
		, description="Arm to the pits :chad:")
	@commands.cooldown(1, 5, commands.BucketType.user)
	async def armpits(self, ctx, amount:int=0):
		if not ctx.channel.is_nsfw():
			await self.notnsfw(ctx=ctx)
			return
		if  amount != 0:
			return await self.send_image(ctx, "armpits", amount)			
		url = await self.danimeapi(tag="armpits")
		await self.waifu_embed(ctx=ctx, link=url)


	@commands.command(usage = "dh wet"
		, description="Sweaty girls!!")
	@commands.cooldown(1, 5, commands.BucketType.user)
	async def wet(self, ctx, amount:int=0):
		if not ctx.channel.is_nsfw():
			await self.notnsfw(ctx=ctx)
			return
		if  amount != 0:
			return await self.send_image(ctx, "wet", amount)			
		url = await self.danimeapi(tag="wet")
		await self.waifu_embed(ctx=ctx, link=url)



def setup (Bot):
	Bot.add_cog(api2(Bot))
	print("Api2 is working")