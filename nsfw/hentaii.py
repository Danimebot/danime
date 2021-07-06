import discord
from discord.ext import commands, tasks
import hentai
from hentai import Format, Hentai, Tag, Utils
import random
import asyncio
import requests
from disputils import BotEmbedPaginator
from cogs.utils import Pag
from discord.ext import menus
from nsfw import imgdl
from misc import emoji
from pygelbooru import Gelbooru
from ago import human
import os
import urllib.request
from random import randint
import shutil
import json


class CatchAllMenu(menus.MenuPages, inherit_buttons=False):
    def __init__(self, source, **kwargs):
        super().__init__(source, **kwargs)
        self._info_page = f"Info:\n⬅️ • Go back one page\n➡️ • Go forward one page\n⏪ • Go the the first page\n⏩ • Go to the last page\n⏹️ • Stop the paginator\n🔢 • Go to a page of your choosing\n❔ • Brings you here"
    
    @menus.button('⏪', position=menus.First(0))
    async def go_to_first_page(self, payload):
        """go to the first page"""
        await self.message.remove_reaction(payload.emoji, payload.member)
        await self.show_page(0)
    
    @menus.button('⬅️', position=menus.Position(0))
    async def go_to_previous_page(self, payload):
        """go to the previous page"""
        await self.show_checked_page(self.current_page - 1)
        await self.message.remove_reaction(payload.emoji, payload.member)
    
    @menus.button('⏹️', position=menus.Position(3))
    async def stop_pages(self, payload):
        """stops the pagination session."""
        self.stop()
        await self.message.delete()
    
    @menus.button('➡️', position=menus.Position(5))
    async def go_to_next_page(self, payload):
        """go to the next page"""
        await self.message.remove_reaction(payload.emoji, payload.member)
  
        await self.show_checked_page(self.current_page + 1)
    
    @menus.button('⏩', position=menus.Position(6))
    async def go_to_last_page(self, payload):
        await self.message.remove_reaction(payload.emoji, payload.member)
     
        await self.show_page(self._source.get_max_pages() - 1)
    
    @menus.button('🔢', position=menus.Position(4))
    async def _1234(self, payload):
        await self.message.remove_reaction(payload.emoji, payload.member)
        i = await self.ctx.send("What page would you like to go to?")
        msg = await self.ctx.bot.wait_for('message', check=lambda m: m.author == self.ctx.author)
        page = 0
        try:
            page += int(msg.content)
        except ValueError:
            return await self.ctx.send(
                f"**{self.ctx.author.name}**, **{msg.content}** could not be turned into an integer! Please try again!",
                delete_after=3)
        
        if page > (self._source.get_max_pages()):
            await self.ctx.send(f"There are only **{self._source.get_max_pages()}** pages!", delete_after=3)
        elif page < 1:
            await self.ctx.send(f"There is no **{page}th** page!", delete_after=3)
        else:
            index = page - 1
            await self.show_checked_page(index)
            await i.edit(content=f"Transported to page **{page}**!", delete_after=3)
    
    @menus.button('❔', position=menus.Position(7))
    async def on_info(self, payload):
        
        await self.message.remove_reaction(payload.emoji, payload.member)
       
        await self.message.edit(embed=discord.Embed(description=self.info_page, color =0xb863f2))
    
    @property
    def info_page(self):
        return self._info_page
    
    def add_info_fields(self, fields: dict):
        for key, value in fields.items():
            self._info_page += f"\n{key} • {value}"


class EmbedSource(menus.ListPageSource):
    def __init__(self, data):
        super().__init__(data, per_page=1)
    
    async def format_page(self, menu, entries: discord.Embed):
        entries.set_footer(text=f'({menu.current_page + 1}/{menu._source.get_max_pages()})')
        return entries

