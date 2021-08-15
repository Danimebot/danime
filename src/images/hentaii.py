import re
import discord
from discord.ext import commands, tasks
from hentai import Format, Hentai, Tag, Utils, Sort
import random
import asyncio
import requests
from disputils import BotEmbedPaginator
from misc import emoji
from pygelbooru import Gelbooru
from ago import human
from random import randint
from pygicord import Paginator
from reactionmenu import ButtonsMenu, ComponentsButton
from dislash import *
import aiohttp






class hentaii(commands.Cog, name="hentaii"):
	def __init__(self, Bot):
		self.Bot = Bot
		self.page = 1
		self.nsfwToggledGuildsGet.start()
		self.n_url = "https://cdn.discordapp.com/attachments/851472922480607312/874213772569481246/logo.png"
		self.update_hompage.start()
		self.sort_dict = {
				'popular' : Sort.Popular,
				'popular-year' : Sort.PopularYear,
				'popular-month' : Sort.PopularMonth,
				'popular-week' : Sort.PopularWeek,
				'popular-today' : Sort.PopularToday,
				'date' : Sort.Date
			}
	
	async def not_nsfw(self, ctx):
		embed = discord.Embed(color = random.choice(self.Bot.color_list))
		embed.title= f"Non-NSFW channel detected!"
		embed.add_field(name="Why should you care?", value=f"Discord forbids the use of NSFW content outside the NSFW-option enabled channels. [More here](https://discord.com/guidelines#:~:text=You%20must%20apply%20the%20NSFW,sexualize%20minors%20in%20any%20way.)", inline=False)
		embed.add_field(name="How can I enable the NSFW channel option?", value=f"** **", inline=False)
		embed.set_image(url=f"https://cdn.discordapp.com/attachments/802518639274229800/802936914054610954/nsfw.gif")
		embed.set_footer(text=f"Pro tip: {self.Bot.DEFAULT_PREFIX}set_nsfw can do the work for you.")
		await ctx.send(embed=embed)			

	async def doujin_embed(self, ctx, doujin, type:str=None):
		language = Tag.get(doujin.language, property_="name")
		emoji = "🌐"
		if language == "english":
			emoji = "<:English_language:802096460170395658> Eng"
		if language == "japanese":
			emoji = "<:Japanese:802096455962984468> Jap"
		if language == "chinese":
			emoji = "<:FlagChina:802097002364010527> Cn"
		type_= self.get_doujin_tags(tags=doujin.category)[0]
		uploded = human(doujin.upload_date, 4)
		try:
			author = self.get_doujin_tags(tags=doujin.artist)[0]
		except IndexError:
			author = "Unknown"
		embed = discord.Embed(title=doujin.title(Format.Pretty),
			url=doujin.url, color=random.choice(self.Bot.color_list))
		embed.add_field(name="Language", value=f"{emoji} ")
		embed.add_field(name="Artist", value=f" {author}")
		embed.add_field(name="Type", value = type_)
		if doujin.num_favorites == 0:
			embed.add_field(name="Favorites", value=f"For some reason this is broken :(")
		else:
			embed.add_field(name="Favorites", value=f"{(doujin.num_favorites)}")
		embed.add_field(name="Pages", value=f" {doujin.num_pages}")
		embed.add_field(name="Upload Date", value=f" {uploded}")
		embed.set_thumbnail(url=doujin.cover)
		
		clean_tags = Tag.get(doujin.tag, property_="name")
		matches = ["lolicon", "shotacon", "gore", "guro", "rape", "cannibalism", "eye penetration", 
				"forbidden content", "scat",
		]
		if any(x in clean_tags for x in matches):
			if not ctx.guild.id in self.Bot.nsfwToggledGuilds: 
				embed = discord.Embed(description ="The content you searched up has images that are not allowed by default.\n Use `dh nsfwtoggle enable` to enable it. Enabling this will also enable booru commands. \n**USING THIS FEATURE IS NOT RECOMMENDED USE AT YOUR OWN RISK!!!**")
				return await ctx.send(embed= embed)
			else:
				pass
		tags = self.get_doujin_tags(tags=doujin.tag)
		embed.add_field(name="Tags",value=f' | '.join(tags), inline=False)
		if doujin.character:
			characters = self.get_doujin_tags(tags=doujin.character)
			embed.add_field(name="Characters",value=' | '.join(characters), inline=False)

		if doujin.parody:
			parodies = self.get_doujin_tags(tags=doujin.parody)
			embed.add_field(name="Parody?",value=f' | '.join(parodies), inline=False)
		if doujin.group:
			group = self.get_doujin_tags(tags= doujin.group)
			embed.add_field(name="Group",value=f' | '.join(group), inline=False)

		if doujin.related:
			related = self.get_related_doujins(doujin.related)
			embed.add_field(name="Related",value=f'\n'.join(related), inline=False)

		row = ActionRow(
			Button(style=ButtonStyle.primary, label="Read", custom_id="first_option") ,
			Button(style=ButtonStyle.primary, label="Send Images", custom_id="second_option"),
			Button(style=ButtonStyle.primary, label="Reading Room", custom_id="third_option"),
			Button(style=ButtonStyle.primary, label="Download", custom_id="fourth_option")
		)
		if type is not None and type == "only_embed":
			return embed
		msg = await ctx.send(embed=embed, components = [row])
		def check(inter):
			return inter.author == ctx.author
		try:
			inter = await msg.wait_for_button_click(check=check, timeout=30)
			await msg.delete()
			if inter.button.label== f'Read':
				menu = ButtonsMenu(ctx, menu_type=ButtonsMenu.TypeEmbed, timeout=90, show_page_director=False)
				list_ = doujin.image_urls
				for i in list_:
					e = discord.Embed(description = f"[Direct link]({doujin.url})")
					e.set_image(url=i)
					menu.add_page(e)
				buttons = [ComponentsButton(style=ComponentsButton.style.primary, label = '' ,emoji='⏪', custom_id=ComponentsButton.ID_GO_TO_FIRST_PAGE),
					ComponentsButton(style=ComponentsButton.style.primary, label = '' ,emoji='◀️', custom_id=ComponentsButton.ID_PREVIOUS_PAGE),
					ComponentsButton(style=ComponentsButton.style.primary, label = '' ,emoji='⏹️', custom_id=ComponentsButton.ID_END_SESSION),
					ComponentsButton(style=ComponentsButton.style.primary, label = '' ,emoji='▶️', custom_id=ComponentsButton.ID_NEXT_PAGE),
					ComponentsButton(style=ComponentsButton.style.primary, label = '' ,emoji='⏩', custom_id=ComponentsButton.ID_GO_TO_LAST_PAGE)
				]
				for button in buttons:
					menu.add_button(button)
				await menu.start()
					
			if inter.button.label== f'Send Images':
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
					
			if inter.button.label== f'Reading Room':
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


			if inter.button.label== f'Download':
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

	
	@commands.command(aliases = ['doujin_id'], description=f"Lets you read hentai through the use of N-hentai API, you will need to use the hentai code as the search attribute.", usage = "dh doujin 00000")
	@commands.guild_only()
	@commands.cooldown(1, 5, commands.BucketType.user)
	async def doujin(self, ctx, id: int):
		
		if ctx.channel.is_nsfw():
			if not Hentai.exists(id):
				await ctx.send("404 not found")
			else:
				doujin = Hentai(id)
				await self.doujin_embed(ctx=ctx, doujin=doujin)
		else:
			await self.not_nsfw(ctx=ctx)

	@commands.command(description=f"Gets a random doujin for you", usage = "dh doujin_random")
	@commands.guild_only()
	@commands.cooldown(1, 5, commands.BucketType.user)
	async def doujin_random(self, ctx):
		
		if ctx.channel.is_nsfw():
			doujin = Utils.get_random_hentai()
			await self.doujin_embed(ctx=ctx, doujin=doujin)
		else:
			await self.not_nsfw(ctx=ctx)
	@commands.command(description=f"General understanding of sorting and tags ig.")
	@commands.guild_only()
	async def doujin_sorting(self, ctx):
		list = [*self.sort_dict]
		await ctx.send("Currenty available tags are: "+", ".join(list))

	@commands.command(description=f"Gets a random doujin id for you", usage = "dh doujin_random_id")
	@commands.guild_only()
	@commands.cooldown(1, 5, commands.BucketType.user)
	async def doujin_random_id(self, ctx):
		if ctx.channel.is_nsfw():
			return await ctx.send(content = Utils.get_random_id())
		else:
			await self.not_nsfw(ctx=ctx)

	@commands.command(description="Get the results for your tag search on nhentai.net. You can also assign the page number and the sorting of the pages. Dh doujin_sorting for sorting info.",
	usage="dh doujin_tag milf 1 date")
	@commands.guild_only()
	@commands.cooldown(1, 5, commands.BucketType.user)
	async def doujin_tag(self, ctx, tag:str, page:int=1, sort:str="popular"):
		if not ctx.channel.is_nsfw():
			return await self.not_nsfw(ctx=ctx)
		
		try:
			sort = self.sort_dict[f'{sort}']
		except KeyError:
			await ctx.send("Wrong sort provided, falling back to popular sort.")
		
		query = "tag:"+tag
		doujins = Utils.search_by_query(query = query, page= page, sort = sort)
		return await self.send_doujins_info(ctx, doujins)

	@commands.command(description="Get the results for your parodies search on nhentai.net. You can also assign the page number and the sorting of the pages. Dh doujin_sorting for sorting info.",
	usage="dh doujin_parody one-piece 1 date")
	@commands.guild_only()
	@commands.cooldown(1, 5, commands.BucketType.user)
	async def doujin_parody(self, ctx, parody:str, page:int=1, sort:str="popular"):
		if not ctx.channel.is_nsfw():
			return await self.not_nsfw(ctx=ctx)
		try:
			sort = self.sort_dict[f'{sort}']
		except KeyError:
			await ctx.send("Wrong sort provided, falling back to popular sort.")
		
		query = "parody:"+parody.replace("_","-")
		doujins = Utils.search_by_query(query = query, page= page, sort = sort)
		return await self.send_doujins_info(ctx, doujins)

	@commands.command(description="Get the results for your artist search on nhentai.net. You can also assign the page number and the sorting of the pages. Dh doujin_sorting for sorting info.",
	usage="dh doujin_artist crimson 1 date")
	@commands.guild_only()
	@commands.cooldown(1, 5, commands.BucketType.user)
	async def doujin_artist(self, ctx, artist:str, page:int=1, sort:str="popular"):
		if not ctx.channel.is_nsfw():
			return await self.not_nsfw(ctx=ctx)
		try:
			sort = self.sort_dict[f'{sort}']
		except KeyError:
			await ctx.send("Wrong sort provided, falling back to popular sort.")
		
		query = "artist:"+artist.replace("_","-")
		doujins = Utils.search_by_query(query = query, page= page, sort = sort)
		return await self.send_doujins_info(ctx, doujins)

	@commands.command(description="Get the results for your group search on nhentai.net. You can also assign the page number and the sorting of the pages. Dh doujin_sorting for sorting info.",
	usage="dh doujin_group crimson-comics 1 date")
	@commands.guild_only()
	@commands.cooldown(1, 5, commands.BucketType.user)
	async def doujin_group(self, ctx, group:str, page:int=1, sort:str="popular"):
		if not ctx.channel.is_nsfw():
			return await self.not_nsfw(ctx=ctx)
		try:
			sort = self.sort_dict[f'{sort}']
		except KeyError:
			await ctx.send("Wrong sort provided, falling back to popular sort.")
		
		query = "group:"+group.replace("_","-")
		doujins = Utils.search_by_query(query = query, page= page, sort = sort)
		return await self.send_doujins_info(ctx, doujins)

	@commands.command(description="Get the results for your character search on nhentai.net. You can also assign the page number and the sorting of the pages. Dh doujin_sorting for sorting info.",
	usage="dh doujin_character rin-tosaka 1 date")
	@commands.guild_only()
	@commands.cooldown(1, 5, commands.BucketType.user)
	async def doujin_character(self, ctx, character:str, page:int=1, sort:str="popular"):
		if not ctx.channel.is_nsfw():
			return await self.not_nsfw(ctx=ctx)
		
		try:
			sort = self.sort_dict[f'{sort}']
		except KeyError:
			await ctx.send("Wrong sort provided, falling back to popular sort.")
		
		query = "character:"+character.replace("_", "-")
		doujins = Utils.search_by_query(query = query, page= page, sort = sort)
		return await self.send_doujins_info(ctx, doujins, description=f"**Doujins related to character {character} sorted by {sort.value}**.")

		

	@commands.command(description="Get the current homepage of nhentai.net." , usage = "dh doujin_homepage")
	@commands.guild_only()
	@commands.cooldown(1, 60, commands.BucketType.user)
	async def doujin_homepage(self, ctx):
		if not ctx.channel.is_nsfw():
			return await self.not_nsfw(ctx=ctx)
		embed = discord.Embed()
		embed.set_thumbnail(url = self.n_url)
		embed.description = f"Recent homepage of [Nhentai.net](https://nhentai.net)"
		embed.add_field(name="Popular Now", value="\n".join(self.data['popular']), inline=False)
		embed.add_field(name="New Uploads#1 ", value="\n".join(self.data['new'][:6]), inline=False)
		embed.add_field(name="New Uploads#1.5 ", value="\n".join(self.data['new'][6:12]), inline=False)
		embed.add_field(name="New Uploads#2 ", value="\n".join(self.data['new'][12:18]), inline=False)
		embed.add_field(name="New Uploads#3 ", value="\n".join(self.data['new'][18:]), inline=False)
		embed.set_footer(text="The data is updated every 30 minutes.")
		await ctx.send(embed=embed)

	@commands.command(description="Get the current populars of nhentai.net." , usage = "dh doujin_popular")
	@commands.guild_only()
	@commands.cooldown(1, 5, commands.BucketType.user)
	async def doujin_popular(self, ctx):
		if not ctx.channel.is_nsfw():
			return await self.not_nsfw(ctx=ctx)
		embed = discord.Embed()
		embed.set_thumbnail(url = self.n_url)
		embed.description = f"Recent populars of [Nhentai.net](https://nhentai.net)"
		embed.add_field(name="Popular Now", value="\n".join(self.data['popular']), inline=False)
		return await ctx.send(embed = embed)

	def get_doujin_tags(self, tags):
		filtered = []
		n = 0
		for tag in tags:
			hyperlink = f"[{tag.name}({tag.count})]({tag.url})"
			filtered.append(hyperlink)
			n += len(hyperlink)
			if n >= 1000:
				break
		return filtered
	
	def get_related_doujins(self, doujins):
		filtered = []
		n = 1
		for doujin in doujins:
			hyperlink = f"`{n}.` [{doujin.title(Format.Pretty)}]({doujin.url}) 📄`{doujin.num_pages}` ❤️`{doujin.num_favorites}`"
			filtered.append(hyperlink)
			n += 1

		return filtered

	async def send_doujins_info(self, ctx, doujins, description:str=f"Powered by [Danime](https://danimebot.xyz/)"):
		filtered = []
		for doujin in doujins:
			hyperlink = f"`ID : {doujin.id}` -> [{doujin.title(Format.Pretty)}]({doujin.url}) with 📄`{doujin.num_pages}` and ❤️`{doujin.num_favorites}.`"
			filtered.append(hyperlink)
		embed = discord.Embed()
		embed.description = f"{description}"
		embed.set_thumbnail(url = self.n_url)
		embed.add_field(name="Results#1", value="\n".join(filtered[:5]), inline=False)
		embed.add_field(name="Results#2", value="\n".join(filtered[5:10]), inline=False)
		embed.add_field(name="Results#3", value="\n".join(filtered[10:15]), inline=False)
		embed.add_field(name="Results#4", value="\n".join(filtered[15:20 ]), inline=False)
		embed.add_field(name="Results#4", value="\n".join(filtered[20:25 ]), inline=False)
		embed.set_footer(text = "Use dh doujin <id> to read these.")
		try:
			await ctx.send(embed=embed)
		except discord.HTTPException:
			await ctx.send("Unknow error occured make sure your query is correct.")

	@commands.command(aliases=['enable_nsfw'],description='Enables the NSFW option from channel settings.')
	@commands.guild_only()
	@commands.has_permissions(manage_channels=True)
	async def set_nsfw(self, ctx):
		await ctx.channel.edit(nsfw = True)
		await ctx.send(f"The channel {ctx.channel.mention} is now a NSFW channel, thanks for the co-operation.")



	@commands.group(pass_context=True)
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
			return await ctx.send(f"Toggle turned on, takes 15-20 seconds for changes to be applied.")
		return await ctx.send("Already enabled, use `dh nsfwtoggle disable` to disabled it.")

	@nsfwtoggle.command(pass_context=True)
	@commands.has_permissions(administrator = True)
	async def disable(self, ctx):
		db = self.Bot.db1['AbodeDB']
		collection = db['nsfwtoggle']
		try:
			search = collection.find_one({"_id" : ctx.guild.id})
			if search is None:
				return await ctx.send("No feature found.")
			collection.delete_one({"_id" : ctx.guild.id})
			self.Bot.nsfwToggledGuilds.remove(ctx.guild.id)
			return await ctx.send("The feature has been disabled.")
		except:
			return await ctx.send("The feature is already disabled.")

	@tasks.loop(seconds=15)
	async def nsfwToggledGuildsGet(self):
		if self.Bot.DEFAULT_PREFIX == "&":
			return
		await self.Bot.wait_until_ready()
		db = self.Bot.db1['AbodeDB']
		collection= db['nsfwtoggle']
		search = collection.find()
		for guild in search:
			id_ = guild["_id"]
			if not id_ in self.Bot.nsfwToggledGuilds:
				self.Bot.nsfwToggledGuilds.append(id_)
		
		return

	@tasks.loop(minutes=30)
	async def update_hompage(self):
		await self.Bot.wait_until_ready()
		if self.Bot.DEFAULT_PREFIX == "&":
			return
		self.data = requests.get(f"{self.Bot.api_url}doujin_homepage").json()
		return
		

def setup (Bot):
	Bot.add_cog(hentaii(Bot))
	print("Hentai cog is working.")
