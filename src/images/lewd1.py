
import discord
import random
from random import randint
import requests
from discord.ext import commands
from cogs.autonsfw import DanimeAPI


class api2(commands.Cog, name="api2"):
	def __init__(self, Bot):
		self.Bot = Bot
		self.danime_api = DanimeAPI(Bot)

		

	async def getreddit(self, sub):
		r = requests.get(f"https://meme-api.herokuapp.com/gimme/{sub}").json()
		return r['url']


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




	@commands.command(aliases=['zero_two'])
	@commands.guild_only()
	@commands.cooldown(1, 5, commands.BucketType.user)
	async def zerotwo(self, ctx, amount:int=0):
		if not ctx.channel.is_nsfw():
			return await self.danime_api.not_nsfw(ctx)

		if  amount != 0:
			return await self.send_image(ctx, "zerotwo", amount)

		random1 = random.randint(0,1)
		pages = ['ZeroTwoHentai']
		if random1 ==0:
			url = await self.getreddit(sub = f"{random.choice(pages)}")
			await self.danime_api.normal_image_embed(ctx=ctx, link = url)
		if random1 == 1:
			await self.danime_api.image_embed(ctx, "zerotwo")
					

	@commands.command()
	@commands.guild_only()
	@commands.cooldown(1, 5, commands.BucketType.user)
	async def konosuba(self, ctx, amount:int=0):
		if not ctx.channel.is_nsfw():
			return await self.danime_api.not_nsfw(ctx)

		if amount != 0:
			return await self.danime_api.send_images(ctx, "konosuba", amount)

		await self.danime_api.image_embed(ctx, "konosuba")


	@commands.command()
	@commands.guild_only()
	@commands.cooldown(1, 5, commands.BucketType.user)
	async def bdsm(self, ctx, amount:int=0):
		if not ctx.channel.is_nsfw():
			return await self.danime_api.not_nsfw(ctx)

		if amount != 0:
			return await self.danime_api.send_images(ctx, "bdsm", amount)

		await self.danime_api.image_embed(ctx, "bdsm")


	@commands.command()
	@commands.guild_only()
	@commands.cooldown(1, 5, commands.BucketType.user)
	async def panties(self, ctx, amount:int=0):
		if not ctx.channel.is_nsfw():
			return await self.danime_api.not_nsfw(ctx)

		if amount != 0:
			return await self.danime_api.send_images(ctx, "panties", amount)

		await self.danime_api.image_embed(ctx, "panties")
	

	@commands.command(usage = "dh elves 4")
	@commands.guild_only()
	@commands.cooldown(1, 5, commands.BucketType.user)
	async def elves(self, ctx, amount:int=0):
		if not ctx.channel.is_nsfw():
			return await self.danime_api.not_nsfw(ctx)

		if amount != 0:
			return await self.danime_api.send_images(ctx, "elves", amount)

		await self.danime_api.image_embed(ctx, "elves")	

	@commands.command(usage = "dh milf 2")
	@commands.cooldown(1, 5, commands.BucketType.user)
	async def milf(self, ctx, amount:int=0):
		if not ctx.channel.is_nsfw():
			return await self.danime_api.not_nsfw(ctx)

		if amount != 0:
			return await self.danime_api.send_images(ctx, "milf", amount)

		await self.danime_api.image_embed(ctx, "milf")

	@commands.command(usage = "dh rem 5")
	@commands.cooldown(1, 5, commands.BucketType.user)
	async def rem(self, ctx, amount:int=0):
		if not ctx.channel.is_nsfw():
			return await self.danime_api.not_nsfw(ctx)

		if amount != 0:
			return await self.danime_api.send_images(ctx, "rem", amount)

		await self.danime_api.image_embed(ctx, "rem")
		
	@commands.command(usage=f"dh tsunade 9")
	@commands.cooldown(1, 5, commands.BucketType.user)
	async def tsunade(self, ctx, amount:int=0):
		if not ctx.channel.is_nsfw():
			return await self.danime_api.not_nsfw(ctx)

		if amount != 0:
			return await self.danime_api.send_images(ctx, "tsunade", amount)

		await self.danime_api.image_embed(ctx, "tsunade")

	@commands.command(usage=f"dh naruto 9")
	@commands.cooldown(1, 5, commands.BucketType.user)
	async def naruto(self, ctx, amount:int=0):
		if not ctx.channel.is_nsfw():
			return await self.danime_api.not_nsfw(ctx)

		if amount != 0:
			return await self.danime_api.send_images(ctx, "naruto", amount)

		await self.danime_api.image_embed(ctx, "naruto")
	@commands.command(usage=f"dh fate 3")
	@commands.cooldown(1, 5, commands.BucketType.user)
	async def fate(self, ctx, amount:int=0):
		if not ctx.channel.is_nsfw():
			return await self.danime_api.not_nsfw(ctx)

		if amount != 0:
			return await self.danime_api.send_images(ctx, "fate", amount)

		await self.danime_api.image_embed(ctx, "fate")

	@commands.command(usage=f"dh dragonball 9", aliases=['dragon_ball'])
	@commands.cooldown(1, 5, commands.BucketType.user)
	async def dragonball(self, ctx, amount:int=0):
		if not ctx.channel.is_nsfw():
			return await self.danime_api.not_nsfw(ctx)

		if amount != 0:
			return await self.danime_api.send_images(ctx, "dragonball", amount)

		await self.danime_api.image_embed(ctx, "dragonball")

	# @commands.command(usage="dh furry 6")
	# @commands.cooldown(1, 5, commands.BucketType.user)
	# async def furry(self, ctx, amount:int=0):
	# 	if not ctx.channel.is_nsfw():
	# 		return await self.danime_api.not_nsfw(ctx)

	# 	if  amount != 0:
	# 		return await self.send_image(ctx, "furry", amount)			
	# 	url = await self.danimeapi(tag="furry")
	# 	await self.waifu_embed(ctx=ctx, link=url)

	@commands.command(usage = "dh pantyhose 5")
	@commands.cooldown(1, 5, commands.BucketType.user)
	async def pantyhose(self, ctx, amount:int=0):
		if not ctx.channel.is_nsfw():
			return await self.danime_api.not_nsfw(ctx)

		if amount != 0:
			return await self.danime_api.send_images(ctx, "pantyhose", amount)

		await self.danime_api.image_embed(ctx, "pantyhose")

	@commands.command(usage = "dh stockings 5", description="Damm them stockings")
	@commands.cooldown(1, 5, commands.BucketType.user)
	async def stockings(self, ctx, amount:int=0):
		if not ctx.channel.is_nsfw():
			return await self.danime_api.not_nsfw(ctx)

		if amount != 0:
			return await self.danime_api.send_images(ctx, "stockings", amount)

		await self.danime_api.image_embed(ctx, "stockings")

	@commands.command(usage = "dh bunnygirl 5")
	@commands.cooldown(1, 5, commands.BucketType.user)
	async def bunnygirl(self, ctx, amount:int=0):
		if not ctx.channel.is_nsfw():
			return await self.danime_api.not_nsfw(ctx)

		if amount != 0:
			return await self.danime_api.send_images(ctx, "bunnygirl", amount)

		await self.danime_api.image_embed(ctx, "bunnygirl")

	@commands.command(usage = "dh quintuplets 5", aliases=['gotobun']
		, description="Gives out images from the anime The Quintessential Quintuplets.")
	@commands.cooldown(1, 5, commands.BucketType.user)
	async def quintuplets(self, ctx, amount:int=0):
		if not ctx.channel.is_nsfw():
			return await self.danime_api.not_nsfw(ctx)

		if amount != 0:
			return await self.danime_api.send_images(ctx, "quintuplets", amount)

		await self.danime_api.image_embed(ctx, "quintuplets")

	@commands.command(usage = "dh hairy 5", aliases=['hairy']
		, description="Bush? Please don't trim them :pleading_face:")
	@commands.cooldown(1, 5, commands.BucketType.user)
	async def bush(self, ctx, amount:int=0):
		if not ctx.channel.is_nsfw():
			return await self.danime_api.not_nsfw(ctx)

		if amount != 0:
			return await self.danime_api.send_images(ctx, "bush", amount)

		await self.danime_api.image_embed(ctx, "bush")

	@commands.command(usage = "dh thicc 5"
		, description="THICCCCCCCCCCCCCCCCCCCC")
	@commands.cooldown(1, 5, commands.BucketType.user)
	async def thicc(self, ctx, amount:int=0):
		if not ctx.channel.is_nsfw():
			return await self.danime_api.not_nsfw(ctx)

		if amount != 0:
			return await self.danime_api.send_images(ctx, "thicc", amount)

		await self.danime_api.image_embed(ctx, "thicc")

	@commands.command(usage = "dh league 5"
		, description="League Of Legends")
	@commands.cooldown(1, 5, commands.BucketType.user)
	async def league(self, ctx, amount:int=0):
		if not ctx.channel.is_nsfw():
			return await self.danime_api.not_nsfw(ctx)

		if amount != 0:
			return await self.danime_api.send_images(ctx, "league", amount)

		await self.danime_api.image_embed(ctx, "league")

	@commands.command(usage = "dh fitness 5"
		, description="Girls that you are afraid of.")
	@commands.cooldown(1, 5, commands.BucketType.user)
	async def fitness(self, ctx, amount:int=0):
		if not ctx.channel.is_nsfw():
			return await self.danime_api.not_nsfw(ctx)

		if amount != 0:
			return await self.danime_api.send_images(ctx, "fitness", amount)

		await self.danime_api.image_embed(ctx, "fitness")



	@commands.command(usage = "dh gifs 5"
		, description="Animated gifs at your door.")
	@commands.cooldown(1, 5, commands.BucketType.user)
	async def gifs(self, ctx, amount:int=0):
		if not ctx.channel.is_nsfw():
			return await self.danime_api.not_nsfw(ctx)

		if amount != 0:
			return await self.danime_api.send_images(ctx, "gifs", amount)

		await self.danime_api.image_embed(ctx, "gifs")


	@commands.command(usage = "dh genshin 5"
		, description="Images related to your fav game, chad.")
	@commands.cooldown(1, 5, commands.BucketType.user)
	async def genshin(self, ctx, amount:int=0):
		if not ctx.channel.is_nsfw():
			return await self.danime_api.not_nsfw(ctx)

		if amount != 0:
			return await self.danime_api.send_images(ctx, "genshin", amount)

		await self.danime_api.image_embed(ctx, "genshin")



	@commands.command(usage = "dh monstergirl 5"
		, description=":eyes:", aliases=['monster_girl'])
	@commands.cooldown(1, 5, commands.BucketType.user)
	async def monstergirl(self, ctx, amount:int=0):
		if not ctx.channel.is_nsfw():
			return await self.danime_api.not_nsfw(ctx)

		if amount != 0:
			return await self.danime_api.send_images(ctx, "monstergirl", amount)

		await self.danime_api.image_embed(ctx, "monstergirl")


	@commands.command(usage = "dh maid 5"
		, description="WELCOME BACK MASTER!!!!!!!")
	@commands.cooldown(1, 5, commands.BucketType.user)
	async def maid(self, ctx, amount:int=0):
		if not ctx.channel.is_nsfw():
			return await self.danime_api.not_nsfw(ctx)

		if amount != 0:
			return await self.danime_api.send_images(ctx, "maid", amount)

		await self.danime_api.image_embed(ctx, "maid")

	@commands.command(usage = "dh succubus 5"
		, description="Don't let her seduce you :eyes:")
	@commands.cooldown(1, 5, commands.BucketType.user)
	async def succubus(self, ctx, amount:int=0):
		if not ctx.channel.is_nsfw():
			return await self.danime_api.not_nsfw(ctx)

		if amount != 0:
			return await self.danime_api.send_images(ctx, "succubus", amount)

		await self.danime_api.image_embed(ctx, "succubus")

	@commands.command(usage = "dh videos 5"
		, description="Sends hentai videos. ")
	@commands.cooldown(1, 5, commands.BucketType.user)
	async def videos(self, ctx, amount:int=0):
		if not ctx.channel.is_nsfw():
			return await self.danime_api.not_nsfw(ctx)

		if amount != 0:
			return await self.danime_api.send_images(ctx, "videos", amount)

		await self.danime_api.image_embed(ctx, "videos")

	@commands.command(usage = "dh azurlane 5"
		, description="Images fom Azur Lane universe.", aliases=['azur_lane'])
	@commands.cooldown(1, 5, commands.BucketType.user)
	async def azurlane(self, ctx, amount:int=0):
		if not ctx.channel.is_nsfw():
			return await self.danime_api.not_nsfw(ctx)

		if amount != 0:
			return await self.danime_api.send_images(ctx, "azurlane", amount)

		await self.danime_api.image_embed(ctx, "azurlane")

	@commands.command(usage = "dh albedo 5"
		, description="Albedo the besto succubus")
	@commands.cooldown(1, 5, commands.BucketType.user)
	async def albedo(self, ctx, amount:int=0):
		if not ctx.channel.is_nsfw():
			return await self.danime_api.not_nsfw(ctx)

		if amount != 0:
			return await self.danime_api.send_images(ctx, "albedo", amount)

		await self.danime_api.image_embed(ctx, "albedo")
	@commands.command(usage = "dh lingerie 5"
		, description="You know the thing and so do I")
	@commands.cooldown(1, 5, commands.BucketType.user)
	async def lingerie(self, ctx, amount:int=0):
		if not ctx.channel.is_nsfw():
			return await self.danime_api.not_nsfw(ctx)

		if amount != 0:
			return await self.danime_api.send_images(ctx, "lingerie", amount)

		await self.danime_api.image_embed(ctx, "lingerie")

	@commands.command(usage = "dh foreplay 5"
		, description="Things you will never do.")
	@commands.cooldown(1, 5, commands.BucketType.user)
	async def foreplay(self, ctx, amount:int=0):
		if not ctx.channel.is_nsfw():
			return await self.danime_api.not_nsfw(ctx)

		if amount != 0:
			return await self.danime_api.send_images(ctx, "foreplay", amount)

		await self.danime_api.image_embed(ctx, "foreplay")

	@commands.command(usage = "dh handjob 5"
		, description="It's not much but honest work.")
	@commands.cooldown(1, 5, commands.BucketType.user)
	async def handjob(self, ctx, amount:int=0):
		if not ctx.channel.is_nsfw():
			return await self.danime_api.not_nsfw(ctx)

		if amount != 0:
			return await self.danime_api.send_images(ctx, "handjob", amount)

		await self.danime_api.image_embed(ctx, "handjob")

	@commands.command(usage = "dh masturbation 5"
		, description="Oh yea")
	@commands.cooldown(1, 5, commands.BucketType.user)
	async def masturbation(self, ctx, amount:int=0):
		if not ctx.channel.is_nsfw():
			return await self.danime_api.not_nsfw(ctx)

		if amount != 0:
			return await self.danime_api.send_images(ctx, "masturbation", amount)

		await self.danime_api.image_embed(ctx, "masturbation")

	@commands.command(usage = "dh swimsuit 5"
		, description="Your fav cloth!!")
	@commands.cooldown(1, 5, commands.BucketType.user)
	async def swimsuit(self, ctx, amount:int=0):
		if not ctx.channel.is_nsfw():
			return await self.danime_api.not_nsfw(ctx)

		if amount != 0:
			return await self.danime_api.send_images(ctx, "swimsuit", amount)

		await self.danime_api.image_embed(ctx, "swimsuit")


	@commands.command(usage = "dh armpits 5"
		, description="Arm to the pits :chad:")
	@commands.cooldown(1, 5, commands.BucketType.user)
	async def armpits(self, ctx, amount:int=0):
		if not ctx.channel.is_nsfw():
			return await self.danime_api.not_nsfw(ctx)

		if amount != 0:
			return await self.danime_api.send_images(ctx, "armpits", amount)

		await self.danime_api.image_embed(ctx, "armpits")


	@commands.command(usage = "dh wet"
		, description="Sweaty/wet girls!!")
	@commands.cooldown(1, 5, commands.BucketType.user)
	async def wet(self, ctx, amount:int=0):
		if not ctx.channel.is_nsfw():
			return await self.danime_api.not_nsfw(ctx)

		if amount != 0:
			return await self.danime_api.send_images(ctx, "wet", amount)

		await self.danime_api.image_embed(ctx, "wet")


	@commands.command(usage = "dh darkskin", aliases=['dark_skin'],
		, description="Darkskin girls, dem good!!!")
	@commands.cooldown(1, 5, commands.BucketType.user)
	async def darkskin(self, ctx, amount:int=0):
		if not ctx.channel.is_nsfw():
			return await self.danime_api.not_nsfw(ctx)

		if amount != 0:
			return await self.danime_api.send_images(ctx, "darkskin", amount)

		await self.danime_api.image_embed(ctx, "darkskin")

def setup (Bot):
	Bot.add_cog(api2(Bot))
	print("Api2 is working")