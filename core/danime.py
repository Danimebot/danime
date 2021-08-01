import discord
from discord.ext import commands
import sys
import os
import traceback
import discord.utils
from pymongo import MongoClient
import os
import random
import jishaku
import certifi
import json
import datetime
import logging

# prefix = "&"
prefix = ("dh ", "Dh ")
vein_id  = 427436602403323905
intents = discord.Intents.default()
intents.guilds = True

# Jishaku Flags
os.environ["JISHAKU_HIDE"] = "True"
os.environ["JISHAKU_NO_UNDERSCORE"] = "True"
os.environ["JISHAKU_NO_DM_TRACEBACK"] = "True"

with open('configs.json') as jsonfile:
    obj = json.load(jsonfile)
    token = obj['data']['token']
    db1_token = obj['data']['db1']
    db2_token = obj['data']['db2']
    api_url = obj['data']['api_url']
    gelbooru_token = obj['data']['gelbooru_token']
    danbooru_token = obj['data']['danbooru_token']
    booru_username = obj['data']['booru_username']
    booru_password = obj['data']['booru_password']
    anon_token = obj['data']['anon_token']
    saucenao_keys = obj['data']['saucenao_keys']

jsonfile.close()

# For basic bot logging
logger = logging.getLogger('WardenLog')
hdlr = logging.StreamHandler()
frmt = logging.Formatter('[{asctime}] [{levelname:<7}] {name}: {message}', "%Y-%m-%d %H:%M:%S", style='{')
hdlr.setFormatter(frmt)
logger.addFilter(hdlr)

class Danime(commands.AutoShardedBot):
	def __init__(self) -> None:
		allowed_mentions = discord.AllowedMentions(roles=False, everyone=False, users=True)
		
		super().__init__(command_prefix=prefix,
				owner_id = vein_id, case_insensitive=True,chunk_guilds_at_startup=False, allowed_mentions=allowed_mentions, intents=intents)
		self.remove_command("help")
		self.DEFAULT_PREFIX = prefix
		self.color = 0xa100f2
		self.vein_id = vein_id
		self.guild_id = 802529391808086066
		self.github = "https://github.com/danimebot/danime"
		self.website_link = "https://danimebot.xyz/"
		self.cupped_fist = "<:Cuppedfist:757112296094040104>"
		self.invite= "https://discord.com/api/oauth2/authorize?client_id=861117247174082610&permissions=392304&scope=bot"
		self.support = "https://discord.com/invite/aTzduKANKh"
		self.starttime = datetime.datetime.utcnow()
		self.pfp = "https://cdn.discordapp.com/avatars/797456198932103189/3cfde6cfddfd2eb7c2933473d6661bb1.png?size=1024"
		self.api_url = api_url
		self.counter = 0
		self.gelbooru_token = gelbooru_token
		self.danbooru_token = danbooru_token
		self.booru_username = booru_username
		self.booru_password = booru_password
		self.saucenao_keys = saucenao_keys
		self.anon_token = anon_token
		self.logger = logger
		self.tips  = [
		  'You can set the current channel to nsfw with dh set_nsfw',
		  'Feel free to join the support server for your queries',
		  'To get help on each command use, dh help commandname',
		  'Feel free to get into touch with us if you find a dead link',
		  'Introduce danime to your friends and share together!',
		  'Like to submit pics? Join the support server',
		  'You can use the autonsfw command to get nsfw pics every minute',
		  'The DanimeAPI has 50k+ image data and is still growing!!'
		]
		self.colors: dict = {
		    "WHITE": 0x26fcff,
		    "AQUA": 0x1ABC9C,
		    "GREEN": 0x2ECC71,
		    "BLUE": 0x3498DB,
		    "PURPLE": 0x9B59B6,
		    "LUMINOUS_VIVID_PINK": 0xE91E63,
		    "GOLD": 0xF1C40F,
		    "ORANGE": 0xE67E22,
		    "who_even_likes_red_bruh!": 0xa5ddff,
		    "NAVY": 0x34495E,
		    "DARK_AQUA": 0x11806A,
		    "Light_blue": 0x30ffcc,
		    "ok": 0x206694,
		    "DARK_PURPLE": 0x71368A,
		    "DARK_VIVID_PINK": 0xAD1457,
		    "DARK_GOLD": 0xC27C0E,
		    "cool_color": 0x6891ff,
		    "something": 0xfc7bb2,
		    "DARK_NAVY": 0xe8c02a,
		    "Hm": 0xebf54c,
		    "nice_color": 0xfc00f1,
		    "nice_color2": 0x21f5fc,
		    "very_nice_color": 0x25c059,
		    "my_fav": 0xb863f2
		}
		self.color_list = [c for c in self.colors.values()]
		self.nsfwToggledGuilds = []
		self.db1 = MongoClient(db1_token, tlsCAFile=certifi.where())
		self.db2 = MongoClient(db2_token, tlsCAFile=certifi.where())
		self.commandName = []
		self.logger.info("Hello, World!")
		self._extensions = (
						'cogs.anime',
						'cogs.owner',
						'nsfw.hentaii',
						'cogs.help',
						'cogs.mod',
						'cogs.games',
						'cogs.fun',
				    # 'cogs.novel',
				    # 'cogs.scrapper'
				    'cogs.logs',
				    'misc.error',
				    'misc.config',
				    'cogs.topics',
				    'cogs.stolencode',
				    'cogs.sauce',
				    'misc.api',
				    'cogs.autonsfw',
				    'nsfw.booru',
				    "nsfw.nsfw",
				    "nsfw.nsfw2",
				    "sfw.safe",
				    "cogs.stealemoji",
				    "misc.whatis"
			)

	def __repr__(self) -> str:
		return super().__repr__()

	def bootup(self) -> None:
		for extension in self._extensions:
			try:
				self.load_extension(extension)
				self.logger.info(f"Loaded Extension - {extension}")
			except Exception as e:
					self.logger.error(f'Error loading the {extension}')
					traceback.print_exc()

		self.load_extension("jishaku")
		self.run(token)