class hentaii(commands.Cog, name="hentaii"):
	def __init__(self, Bot):
		self.Bot = Bot
		self.page = 1
		
		self.nsfwToggledGuildsGet.start()

	@commands.command(aliases=['id','doujin'], description=f"Lets you read hentai through the use of N-hentai API, you will need to use the hentai code as the search attribute.")
	@commands.guild_only()
	@commands.cooldown(1, 5, commands.BucketType.guild)
	@commands.bot_has_permissions(manage_messages = True)
	async def search(self, ctx, id: int):
		
		if ctx.channel.is_nsfw():
			send = await ctx.send(f"<:nh3ntai:802131455215796224> Searching for ``{id}`` ")
			
			
			if not Hentai.exists(id):
				await ctx.send("404 not found")
			else:
			
				doujin = Hentai(id)
				
				
				language = Tag.get(doujin.language, property_="name")

				emoji = "🌐"
				if language == "english":
					emoji = "<:English_language:802096460170395658>"
				if language == "japanese":
					emoji = "<:Japanese:802096455962984468>"
				if language == "chinese":
					emoji = "<:FlagChina:802097002364010527>"
				type_= Tag.get(doujin.category, property_="name")
				close = []
				for related in doujin.related:
					hmm = str(related.id)
					close.append(related.title(Format.Pretty))
				uploded = doujin.upload_date

				uploadedBetter = human(uploded, 4)
				Author = Tag.get(doujin.artist, property_='name')
				if Author == None:
					Author = "Not given"
				embed = discord.Embed(title=doujin.title(Format.Pretty),
				 url=doujin.url, color=random.choice(self.Bot.color_list))
				
				embed.add_field(name="Language", value=f"{emoji} ")
				
				embed.add_field(name="Author", value=f" `{Author}`")

				embed.add_field(name="Type", value = type_)
				if doujin.num_favorites == 0:
					embed.add_field(name="Favorites", value=f"For some reason this is broken :(")
				else:
					embed.add_field(name="Favorites", value=f"❤ {(doujin.num_favorites)}")
				embed.add_field(name="Pages", value=f"📕 {doujin.num_pages}")
				embed.add_field(name="Upload Date", value=f" {uploadedBetter}")
				embed.set_thumbnail(url=doujin.thumbnail)
				thing= doujin.tag
				tags = []
				for tag in thing:
					z = Tag.get(thing, property_="name")
					
				matches = ["lolicon", "shotacon", "gore", "rape", "cannibalism", "eye penetration", 
						"forbidden content", "scat",
				]
				if any(x in z for x in matches):
					if not ctx.guild.id in self.nsfwToggledGuilds: 
						embed = discord.Embed(description ="The content you searched up has images that are not allowed by default.\n Use `dh nsfwtoggle enable` to enable it. \n**USING THIS FEATURE IS NOT RECOMMENDED USE AT YOUR OWN RISK!!!**")
						return await ctx.send(embed= embed)
					else:
						pass
				embed.add_field(name="Tags",value=f"{z}", inline=False)
				if close != None:
					embed.add_field(name="Related",value=f" \n".join(close))
				embed.add_field(name=f"Reactions", 
					value=f"React with <:nh3ntai:802131455215796224> if you want to read this. \nReact with <:horny:810392503547199509> to get all the images. \nReact with 📤 if you want to open a reading room.\n"
							"React with 📥 to download this doujin." , inline=False)
				await send.delete()
				x = await ctx.send(embed=embed)

				await x.add_reaction("<:nh3ntai:802131455215796224>")
				await x.add_reaction("<:horny:810392503547199509>")
				await x.add_reaction("📤")
				await x.add_reaction("📥")
				def check(reaction,user):
					
					return user == ctx.author and user.id != ctx.me.id
				try:
					reaction, user= await self.Bot.wait_for("reaction_add",timeout=60, check=check)
					await x.remove_reaction( emoji = f"<:nh3ntai:802131455215796224>" , member = ctx.author)
					if str(reaction.emoji) == f'<:nh3ntai:802131455215796224>':
						await x.delete()
						a =0 
						if a == 0:
							list_ = doujin.image_urls
							embeds= []
							for i in list_:
							    e = discord.Embed(color = random.choice(self.Bot.color_list))
							    e.description = f"[Direct link]({doujin.url})"
							    e.set_image(url=i)
							    embeds.append(e)
							source = EmbedSource(embeds)
							menu = CatchAllMenu(source=source)
							await menu.start(ctx)
					if str(reaction.emoji) ==f"<:horny:810392503547199509>":
						if len(doujin.image_urls) > 100:
							return await ctx.send("Too many pages to be sent here.")
						
						a = 0 
						b = 5
						while len(doujin.image_urls) >= a:
							try:
								await ctx.send("\n".join(doujin.image_urls[a:b]))
							except Exception:
								break
							a += 5
							b += 5
							
					if str(reaction.emoji) == f"📤":
						
							try:
								channelName = f"Reading room #{ctx.author.discriminator}"
								overwrites = {
									ctx.guild.default_role: discord.PermissionOverwrite(read_messages=False),
									ctx.guild.me: discord.PermissionOverwrite(read_messages=True, manage_channels=True, manage_messages=True),
									ctx.author : discord.PermissionOverwrite(read_messages= True)
									}
								readingChannel = await ctx.guild.create_text_channel(f'{channelName}', overwrites=overwrites,
								 nsfw=True, reason = "Trigger : reading room" , 
								 topic = "Automatically created channel, will be deleted after.",
								 slowmode = 100
								 )
								await readingChannel.send(f"Hello, this is your reading channel, if you want to end it react on  ⏹️  button below on the embed. The reactions will go after 5 minutes of timeout, meaning you have 5 minutes to read one page, thank you!")
								await ctx.send(f"Your reading channel has been set to {readingChannel.mention}, please be there shortly.")
								embeds = []
								for images in doujin.image_urls:
									e = discord.Embed(color = 0x3fb3f1)
									e.description = f"[Direct link]({doujin.url})"
									e.set_image(url = images)
									embeds.append(e)

								paginator = BotEmbedPaginator(ctx, embeds)
								await paginator.run(channel = readingChannel)	
								await readingChannel.delete(reason = "Trigger : end reading session")
							
							except discord.Forbidden:
								await ctx.send("It seems I don't have `manage channels` permissions enabled, enable it to use this feature.")


					if str(reaction.emoji) == F"📥":
						await x.delete()
						await ctx.send(f"You will be given a direct download link, it will be a zip file, you can reassure about the security but it's wise to run a quick scan.")
						db  = self.Bot.db1['AbodeDB']
						collection =   db['direct_links']
						if (collection.find_one({"_id": doujin.id})== None):
							data = requests.get(f"{self.Bot.api_url}doujin/{doujin.id}").json()
							uploded_url = data['url']
							em = discord.Embed()
							em.description = f"Here is your [direct download link]({uploded_url}), enjoy!"
							await ctx.send(embed=em)
							collection.insert_one({"_id": doujin.id, "link": f"{uploded_url}"})
						else:
							search = collection.find({"_id" : doujin.id})
							for result in search:
								uploded_url = result["link"]
							em =  discord.Embed()
							em.description = f"Here is your [direct download link]({uploded_url}), enjoy!"
							await ctx.send(embed=em)

				except asyncio.TimeoutError:
					await ctx.send("Timed out!")
		else:
			embed = discord.Embed(color = random.choice(self.Bot.color_list))
			embed.title= f"Non-NSFW channel detected!"
			embed.add_field(name="Why should you care?", value=f"Discord forbids the use of NSFW content outside the NSFW-option enabled channels. [More here](https://discord.com/guidelines#:~:text=You%20must%20apply%20the%20NSFW,sexualize%20minors%20in%20any%20way.)", inline=False)
			embed.add_field(name="How can I enable the NSFW channel option?", value=f"** **", inline=False)
			embed.set_image(url=f"https://cdn.discordapp.com/attachments/802518639274229800/802936914054610954/nsfw.gif")
			embed.set_footer(text=f"Pro tip: {self.Bot.DEFAULT_PREFIX}set_nsfw can do the work for you.")
			await ctx.send(embed=embed)			  

	def upload(self, filename):
		url = f'https://api.anonfiles.com/upload?token={self.Bot.anon_token}'
		files = {'file': (open(filename, 'rb'))}
	 
		r = requests.post(url, files=files)
		print("[UPLOADING]", filename)
		resp = json.loads(r.text)
		if resp['status']:
			urlshort = resp['data']['file']['url']['short']
			urllong = resp['data']['file']['url']['full']
			return urllong
		else:
			message = resp['error']['message']
			errtype = resp['error']['type']
			print(f'[ERROR] {message}\n{errtype}')



	@commands.command(aliases=['enable_nsfw'],description='Enables the NSFW option from channel settings.')
	@commands.guild_only()
	@commands.has_permissions(manage_channels=True)
	async def set_nsfw(self, ctx):
		await ctx.channel.edit(nsfw = True)
		await ctx.send(f"The channel {ctx.channel.mention} is now a NSFW channel, thanks for the co-operation.")



	@commands.group(pass_context=True)
	@commands.has_permissions(manage_webhooks=True)
	@commands.bot_has_permissions(manage_webhooks=True)
	async def nsfwtoggle(self,ctx):
		if ctx.invoked_subcommand is None:
			helper = str(ctx.invoked_subcommand) if ctx.invoked_subcommand else str(ctx.command)
			await ctx.send(f"{ctx.author.name} The correct way of using that command is : ")
			await ctx.send_help(helper)


	@nsfwtoggle.command(pass_context=True)
	@commands.has_permissions(administrator = True)
	async def enable(self, ctx):
		guild_id = ctx.guild.id
		db = self.Bot.db1['AbodeDB']
		collection  = db['nsfwtoggle']
		if (collection.find_one({"_id": guild_id})== None):
			data = {"_id" : guild_id, "admin" : ctx.author.id }
			collection.insert_one(data)
			return await ctx.send(f"Toggle turned on, takes 1-2 mintues for changes to be applied.")
		return await ctx.send("Already enabled, use `dh nsfwtoggle disable` to disabled it.")

	@nsfwtoggle.command(pass_context=True)
	@commands.has_permissions(administrator = True)
	async def disable(self, ctx):
		db = self.Bot.db1['AbodeDB']
		collection = db['nsfwtoggle']
		try:
			search = collection.find_one({"_id" : ctx.guild.id})
			collection.delete_one({"_id" : ctx.guild.id})
			return await ctx.send("The feature has been disabled.")
		except:
			return await ctx.send("The feature is already disabled.")

	@tasks.loop(seconds=15)
	async def nsfwToggledGuildsGet(self):
		await self.Bot.wait_until_ready()
		db = self.Bot.db1['AbodeDB']
		collection= db['nsfwtoggle']
		search = collection.find()
		self.nsfwToggledGuilds = []
		for guild in search:
			id_ = guild["_id"]
			if not id_ in self.nsfwToggledGuilds:
				self.nsfwToggledGuilds.append(id_)
		
		return

def setup (Bot):
	Bot.add_cog(hentaii(Bot))
	print("Hentai cog is working.")
