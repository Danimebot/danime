import discord
from discord.ext import commands

import pymongo
from pymongo import MongoClient




class danimeapi(commands.Cog, name="danimeapi"):
	def __init__(self, Bot):
		self.Bot = Bot



	@commands.command()
	@commands.is_owner()
	@commands.guild_only()
	async def addimage(self, ctx, collection:str, url:str):
		if url == None:
			return await ctx.send(f"Bruh!")

		db = self.Bot.db2['AbodeDB']
		collection = db [f'{collection}']


		if (collection.find_one({"_id": url})== None):
			data = {"_id": f"{url}"}

			collection.insert_one(data)
			return await ctx.send("Added a new image.")

	@commands.command()
	@commands.is_owner()
	@commands.guild_only()
	async def removeimage(self, ctx, collection:str, url:str):
		if url == None:
			return await ctx.send(f"Bruh!")

		urls = list(url.split("+"))
		db = self.Bot.db2['AbodeDB']
		collection = db [f'{collection}']
		for url in urls:
			try:
				query = {"_id":url}
				collection.delete_one(query)

				await ctx.send(f"Removed.")
			except:
				await ctx.send("This image is not in the databse, try contacting the owner in our support server.")
	@commands.command()
	@commands.is_owner()
	@commands.guild_only()
	async def getallimages(self, ctx, id_:int,collection:str, amount:int=3000):
		z = await ctx.send("Working on it!!")
		db = self.Bot.db2['AbodeDB']
		collection= db[f'{collection}']
		firstList = []
		secondList = []

		result = collection.find()
		for r in result:
			firstList.append(r['_id'])
		channel = self.Bot.get_channel(id_)
		async for message in channel.history(limit=amount):
			try:
				if message.content.startswith("&upload_images") or message.content.startswith("+jsk debug upload_images"):
					await ctx.send(f"Scraped images till [Here]({message.jump_url})")
					break
				# url = (message.content)

				# if not url.startswith("https"):
				# 	continue
				url = str(message.attachments[0].url)
				if url.endswith("mp4") or url.endswith("gif"):
					continue
				# if message.author.bot == True:
				# 	continue
				secondList.append(url)
			except:
				pass
		
		for x in secondList:
			if not x in firstList:
				data = {"_id": x}
				collection.insert_one(data)
		x = (f'{len(firstList)} in cloud.')
		y = (f'{len(secondList)} in this instance.')
		xx =  len(secondList) - len(firstList) 
		await z.edit(content=f'It seems it worked! Report\n{x}\n{y}\nnew images : {xx}')


def setup (Bot):
	Bot.add_cog(danimeapi(Bot))
	print("DanimeAPI is working.")