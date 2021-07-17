import discord
from discord.ext import commands
import requests
import pymongo
from pymongo import MongoClient
import datetime



class danimeapi(commands.Cog, name="danimeapi"):
	def __init__(self, Bot):
		self.Bot = Bot


	def is_dev(ctx):
		access = [427436602403323905, 353922674684329987,811823086193999892, 814953152640974869, 360087319992074251] 
		if ctx.author.id in access:
			return True
		return False

	@commands.command()
	@commands.check(is_dev)
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
	@commands.check(is_dev)
	@commands.guild_only()
	async def removeimage(self, ctx, collection:str, url:str):
		if url == None:
			return await ctx.send(f"Bruh!")

		urls = list(url.split("+"))
		db = self.Bot.db2['AbodeDB']
		collection = db [f'{collection}']
		for url in urls:
			try:
				query = {"_id": url}
				search = collection.find_one(query)
				if search == None:
					return await ctx.send("Nothing found.")
				collection.delete_one(query)
				await ctx.send(f"Removed.")
			except:
				await ctx.send("This image is not in the databse, try contacting the owner in our support server.")
	
	@commands.command()
	@commands.check(is_dev)
	async def linkstatus(self, ctx, link:str):
		db = self.Bot.db2['AbodeDB']
		collections = db.list_collection_names()
		matches = []
		for collection in collections:
			activeCollection = db[f'{collection}']
			query = {"_id" : link}
			search = activeCollection.find_one(query)
			if search != None:
				collection = collection
				matches.append(collection)
			else:
				continue
		
		r = requests.get(link).content
		try:
			status = 200
		except:
			status = r.status_code
		try:
			embed = discord.Embed()
			embed.description = f"Link status  || [Link]({link})"
			embed.add_field(name = "Collections", value = f", ".join(matches))
			embed.add_field(name = "Status Code", value= status)
			embed.add_field(name = "Remove it?", value= f"`dh removeimage <collection> {link}`", inline=False)
			await ctx.send(embed=embed)
		except:
			return await ctx.send("Something went wrong.")
			

	@commands.command()
	@commands.guild_only()
	@commands.check(is_dev)
	async def getallimages(self, ctx, id_:int,collection:str, amount:int=3000):
		z = await ctx.send("Working on it!!")
		db = self.Bot.db2['AbodeDB']
		check = db.list_collection_names()

		if not collection in check:
			check = " , ".join(check)
			return await ctx.send(f"DB not found for the given query. Available queries {check}. **NOTE EVERYTHING IS CASE SENSETIVE**")
		
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
		xx =  len(secondList) + len(firstList) 
		await z.edit(content=f'It seems it worked! Report\n{x}\n{y}\nTotal {xx}')


	@commands.command()
	@commands.check(is_dev)
	async def apistatus(self, ctx):
		url = " https://discordstatus.com/api/v2/status.json"
		r = requests.get(url).json()
		name = r['page']['name']
		url = r['page']['url']
		time_zone = r['page']['time_zone']
		updated_at = r['page']['updated_at']
		status = r['status']['description']
		em = discord.Embed(timestamp = datetime.datetime.fromisoformat(updated_at))
		em.description = f"Api Status for [{name}]({url})"
		em.add_field(name = "TimeZone", value = time_zone)
		em.add_field(name = "Status", value = status, inline = False)
		em.set_footer(text="Last Updated")
		await ctx.send(embed=em)


def setup (Bot):
	Bot.add_cog(danimeapi(Bot))
	print("DanimeAPI is working.")
