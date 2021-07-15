import discord
from discord.ext import commands, tasks
import pymongo
from pymongo import MongoClient
import random
import requests


class DanimeAPI:
	def __init__(self, api_url):
		self.api_url = api_url


	def get_image(self, tag):
		return requests.get(f"{self.api_url}{tag}").json()['url']

	def get_many_images(self, tag, amount):
		return requests.get(f"{self.api_url}{tag}/{amount}").json()['urls']

	def get_hentai(self, id):
		return requests.get(f"{self.api_url}{doujin}/{id}").json()['url']

	def tag_dict(self, tag:str):
		dict = {
			"sfwneko" : "sneko",
			"sfwoppai" : "soppai",
			"sfwswimsuit" : "sswimsuit",
			"hairy" : "bush"
		}
		return dict[tag]

	def available_paths(self, mongo_url):
		availablePaths = mongo_url['AbodeDB']['1avialablepaths'].find_one({"_id" : 1})['available_paths']
		return availablePaths

	async def is_nsfw(self, ctx):
		embed = discord.Embed()
		embed.title= f"Non-NSFW channel detected!"
		embed.add_field(name="Why should you care?", value=f"Discord forbids the use of NSFW content outside the NSFW-option enabled channels. [More here](https://discord.com/guidelines#:~:text=You%20must%20apply%20the%20NSFW,sexualize%20minors%20in%20any%20way.)", inline=False)
		embed.add_field(name="How can I enable the NSFW channel option?", value=f"** **", inline=False)
		embed.set_image(url=f"https://cdn.discordapp.com/attachments/802518639274229800/802936914054610954/nsfw.gif")
		embed.set_footer(text=f"Pro tip: dh set_nsfw can do the work for you.")
		return await ctx.send(embed=embed) 


class auto(commands.Cog, name="auto"):
	def __init__(self, Bot):
		self.Bot = Bot
		self.auto_send.start()
		self.danime_api = DanimeAPI(self.Bot.api_url)

	@tasks.loop(seconds=60)
	async def auto_send(self):
		await self.Bot.wait_until_ready()
		try:
			# if self.Bot.DEFAULT_PREFIX == "&":
			# 	return 
			self.Bot.counter += 1
			db = self.Bot.db1['AbodeDB']
			collection= db['autonsfw']
			available_paths = self.danime_api.available_paths(self.Bot.db2)
			for path in available_paths:
				color = random.choice(self.Bot.color_list)
				specificSearch = collection.find({"tag" : path})
				if specificSearch.count() == 0:
					continue
				specificLength =  specificSearch.count()
				image_list = self.danime_api.get_many_images(path, specificLength)
				for key, item in enumerate(specificSearch):
					webhook_url =item["_id"]
					setTime = item["time"]
					setTag = item["tag"]
					image = image_list[key]
					embed =  discord.Embed(color =  color)
					embed.set_image(url=f"{image}")
					embed.description = f"Images powered by [Danime Bot]({self.Bot.invite})"
					if self.Bot.counter % setTime == 0:
						try:
							self.Bot.loop.create_task(self.sendwebhook(collection = collection, webhook_url = webhook_url, embed = embed))
						except:
							continue
		except ValueError:	
			self.Bot.counter += 1
			print("Couldn't send it")
			pass
		except:
			self.Bot.counter += 1
			pass

			
	async def sendwebhook(self, collection, webhook_url, embed:discord.Embed):
		try:
			bot_avatar = "https://cdn.discordapp.com/attachments/790246681563889694/804058149504942080/Vien.png"
			hook = discord.Webhook.from_url(webhook_url,adapter=discord.RequestsWebhookAdapter())
			hook.send(embed=embed, avatar_url= bot_avatar)
		except discord.NotFound:
			collection.delete_one({"_id" : webhook_url})
			print("Deleted")
		except discord.HTTPException:
			await self.removeimage(setTag, image)
			print(f"Removed , {setTag} tag, url : {image}")

	async def removeimage(self, tag, url ):
		db = self.Bot.db2['AbodeDB']
		collection = db[tag]
		try:
			collection.delete_one({"_id" : url})
		except:
			pass

def setup (Bot):
	Bot.add_cog(auto(Bot))
	print("Auto nsfw is working.")