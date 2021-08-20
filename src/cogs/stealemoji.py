import discord
from discord.ext import commands
import os
import requests
from typing import Union
from core import danime

class stealemoji(commands.Cog):
	def __init__(self, Bot):
		self.Bot = Bot


	@commands.command(aliases= ['stealemoji', 'steal'], description="You can use this command to add an emoji to your server. Does require you to have nitro.", usage="dh addemoji <emoji> <name|optional>")
	@commands.has_permissions(manage_emojis= True)
	async def addemoji(self, ctx, emoji: Union[discord.Emoji, discord.PartialEmoji], setname:str=None):

		if type(emoji) in [discord.PartialEmoji, discord.Emoji]:
			send = await ctx.send("Emoji detected! Adding it to the guild..")
			emojiUrl = emoji.url
			if setname == None:
				setname = emoji.name
			emojiExtension = self.get_emoji_extension(str(emojiUrl))
			if emojiExtension == None:
				return await send.edit(content = "Error occured while getting emoji extension.")
			getpath = self.download_emoji(emojiUrl, setname, emojiExtension)
			try:
				with open(getpath, "rb") as image:
					createdEmoji = await ctx.guild.create_custom_emoji(name = setname, image = image.read())
					message = f"Sucessfully created emoji with the name `{createdEmoji.name}` and id `{createdEmoji.id}`."
					os.remove(getpath)
					return await send.edit(content=message)
			except discord.Forbidden:
				os.remove(getpath)
				await send.edit(content = "It seems I don't have perms to add that image.")
			except discord.HTTPException:
				os.remove(getpath)
				await send.edit(content= "An error occurred while creating the emoji.")
		else:
			await ctx.send("Emoji not found.")
			
	def download_emoji(self, url, name, extension):
		img_data = requests.get(url).content
		path = "/home/ubuntu/danime/src/download/"
		if not os.path.exists(path):
			path = "/home/vein/Documents/danime/src/download/"

		try:
			with open(f"{path}{name}" + extension, 'wb') as handler:
				handler.write(img_data)
				filepath = f"{path}{name}" + extension
				return filepath
				
		except:
			pass

	def get_emoji_extension(self, url):
		formats = ['jpg', 'png', 'jpeg', 'webp', 'gif']
		for format in formats:
			if url.endswith(format):
				return f".{format}"
		return None

def setup(Bot: danime.Danime):
	Bot.add_cog(stealemoji(Bot))
	Bot.logger.info("Emoji stealer is working.")