import discord
from discord.ext import commands
import requests
from misc.searchchr import charSearch
import re
import random
import cfscrape
from disputils import BotEmbedPaginator
from urllib.request import Request, urlopen
from bs4 import BeautifulSoup as soup
from lxml import etree
from lxml.html import fromstring, HTMLParser
from cogs.utils import Pag
from core import danime

class novel(commands.Cog, name="novel"):
	def __init__(self, Bot):
		self.Bot = Bot
	def removeTags(self, text):
		clean = re.compile('<.*?>')
		return re.sub(clean, '', text)
	

	@commands.command(description="Lets you search about a character from an Anime.")
	@commands.guild_only()
	@commands.cooldown(1, 15, commands.BucketType.user)
	async def character(self,ctx, *, charName):
		result = charSearch(charName)
		
		embed = discord.Embed(color = random.choice(self.Bot.color_list))

		Title = result["data"]["Character"]["name"]["full"]
		charUrl =result["data"]["Character"]["siteUrl"]
		description = self.removeTags(result["data"]["Character"]["description"]).replace("&quot;", '"')

		for title in result["data"]["Character"]["media"]["nodes"]:
			embed.add_field(name="From anime", value='[{}]({})'.format(title["title"]["english"], title["siteUrl"], inline=False))
		embed.set_author(name=f"{Title}", url=f"{charUrl}")
		if len(description) > 1:
			embed.add_field(name="Description", value=description[:1023], inline=False)
		if len(description) >1024:
			embed.add_field(name="** ** ", value=f"{description[1024:2042]}...", inline=False)
		embed.set_thumbnail(url=result["data"]["Character"]["image"]["large"])
		embed.add_field(name="Read more", value=f"[Here]({charUrl})")
		embed.set_footer(text=f"Requested by {ctx.author}")
		send = await ctx.send(embed=embed)
		await send.add_reaction("✅")
		def check(reaction,user):
			return user == ctx.author and user.id != ctx.me.id
		try:
			reaction, user= await self.Bot.wait_for("reaction_add",timeout=30, check=check)
			if str(reaction.emoji) == f'✅':
				await ctx.message.delete()
				await send.delete()
		except:
			return
		

	@commands.command(aliases=["ln"], description=f"Lets you search both wuxia and light novels over the internet.")
	@commands.guild_only()
	@commands.cooldown(1, 60, commands.BucketType.user)
	async def novel(self, ctx, *, title):
		await ctx.message.add_reaction("✅")

		
		query = (re.sub("[ ,.]", "-", title))
		url = f"https://www.lightnovelworld.com/novel/{query}"
		scraper = cfscrape.create_scraper()
		content = (scraper.get(f"{url}").content)  
		page = soup(content, 'html.parser')

		

		query1 = (re.sub("[ ,.]", "-", title))
		url1 = f"https://www.readlightnovel.org/{query1}"
		scraper1 = cfscrape.create_scraper()
		content1 = (scraper1.get(f"{url1}").content)  
		page1 = soup(content1, 'html.parser')	
		image_url = f"{ctx.me.avatar_url}"
		image_url = page1.find("div", {"class":"novel-cover"}).find("a").img["src"]

		

		title =  page.find("h1", {"class": "novel-title text2row"}).text.strip()

		author = page.find("div", {"class": "author"}).find("a").text.strip()
		chapters = page.find("div", {"class": "header-stats"}).find("strong").text.strip()
		chapterNO = chapters[5:]
		try:
			status = page.find("div", {"class": "header-stats"}).find("strong", {"class": "ongoing"}).text.strip()
		except:
			status = "Completed"
		lastUpdate = page.find("div", {"class": "updinfo"}).text.strip()
		

		
		rating =  (page.find("div", {"class": "rating-star"}).find("strong").text.strip())
		ratingtrim = rating[:1]
		trimmed= int(ratingtrim)
		rank1 = page.find("div", {"class": "rank"}).find("strong").text.strip()
		rank = rank1[5:]

		about = page.find("section", {"id": "info"}).find("p", {"class": "description"}).text.strip()
		synopsis = page.find("div", {"class": "content"}).p.text.strip()
		tags_html = page.find("ul", {"class": "content"}).find_all("li")
		tags = []
		for tag in tags_html:
			tags.append(tag.text.strip())
		genre_html = page.find("div", {"class":"categories"}).find_all("li")
		genres= []
		for genre in genre_html:
			genres.append(genre.text.strip())
		views_html = page.find("div", {"class" : "header-stats"}).find_all("span")
		views = ""
		a = 0
		for view in views_html:
			a +=1 
			if a == 2:
				views = view.text.strip()
				break

		star = "⭐"
		half_star = "<:Half_Star:802949209049006100>"
		if trimmed < 1:
			stars= f"{half_star}"
		elif trimmed >1 and trimmed < 1.5:
			stars= f"{star}{half_star}"
			
		elif trimmed ==2:
			stars= f"{star}{star}"
			
		elif trimmed >2 and trimmed < 2.5:
			stars= f"{star}{star}{half_star}"
			
		elif trimmed == 3:
			stars= f"{star}{star}{star}"
			
		elif trimmed >3 and trimmed < 3.5:
			stars= f"{star}{star}{star}{half_star}"
			
		elif trimmed ==4:
			stars= f"{star}{star}{star}{star}"
			
		elif trimmed >4 and trimmed < 4.5:
			stars= f"{star}{star}{star}{star}{half_star}"
			
		elif trimmed ==5:
			stars= f"{star}{star}{star}{star}{star}"
		url = f"https://www.novelupdates.com/series/{query}"
		embed = discord.Embed(color =random.choice(self.Bot.color_list))
		embed.set_thumbnail(url=f"{str(image_url)}")
		embed.set_author(name=f"{title}", url =f"{url}")
		embed.add_field(name="Author", value=f"{author}")
		embed.add_field(name="Chapters", value=f"{chapterNO}")
		embed.add_field(name="Status", value=f"{status}")
		embed.add_field(name="Rank", value=f"{rank}")
		embed.add_field(name="Views", value=f"{views[23:]}")
		embed.add_field(name="Ratings", value=f"{stars}")
		embed.add_field(name="Genres", value=f", ".join(genres), inline=False)
		embed.add_field(name="About", value=f"{about[:1023]}", inline=False)
		embed.add_field(name="Synopsis", value=f"{synopsis[:1023]}", inline=False)
		embed.add_field(name="Tags", value=f", ".join(tags[:50]), inline=False)
		embed.set_footer(text = F"Requested by {ctx.author} | To read this novel just do {self.Bot.DEFAULT_PREFIX}readnovel <novelname>")
		await ctx.send(embed=embed)

		def check(reaction,user):
			return user == ctx.author and user.id != ctx.me.id
		try:
			reaction, user= await self.Bot.wait_for("reaction_add",timeout=30, check=check)
			if str(reaction.emoji) == f'✅':
				await ctx.message.delete()
				await send.delete()
		except:
			return

	@commands.command(aliases = ['novelcheck', 'novelread'], description=f"Lets you read most of the novels out there.")
	@commands.guild_only()
	@commands.cooldown(1, 260, commands.BucketType.user)
	async def readnovel(self, ctx, *, title):
		await ctx.send(f"Searching for {title}")
		query1 = (re.sub("[ ,.]", "-", title))
		url1 = f"https://www.readlightnovel.org/{query1}"
		scraper1 = cfscrape.create_scraper()
		content1 = (scraper1.get(f"{url1}").content)  
		page = soup(content1, 'html.parser')
		title =  page.find("div", {"class":"block-title"}).find("h1").text.strip()
		image_url = page.find("div", {"class":"novel-cover"}).find("a").img["src"]
		# chapters = page.find("div", {"class": "header-stats"}).find("strong").text.strip()
		# chapterNO = chapters[5:]
		embed = discord.Embed(color = random.choice(self.Bot.color_list))
		embed.title= f"Success!, novel found as ``{title}`` with ``0`` chapters."
		embed.description =f"To read this novel react with <:Cuppedfist:757112296094040104>"
		embed.set_image(url=F"{image_url}")
		send = await ctx.send(embed=embed)
		
		await send.add_reaction("<:Cuppedfist:757112296094040104>")
		def check(reaction,user):
			return user == ctx.author and user.id != ctx.me.id
		try:
			reaction, user= await self.Bot.wait_for("reaction_add",timeout=30, check=check)
			if str(reaction.emoji) == f'✅':
				await ctx.message.delete()
				await send.delete()
			if str(reaction.emoji) == f'<:Cuppedfist:757112296094040104>':
				await send.delete()
				send2=  await ctx.send(F"Which chapter do you want to read?")
				a = 0
				try:
				
					
					def check1(m):
						return m.author == ctx.author and m.content.isdigit()
					queryChapter = await self.Bot.wait_for("message", timeout=30, check=check1)
					try:
						await send2.delete()
						
						chapter = queryChapter.content
						
						query = f"{url1}/chapter-{chapter}"
						scraper1 = cfscrape.create_scraper()
						content = (scraper1.get(f"{query}").content)
						page = soup(content, 'html.parser')
						paragraphs_html = page.find("div", {"class":"desc"}).find_all("p")
						paragraphs = []
						for paragraph in paragraphs_html:
							data = paragraph.text.strip()
							data1 = data
							paragraphs.append(data1)

						title = f"Chapter {chapter} | Note you only have a minute to read this page contents."
						await Pag(title=title, color=random.choice(self.Bot.color_list), entries=paragraphs, embed = False,length = 2, timeout = 60).start(ctx)

					except:
						return
				except:
					await ctx.send(f"There probably doesn't exist a chapter by that number, try again after getting the correct chapter.")
		except:
			return	




def setup (Bot: danime.Danime):
	Bot.add_cog(novel(Bot)) 
	Bot.logger.info("Novel cog is working.")