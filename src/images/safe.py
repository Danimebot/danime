import discord
from discord.ext import commands
import requests
import random
from random import randint


class safe(commands.Cog, name = "safe"):
	def __init__(self, Bot):
		self.Bot = Bot

	async def send_image(self, ctx, tag:str, amount:int):
		if amount > 10:
			return await ctx.send("Can't go higher than 10.")
		urls = requests.get(f"{self.Bot.api_url}{tag}/{amount}").json()['urls']	
		try:
			if amount <= 5:
				await ctx.send("\n".join(urls[:amount]))
			if amount > 5:
				await ctx.send("\n".join(urls[:5]))
				await ctx.send("\n".join(urls[5:amount]))
		except :
			return await ctx.send("ERROR!")
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
		
	async def some_random_embed(self, ctx, type:str, query:str=None):
		if type != "none":
			r = requests.get(f"https://some-random-api.ml/{type}/{query}").json()
			embed = discord.Embed(color =random.choice(self.Bot.color_list))
			try: 
				embed.description = r['fact']
				embed.set_image(url = r['image'])
			except KeyError:
				embed.set_image(url = r['link'])
			
			embed.set_footer(text=f'Requested by {ctx.author.name}, Source : some-random-api.ml', icon_url=ctx.author.avatar_url)
			return await ctx.send(embed=embed)


	async def getreddit(self, sub):
		r = requests.get(f"https://meme-api.herokuapp.com/gimme/{sub}").json()
		return r['url']

	async def danimeapi(self, tag):
		data = requests.get(f"{self.Bot.api_url}{tag}").json()
		image = data['url']
		return image


	@commands.command(description='Sends a random doggo picture and also a related fact.')
	@commands.cooldown(1, 5, commands.BucketType.user)
	async def dog(self, ctx):
		await self.some_random_embed(ctx=ctx, type="animal", query="dog")

	@commands.command(description='Sends a random cat picture and also a related fact.')
	@commands.cooldown(1, 5, commands.BucketType.user)
	async def cat(self, ctx):
		await self.some_random_embed(ctx=ctx, type="animal", query="cat")

	@commands.command(description='Sends a random panda picture and also a related fact.')
	@commands.cooldown(1, 5, commands.BucketType.user)
	async def panda(self, ctx):
		await self.some_random_embed(ctx=ctx, type="animal", query="panda")

	@commands.command(description='Sends a random fox picture and also a related fact.')
	@commands.cooldown(1, 5, commands.BucketType.user)
	async def fox(self, ctx):
		await self.some_random_embed(ctx=ctx, type="animal", query="fox")

	@commands.command(description='Sends a random bird picture and also a related fact.')
	@commands.cooldown(1, 5, commands.BucketType.user)
	async def bird(self, ctx):
		await self.some_random_embed(ctx=ctx, type="animal", query="bird")

	@commands.command(description='Sends a random koala picture and also a related fact.')
	@commands.cooldown(1, 5, commands.BucketType.user)
	async def koala(self, ctx):
		await self.some_random_embed(ctx=ctx, type="animal", query="koala")

	@commands.command(description='Sends a random kangaroo picture and also a related fact.')
	@commands.cooldown(1, 5, commands.BucketType.user)
	async def kangaroo(self, ctx):
		await self.some_random_embed(ctx=ctx, type="animal", query="kangaroo")

	@commands.command(description='Sends a random raccoon picture and also a related fact.')
	@commands.cooldown(1, 5, commands.BucketType.user)
	async def raccoon(self, ctx):
		await self.some_random_embed(ctx=ctx, type="animal", query="raccoon")

	@commands.command(description='Sends a random redpanda picture and also a related fact.')
	@commands.cooldown(1, 5, commands.BucketType.user)
	async def redpanda(self, ctx):
		await self.some_random_embed(ctx=ctx, type="animal", query="red_panda")

	@commands.command(description='Sends a random pikachu picture.')
	@commands.cooldown(1, 5, commands.BucketType.user)
	async def pikachu(self, ctx):
		await self.some_random_embed(ctx=ctx, type="img", query="pikachu")


	@commands.command(description='funni')
	@commands.cooldown(1, 5, commands.BucketType.user)
	async def joke(self, ctx):
		url = "https://some-random-api.ml/joke"
		embed = discord.Embed(color =random.choice(self.Bot.color_list))
		embed.description = requests.get(url).json()['joke']
		await ctx.send(embed=embed)

	@commands.command(description='Get honry verification :eyes:')
	@commands.cooldown(1, 5, commands.BucketType.user)
	async def horny(self, ctx, user:discord.Member = None):
		if not user:
			user = ctx.author
		url = f"https://some-random-api.ml/canvas/horny?avatar={user.avatar_url_as(format='png')}"
		embed=discord.Embed(color =random.choice(self.Bot.color_list))
		embed.set_image(url = url )
		embed.description = f":eyes: {user.name} is now a certified horny."
		await ctx.send(embed=embed)


	# No, the double s is not a type, s stands for safe image.
	@commands.command(aliases=['swimsuit'], usage= "dh swimsuit 4",
		description="Get safe swimsuit boi")
	@commands.cooldown(1, 5, commands.BucketType.user)
	async def sfwswimsuit(self, ctx, amount:int=0):
		if  amount != 0:
			return await self.send_image(ctx, "sswimsuit", amount)		

		url = await self.danimeapi(tag = "sswimsuit")
		await self.waifu_embed(ctx=ctx, link =url)

	@commands.command(aliases=['sneko'], usage= "dh sneko 4",
		description= "Get cute nekos ofc SFW!")
	@commands.cooldown(1, 5, commands.BucketType.user)
	async def sfwneko(self, ctx, amount:int=0):
		if  amount != 0:
			return await self.send_image(ctx, "sneko", amount)		

		url = await self.danimeapi(tag = "sneko")
		await self.waifu_embed(ctx=ctx, link =url)


	@commands.command(aliases=['soppai'], usage= "dh soppai 4",
		description= "Get SFW oppai images ;)")
	@commands.cooldown(1, 5, commands.BucketType.user)
	async def sfwoppai(self, ctx, amount:int=0):
		if  amount != 0:
			return await self.send_image(ctx, "soppai", amount)		

		url = await self.danimeapi(tag = "soppai")
		await self.waifu_embed(ctx=ctx, link =url)

	@commands.command( usage= "dh sfw 4", description= "Get SFW images ;) dh whatis sfw for more info")
	@commands.cooldown(1, 5, commands.BucketType.user)
	async def sfw(self, ctx, amount:int=0):
		if  amount != 0:
			return await self.send_image(ctx, "sfw", amount)		

		url = await self.danimeapi(tag = "sfw")
		await self.waifu_embed(ctx=ctx, link =url)

def setup(Bot):
	Bot.add_cog(safe(Bot))
	print("Safe cog is working.")