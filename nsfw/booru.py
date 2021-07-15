import discord
from discord.ext import commands
import nsfw.imgdl as imgdl
import rule34
import aiohttp
from pygelbooru import Gelbooru
from nsfw.hentaii import hentaii
import random

class booru(commands.Cog, name="booru"):
	def __init__(self, Bot):
		self.Bot = Bot
		global nsfwToggledGuilds
		nsfwToggledGuilds = self.Bot.nsfwToggledGuilds
		

	async def togglecheck(ctx):
		if ctx.guild.id in nsfwToggledGuilds:
			return True
		em = discord.Embed(
			description = "Hey, it seems you used an image command with images not monitored by the bot, contact an admin and use the command `dh nsfwtoggle enable` to be able to use this command.")
		await ctx.send(embed = em)
		return False

	async def send_image(self, ctx , urls, amount):
		random.shuffle(urls)
		try:

			if amount <= 5:
				await ctx.send("\n".join(urls[:amount]))
			if amount > 5:
				await ctx.send("\n".join(urls[:5]))
				await ctx.send("\n".join(urls[5:amount]))
		except :
			return await ctx.send("Please try a valid tag.")		


	@commands.command()
	@commands.guild_only()
	@commands.cooldown(1, 5, commands.BucketType.user)
	@commands.check(togglecheck)
	async def yandere(self, ctx, tags:str, amount :int = 1):
		if amount >10:
			return await ctx.send("10 is the limit")
		urls = imgdl.yandere(url=tags)
		await self.send_image(ctx=ctx, urls=urls, amount=amount)

		
	@commands.command()
	@commands.guild_only()
	@commands.cooldown(1, 5, commands.BucketType.user)
	@commands.check(togglecheck)
	async def konachan(self, ctx, tags:str, amount :int = 1):
		if amount >10:
			return await ctx.send("10 is the limit")
		urls = imgdl.konachan(url=tags)
		await self.send_image(ctx=ctx, urls=urls, amount=amount)

	@commands.command()
	@commands.guild_only()
	@commands.cooldown(1, 5, commands.BucketType.user)
	@commands.check(togglecheck)
	async def rule34(self, ctx, tags:str, amount: int = 1):
		if amount >10:
			return await ctx.send("10 is the limit")
		rule34_ = rule34.Rule34()
		urls = []
		request = await rule34_.getImages(tags = tags, randomPID=True, fuzzy=True)
		for x in request:
			urls.append((x.sample_url))
		await self.send_image(ctx=ctx, urls=urls, amount=amount)	


	@commands.command()
	@commands.guild_only()
	@commands.cooldown(1, 5, commands.BucketType.user)
	@commands.check(togglecheck)
	async def realbooru(self, ctx, tags:str, amount:int=1):
		if amount >10:
			return await ctx.send("10 is the limit")
		api_url = BooruRealbooru().get_api_url(tags)
		booru_json = await self.aiojson(api_url)
		if not booru_json:
			return await ctx.send("No result!")
		urls = []
		i = 0
		for x in booru_json:
			chosen_post = (booru_json[i])
			image_url = BooruRealbooru.get_image_url(self, chosen_post)
			urls.append(image_url)
			i += 1
		await self.send_image(ctx=ctx, urls=urls, amount=amount)

	@commands.command()
	@commands.guild_only()
	@commands.cooldown(1, 5, commands.BucketType.user)
	@commands.check(togglecheck)
	async def danbooru(self, ctx, tags:str, amount:int=1):
		if amount >10:
			return await ctx.send("10 is the limit")
		urls = imgdl.danbooru(tags = tags)
		await self.send_image(ctx=ctx, urls=urls, amount=amount)

	@commands.command()
	@commands.guild_only()
	@commands.cooldown(1, 5, commands.BucketType.user)
	@commands.check(togglecheck)
	async def gelbooru(self, ctx, tags:str, amount:int=1):
			tags =  tags.replace(";", "_")
			list_tag = list(tags.split("+"))
			# list_tag.append("-rating:safe")
			page = random.randint(1, 100)

			gelbooru = Gelbooru(f'&api_key={self.Bot.gelbooru_token}', '736918')
			results = await gelbooru.search_posts(tags=list_tag, exclude_tags=['loli', 'shota', 'lolicon'], page = page)
			n = 0
			urls = []
			for result in results:
				url = str(results[n])
				if url.endswith("mp4"):
					continue
				if url.endswith("webm"):
					continue
				urls.append(url)
				n= n+1
			await self.send_image(ctx=ctx, urls=urls, amount=amount)
			
	@commands.command()
	@commands.guild_only()
	@commands.cooldown(1, 5, commands.BucketType.user)
	@commands.check(togglecheck)
	async def safebooru(self, ctx, tags:str, amount:int=1):
		urls = imgdl.safebooru(tags = tags)
		await self.send_image(ctx=ctx, urls=urls, amount=amount)


	async def aiojson(self, url):
		async with aiohttp.ClientSession() as cs:
			async with cs.get(url) as data:
				if data.status == 200:
					ctype = data.headers['Content-Type']
					text_data = await data.text()

					# print(text_data)
					x = await data.json(content_type=None)
					data.close()
					return x
			data.close()

class BooruRealbooru:
    """Booru class for Realbooru"""
    name = "Realbooru"
    domain = "realbooru.com"
    random_supported = False

    def get_api_url(self, tags: str):
        return f"https://realbooru.com/index.php?page=dapi&s=post&q=index&limit=100&json=1"\
               f"&tags=score:>=10 -webm {tags}"

    def get_post_url(self, post_id):
        return f"https://realbooru.com/index.php?page=post&s=view&id={post_id}"

    def get_post_hash(self, post_json):
        return post_json["hash"]

    def get_post_timestr(self, post_json):
        return datetime.datetime.utcfromtimestamp(post_json["change"])

    def get_image_url(self, post_json):
        return f"https://realbooru.com/images/"\
               f"{post_json['directory']}/{post_json['image']}"

    def get_owner_name(self, post_json):
        return post_json['owner']

    def get_post_tags(self, post_json):
        return post_json['tags']

    def get_post_score(self, post_json):
        return post_json['score']



def setup (Bot):
	Bot.add_cog(booru(Bot))
	print("Booru cog is working.")