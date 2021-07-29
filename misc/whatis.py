import discord
from discord.ext import commands
import random


class whatiscog(commands.Cog):
	def __init__(self, Bot):
		self.Bot = Bot

	@commands.command()
	async def whatis(self, ctx, item:str=None):
		
		itemdict  = {
			"nsfw" : "The nsfw section of the bot contains artworks from various sites such as danbooru, safebooru, etc. By NSFW we mean artworks that have the rating of explicit on the booru websites, or contain things that should be seen by an adult. This doesn't mean there are only explicit images on this category, Images here can be both SFW and NSFW that have a certian lewd taste to them. If you think like the image is way to off to be in this section feel free to report it in the support server.",

			"sfw" : "The SFW section of the bot contains artworks without the rating explicit images. All or most of the images are from safebooru, so all the images that are set as safe there are alligble to be added to the bot, this included the questionable arts, SFW section's main focus is not to satisy a younger audience but to give the nsfw users some time off and enjoy some cute images, this doesn't mean there will be explicit images included, the bot will abide by discord TOS but I will try to keep things R-17 for the most time."
				
		}
		items = [*itemdict]
		if item is None:
			return await ctx.send(embed=discord.Embed(title="Please pass in any of the following query too.", description=", ".join(items)))
		item = item.lower()
		if item in items:
			embed = discord.Embed(color = random.choice(self.Bot.color_list))
			embed.description = (itemdict[item])
			embed.title = f"What is __{item}__ in the context of Danime?"
			await ctx.send(embed=embed)



def setup(Bot):
	Bot.add_cog(whatiscog(Bot))
	print("What is cog is working")