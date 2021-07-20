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

		urls = list(url.split("+"))
		db = self.Bot.db2['AbodeDB']
		collection = db [f'{collection}']
		check = db.list_collection_names()

		if not collection.name in check:
			return await ctx.send("No result for the db query.")
		for url in urls:
			if (collection.find_one({"_id": url})== None):
				data = {"_id": url}
				collection.insert_one(data)
				await ctx.send("Added a new image.")
			else:
				await ctx.send("It seems the image is already added.")

	@commands.group(pass_context=True)
	@commands.check(is_dev)
	@commands.guild_only()
	async def removeimage(self, ctx, collection:str, url:str):
		if ctx.invoked_subcommand is None:
			if url == None:
				return await ctx.send(f"Bruh!")

			urls = list(url.split("+"))
			db = self.Bot.db2['AbodeDB']
			collection = db [f'{collection}']

			check = db.list_collection_names()
			if not collection.name in check:
				return await ctx.send("No result for the db query.")
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
	async def deleteimage(self, ctx, url:str):
		await ctx.send("This command will delete the image from all the database if matched, please use this wisley.", delete_after=7)
		db = self.Bot.db2['AbodeDB']
		collections = db.list_collection_names()
		for collection in collections:
			activeCollection = db[f'{collection}']
			query = {"_id" : url}
			search = activeCollection.find_one(query)
			if search != None:
				activeCollection.delete_one({"_id" : url})
				await ctx.send(f"DELETED IMAGE from {activeCollection.name}.")
			else:
				continue


	@commands.command()
	@commands.check(is_dev)
	@commands.guild_only()
	async def moveimage(self, ctx, collection:str, url:str, collection2:str):
		if url == None:
			return await ctx.send(f"Bruh!")

		urls = list(url.split("+"))
		db = self.Bot.db2['AbodeDB']
		check = db.list_collection_names()
		collection = db [f'{collection}']
		collection2 = db[collection2]

		if not collection.name in check or not collection2.name in check:
			return await ctx.send("Check failed, wrong db given.")

		try:
			query = {"_id": url}
			search = collection.find_one(query)
			search2 = collection2.find_one(query)
			if search != None:
				collection.delete_one(query)
			if search2 != None:
				return await ctx.send("Image already exists at the moved folder.")
			
			collection2.insert_one({"_id" : url})
			await ctx.send(f"Image moved from `{collection.name}` to `{collection2.name}`")
			
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
			else:y55555
				continue
		matches = ['No matches'] if len(matches)== 0 else matches
		r = requests.get(link).content
		try:
			status = 200
		except:
			status = r.status_code
		# try:
		embed = discord.Embed()
		embed.description = f"Link status  || [Link]({link})"
		embed.add_field(name = "Collections", value = f", ".join(matches))
		embed.add_field(name = "Status Code", value= status)
		embed.add_field(name = "Remove it?", value= f"`dh removeimage <collection> {link}`", inline=False)
		await ctx.send(embed=embed)
		# except:
		# 	return await ctx.send("Something went wrong.")
	
	@commands.command()
	@commands.guild_only()
	@commands.check(is_dev)
	async def sendallimages(self, ctx, id:int):
		channel = self.Bot.get_channel(id)
		z = await ctx.send("Working on it!!")
		db = self.Bot.db2['AbodeDB']

		collection= db[f'anal']
		collection2 = db[f'anal2']
		search1 = collection.find()
		search2 = collection2.find()
		search2url = []
		for value in search2:
			search2url.append(value['_id'])

		for value in search1:
			url = value["_id"]
			if not url in search2url:
				await channel.send(url)




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
			# try:
			# 	# if message.content.startswith("&upload_images") or message.content.startswith("+jsk debug upload_images"):
			# 	# 	await ctx.send(f"Scraped images till [Here]({message.jump_url})")
			# 	# 	break
				url = message.content
				
				if message.attachments != None:
					for attachments in message.attachments:
						content = attachments.url
						if content.startswith("https"):
							check = self.is_url()
							if check == True:
								secondList.append(content)

				if url.endswith("mp4") or url.endswith("gif"):
					continue
				if not url.startswith("https"):
					continue
				if url in firstList:
					continue
				secondList.append(url)
			# except:
			# 	pass
		
		for x in secondList:
			if x.startswith("https") and x not in firstList:
				await ctx.send(x)
				data = {"_id": x}
				try:
					collection.insert_one(data)
				except:
					print(f"Couldn't send {x}")

		message = f"Process completed, with addition of `{len(secondList)}` images to the tag `{collection.name}`, now the tag has total of `{len(firstList) + len(secondList)}` images."
		await ctx.send(embed=discord.Embed(description = message))

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

	def is_url(self, message):
		pattern =  re.compile(r"^https?://\S+(\.jpg|\.png|\.jpeg|\.webp]|\.gif)$")
		if not pattern.match(message):
			return False
		return True

	@commands.command()
	@commands.check(is_dev)
	async def updateapiinfo(self, ctx):
		db = self.Bot.db2['AbodeDB']
		collections = db.list_collection_names()
		collections.sort()
		results = []
		n = 1
		total = 0
		for collection in collections:
			activeCollection = db[f'{collection}']
			total += activeCollection.count()
			if activeCollection.count() > 60:
				string = f"`{n}.` {activeCollection.name.capitalize()} : `{activeCollection.count()}`"
				results.append(string)
				n+=1
		embed = discord.Embed(timestamp=datetime.datetime.now())
		embed.title = "Information on the DanimeAPI database collections."
		embed.description = "\n".join(results)
		embed.set_thumbnail(url = ctx.me.avatar_url)
		embed.set_footer(text=f"Total images : {total} | Last updated ", )
		await ctx.send(embed=embed) 



def setup (Bot):
	Bot.add_cog(danimeapi(Bot))
	print("DanimeAPI is working.")
