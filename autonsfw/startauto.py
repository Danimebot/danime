import os 
import json
import discord
from discord.ext import commands, tasks
import requests
import sys 
import traceback
from pymongo import MongoClient
import certifi

path = "/home/ubuntu/danime/configs.json"

if not os.path.exists(path):
	path = "/home/vein/Documents/danime/configs.json"

with open(path) as jsonfile:
    obj = json.load(jsonfile)
    token = obj['data']['token']
    db1_token = obj['data']['db1']
    db2_token = obj['data']['db2']
    api_url = obj['data']['api_url']
   
jsonfile.close()

prefix = "&"
bot = commands.Bot(command_prefix = prefix)
bot.DEFAULT_PREFIX = prefix
bot.api_url = api_url
bot.colors = {
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
bot.color_list = [c for c in bot.colors.values()]
bot.counter = 0
bot.github = "https://github.com/Vein05/danime"
bot.website_link = "https://danime.netlify.app/"
bot.cupped_fist = "<:Cuppedfist:757112296094040104>"
bot.invite= "https://discord.com/api/oauth2/authorize?client_id=861117247174082610&permissions=392304&scope=bot"
bot.support = "https://discord.com/invite/aTzduKANKh"

extensions = [
	"cogs.autonsfw"
]
if __name__ == "__main__":
    for extension in extensions:
        try:
            bot.load_extension(extension)
        except Exception as e:
            print(f"Error loading the {extension}", file=sys.stderr)
            traceback.print_exc()

@bot.event
async def on_ready():
	print("Autonsfw working.")

bot.db1 = MongoClient(db1_token, tlsCAFile=certifi.where())
bot.db2 = MongoClient(db2_token, tlsCAFile=certifi.where())

bot.run(token)