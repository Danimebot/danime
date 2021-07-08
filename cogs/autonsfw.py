import discord
from discord.ext import commands, tasks
import pymongo
from pymongo import MongoClient
import random
import requests


class auto(commands.Cog, name="auto"):



	def __init__(self, Bot):
		self.Bot = Bot
		self.autosend.start()
		

	@commands.group(pass_context=True)
	@commands.has_permissions(manage_webhooks=True)
	@commands.bot_has_permissions(manage_webhooks=True)
	async def autonsfw(self,ctx):
		if ctx.invoked_subcommand is None:
			helper = str(ctx.invoked_subcommand) if ctx.invoked_subcommand else str(ctx.command)
			await ctx.send(f"{ctx.author.name} The correct way of using that command is : ")
			await ctx.send_help(helper)


	@autonsfw.command(pass_context=True)
	@commands.has_permissions(manage_webhooks=True)
	@commands.bot_has_permissions(manage_webhooks=True)
	async def enable(self,ctx,tag=None, time=None):
		if not ctx.channel.is_nsfw():
			embed = discord.Embed(color = random.choice(self.Bot.color_list))
			embed.title= f"Non-NSFW channel detected!"
			embed.add_field(name="Why should you care?", value=f"Discord forbids the use of NSFW content outside the NSFW-option enabled channels. [More here](https://discord.com/guidelines#:~:text=You%20must%20apply%20the%20NSFW,sexualize%20minors%20in%20any%20way.)", inline=False)
			embed.add_field(name="How can I enable the NSFW channel option?", value=f"** **", inline=False)
			embed.set_image(url=f"https://cdn.discordapp.com/attachments/802518639274229800/802936914054610954/nsfw.gif")
			embed.set_footer(text=f"Pro tip: {self.Bot.DEFAULT_PREFIX}set_nsfw can do the work for you.")
			return await ctx.send(embed=embed) 		
		try:
		
			
			##Checks the time and backs off it's over than 30
			if time != None:
				time = int(f"{time}")
				if time > 30:
					return await ctx.send("Sorry mate but 30 is the limit.")


			##It's checking the tag if it exists or not, if not backs away
			if tag != None:
				try:
					tag = self.tagdict(tag)
				except :
					tag = tag
				
				try:
					checkUrl = f"{self.Bot.api_url}{tag}"
					r = requests.get(f"{checkUrl}").json()['url']
				except TypeError:
					return await ctx.send("Please provide a valid tag, you can see the tags from the help command.")
			
			channel = ctx.message.channel

			webhook = await channel.create_webhook(name="Danime | Autonsfw")
			webhook_url = webhook.url
			db =  self.Bot.db2['AbodeDB']
			collection= db['auto_channels']
			if time == None or time < 1:
				time == "None"
			elif tag == None:
				tag = "None"

			if (collection.find_one({"channel_id": channel.id})== None):
				if isinstance(time, int):
					data = {"_id": webhook_url, "channel_id": channel.id, "tag": f"{tag}"
					, "time": time
					}
				else:
					data = {"_id": webhook_url, "channel_id": channel.id, "tag": f"{tag}"
					, "time": "None"
					}
				collection.insert_one(data)

				await ctx.send(f'The channel has been set to accept the feature with tag {tag} and procces time {time} minute. Make sure I have the permissions to mangage webhooks!!')
			
			else:
				await webhook.delete()
				await ctx.send("This channel alreay has the auto nsfw feature enabled. If you just removed the webhook then this won't work, join the support server and ask the staff to manually remove it.")
		except:
			await ctx.send("I may not have enough permissions to complete the follow operation, make sure I have manage_webhooks and manage_channel permissions available. Also be sure the tags are available on the bot.")

	def tagdict(self, tag:str):
		dict = {
			"sfwneko" : "sneko",
			"sfwoppai" : "soppai",
			"sfwswimsuit" : "sswimsuit", 
		}
		return dict[f"{tag}"]
	@autonsfw.command()
	@commands.has_permissions(manage_webhooks=True)    
	@commands.bot_has_permissions(send_messages=True)
	async def disable(self,ctx):
			db =  self.Bot.db2['AbodeDB']
			collection= db['auto_channels']
			if (collection.find_one({"channel_id": ctx.channel.id})== None):
				await ctx.send("This channel doesn't have the auto nsfw feature.")
			else:
				collection.delete_one({"channel_id": ctx.channel.id})
				await ctx.send("Successfully removed the feature.")

	async def danimeapi(self, tag):
		data = requests.get(f"{self.Bot.api_url}{tag}").json()
		image = data['url']
		return image



	@tasks.loop(seconds=15)
	async def autosend(self):
		try:
			if self.Bot.DEFAULT_PREFIX == "&":
				return 
			self.Bot.counter += .25
			if int(self.Bot.counter) != self.Bot.counter:
				return
			db = self.Bot.db2['AbodeDB']
			collection= db['auto_channels']
			bot_avatar = "https://cdn.discordapp.com/attachments/790246681563889694/804058149504942080/Vien.png"
			search = collection.find().sort("time", 1)
			

			for ans in search:
					webhook_url =ans["_id"]
					setTime = ans["time"]
					setTag = ans["tag"]
					
					if setTime == "None" and setTag =="None":
						try:
							image =  await self.danimeapi(tag = "nsfw")
							hook = discord.Webhook.from_url(webhook_url,adapter=discord.RequestsWebhookAdapter())
							
							embed =  discord.Embed(color =  random.choice(self.Bot.color_list))
							embed.set_image(url=f"{image}")
							embed.description = f"Images powered by [Danime]({self.Bot.invite})"
							hook.send(embed=embed,
								avatar_url= f"{bot_avatar}"
								)
							continue
						except discord.NotFound:
							collection.delete_one({"_id" : webhook_url})
							print("Deleted")
						except discord.HTTPException:
							print(image)
							continue
						except:
							continue


						
						
					if setTime == "None":
						if setTag != "None":
							try:
								image = await self.danimeapi(tag = setTag)
								hook = discord.Webhook.from_url(webhook_url,adapter=discord.RequestsWebhookAdapter())
								embed =  discord.Embed(color =  random.choice(self.Bot.color_list))
								embed.set_image(url=f"{image}")
								embed.description = f"Images powered by [Danime]({self.Bot.invite})"
								hook.send(embed=embed, avatar_url= f"{bot_avatar}")
								continue
							except discord.NotFound:
								collection.delete_one({"_id" : webhook_url})
								print("Deleted")
							except discord.HTTPException:
								url = f"{setTag} tag, url : {image} "
								print(url)
								continue
							except:
								continue

					if setTime != "None" and setTag !=  "None":
						if  (self.Bot.counter % setTime) == 0:
							try:
							
								image = await self.danimeapi(tag = setTag)
								hook = discord.Webhook.from_url(webhook_url,adapter=discord.RequestsWebhookAdapter())
								embed =  discord.Embed(color =  random.choice(self.Bot.color_list))
								embed.set_image(url=f"{image}")
								embed.description = f"Images powered by [Danime]({self.Bot.invite})"
								hook.send(embed=embed, avatar_url= f"{bot_avatar}")
								continue
							except discord.NotFound:
								collection.delete_one({"_id" : webhook_url})
								print("Deleted")
							except discord.HTTPException:
								url = f"{setTag} tag, url : {image} "
								print(url)
							except:
								continue
			
				
			

		except ValueError:
			self.Bot.counter += .25
			print("Couldn't send it")
			pass


def setup (Bot):
	Bot.add_cog(auto(Bot))
	print("Auto nsfw is working.")