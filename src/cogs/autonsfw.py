import discord
from discord.ext import commands
import pymongo
from pymongo import MongoClient
import requests
from core import danime
from dislash import *


class DanimeAPI:
	def __init__(self, Bot):
		self.Bot = Bot

	def get_image(self, tag):
		return requests.get(f"{self.Bot.api_url}{tag}").json()['url']

	def get_many_images(self, tag, amount):
		return requests.get(f"{self.Bot.api_url}{tag}/{amount}").json()['urls']

	def get_hentai(self, id):
		return requests.get(f"{self.Bot.api_url}doujin/{id}").json()['url']

	def tag_dict(self, tag:str):
		dict = {
			"sfwneko" : "sneko",
			"sfwoppai" : "soppai",
			"sfwswimsuit" : "sswimsuit",
			"hairy" : "bush",
			"erofeet" :"feet"
		}
		return dict[tag]

	def available_paths(self, mongo_url):
		return mongo_url['AbodeDB']['1avialablepaths'].find_one({"_id" : 1})['available_paths'] 

	async def not_nsfw(self, ctx):
		embed = discord.Embed()
		embed.title= f"Non-NSFW channel detected!"
		embed.add_field(name="Why should you care?", value=f"Discord forbids the use of NSFW content outside the NSFW-option enabled channels. [More here](https://discord.com/guidelines#:~:text=You%20must%20apply%20the%20NSFW,sexualize%20minors%20in%20any%20way.)", inline=False)
		embed.add_field(name="How can I enable the NSFW channel option?", value=f"** **", inline=False)
		embed.set_image(url=f"https://cdn.discordapp.com/attachments/802518639274229800/802936914054610954/nsfw.gif")
		embed.set_footer(text=f"Pro tip: dh set_nsfw can do the work for you.")
		return await ctx.send(embed=embed) 

	async def send_images(self, ctx, tag: str, amount: int):
	    if amount > 10:
	        return await ctx.send("Can't go higher than 10.")
	    urls = self.get_many_images(tag, amount)
	    a = 0 
	    b = 5
	    while len(urls) >= a:
	        try:
	            await ctx.send(content =f"\n".join(urls[a:b]), components = [ActionRow(Button(style=ButtonStyle.link, label="Danime", url=f"{self.Bot.website_link}"))])
	        except discord.HTTPException:
	            break
	        a += 5
	        b += 5


	async def image_embed(self, ctx, tag):
	    link = self.get_image(tag)
	    embed = discord.Embed(color=0x7fcbff)
	    embed.description = f"[Image]({link}) Powered by **[Danime]({self.Bot.invite})** ||Tag : {tag}||"
	    embed.set_image(url=link)
	    return await ctx.send(embed=embed, components = [ActionRow(Button (style=ButtonStyle.primary, label="NUTT", custom_id="NUTT_BUTTON"),Button(style=ButtonStyle.link, label="Sauce", url=f"https://saucenao.com/search.php?url={link}"))])
	    
	async def normal_image_embed(self, ctx, link, dl=None):
		embed = discord.Embed(color =0x7fcbff)
		embed.description = f"Bad image? [Report it]({self.Bot.support})"
		if dl:
			embed.description=f"[Link]({dl})"
		embed.set_image(url=f"{link}")
		await ctx.send(embed=embed)


class auto(commands.Cog, name="auto"):
	def __init__(self, Bot: danime.Danime):
		self.Bot = Bot
		self.danime_api = DanimeAPI(Bot)
	

	@commands.group(pass_context=True)
	@commands.has_permissions(manage_webhooks=True)
	@commands.bot_has_permissions(manage_webhooks=True)
	async def autonsfw(self,ctx):
		if ctx.invoked_subcommand is None:
			helper = str(ctx.invoked_subcommand) if ctx.invoked_subcommand else str(ctx.command)
			await ctx.send(f"{ctx.author.name} The correct way of using that command is : ")
			await ctx.send_help(helper)


	@autonsfw.command(pass_context=True, usage = "dh autonsfw enable yuri 5",
		description = "Cool feature that allows you to receive hentai automatically.")
	@commands.has_permissions(manage_webhooks=True)
	@commands.bot_has_permissions(manage_webhooks=True)
	async def enable(self, ctx, tag:str="nsfw", time:int=1):
		if not ctx.channel.is_nsfw():
			return await self.danime_api.not_nsfw(ctx)	
		try:

			if  time > 60:
				return await ctx.send("Sorry mate but 60 is the limit for the free version. Please refer to `dh premium` for longer times.")
			if time < 5:
				if ctx.guild.id in self.Bot.premium_guilds:
					pass
				else:
					return await ctx.send("Hey you have to atleast have 5 minutes of post time.")

			##It's checking the tag if it exists or not, if not backs away
			try:
				tag = self.danime_api.tag_dict(tag)
			except:
				tag = tag

			if tag == "videos":
				return await ctx.send("Sorry you can't have videos on auto.")
				
			if tag not in self.danime_api.available_paths(self.Bot.db2):
				return await ctx.send("Please provide a valid tag, you can see the tags from the help command.")
			
			channel = ctx.channel
			webhook = await channel.create_webhook(name="Danime | Autonsfw")
			webhook_url = webhook.url
			db =  self.Bot.db1['AbodeDB']
			collection= db['autonsfw']

			
			active = collection.find({"guild_id" : ctx.guild.id}).count()
			if active >= 10:
				if ctx.guild.id in self.Bot.premium_guilds:
					if active >= 30:
						return await ctx.send("Hey mate even though you have premium, we are limited to only server 30 active channels at the moment.")
					pass
				else:
					return await ctx.send("A server can't have more than 10 active autonsfw plugins. Please remove an active plugin or get the premium version from dh premium.")

			if (collection.find_one({"channel_id": channel.id})== None):
				if isinstance(time, int):
					data =  {
					"_id": webhook_url,
					"guild_id" : channel.guild.id,
					"channel_id" : channel.id,
					"tag" : tag,
					"time" : time
					}
				collection.insert_one(data)
				await ctx.send(f'The channel has been set to accept the AutoNSFW feature with tag `{tag}` and procces time `{time}` minute.')	
			else:
				await webhook.delete()
				await ctx.send("This channel alreay has the auto nsfw feature enabled. If you just removed the webhook then this won't work, join the support server and ask the staff to manually remove it.")
		
		except discord.Forbidden:
			await ctx.send("I may not have enough permissions to complete the follow operation, make sure I have manage_webhooks and manage_channel permissions available.")
		
		except discord.HTTPException:
			await ctx.send("It seems there are already 10 webhooks in this channel, please delete them by going to `edit channel > integrations > webhooks` and deleting the one which isn't used.")

		except Exception:
			await ctx.send("Hey, it seems you called the command incorrectly, use this command like : `dh autonsfw enable stockings 5`")
	

	@autonsfw.command(usage = "dh autonsfw disable", description="Disables autonsfw for the channel the command was used on.")
	@commands.has_permissions(manage_webhooks=True)    
	@commands.bot_has_permissions(send_messages=True)
	async def disable(self,ctx):
			db =  self.Bot.db1['AbodeDB']
			collection= db['autonsfw']
			search = collection.find({"channel_id" : ctx.channel.id})
			
			if search is None:
				return await ctx.send("No active autonsfw plugin found in this channel.")

			else:
				collection.delete_one({"channel_id": ctx.channel.id})
				return await ctx.send("Successfully removed the feature.")

def setup (Bot: danime.Danime) -> None:
	Bot.add_cog(auto(Bot))
	Bot.logger.info("Auto nsfw is working.")