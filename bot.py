import discord
from discord.ext import commands, tasks
import sys
import os
import traceback
import discord.utils
from pymongo import MongoClient
import os
import datetime
import psutil
import random
import jishaku
import certifi
from misc import emoji
import json

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
jsonfile.close()

    
# prefix = "&"
prefix = "dh "
vein_id  = 427436602403323905
intents = discord.Intents.all()
# bot = commands.AutoShardedBot(command_prefix=prefix, case_insensitive=True, intents=intents, owner_id=vein_id, chunk_guilds_at_startup=False)
bot = commands.AutoShardedBot(command_prefix=["dh ", "Dh "], case_insensitive=True, intents=intents, owner_id=vein_id, chunk_guilds_at_startup=False)

bot.DEFAULT_PREFIX = prefix
bot.remove_command("help")
bot.color = 0xa100f2
bot.vein_id = vein_id
bot.guild_id = 802529391808086066
bot.github = "https://github.com/Vein05/danime"
bot.website_link = "https://danime.netlify.app/"
bot.cupped_fist = "<:Cuppedfist:757112296094040104>"
bot.invite= "https://discord.com/api/oauth2/authorize?client_id=861117247174082610&permissions=392304&scope=bot"
bot.support = "https://discord.com/invite/aTzduKANKh"
bot.starttime = datetime.datetime.utcnow()
bot.pfp = "https://cdn.discordapp.com/avatars/797456198932103189/3cfde6cfddfd2eb7c2933473d6661bb1.png?size=1024"
bot.api_url = api_url
bot.counter = 0
bot.gelbooru_token = gelbooru_token
bot.danbooru_token = danbooru_token
bot.booru_username = booru_username
bot.booru_password = booru_password
bot.anon_token = anon_token
bot.tips  = [
    'You can set the current channel to nsfw with dh set_nsfw',
    'Feel free to join the support server for your queries',
    'To get help on each command use, dh help commandname',
    'Feel free to get into touch with us if you find a dead link',
    'Introduce danime to your friends and share together!',
    'Like to submit pics? Join the support server',
    'You can use the autonsfw command to get nsfw pics every minute',
    'The DanimeAPI has 35k+ image data and is still growing!!'
]

@bot.event
async def on_ready():
    await bot.wait_until_ready()
    status.start()
    bot.commandName = []
    for cmd in bot.commands:
        bot.commandName.append(cmd.name)
    print("Bot is running.")
    vein= bot.get_guild(802529391808086066).get_member(vein_id)
    await vein.send("https://cdn.discordapp.com/attachments/774905992743747584/795535756759531530/sob.jpg")

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


@bot.command(aliases=['botinfo'])
@commands.guild_only()
async def stats(ctx):
    now = datetime.datetime.utcnow()
    elapsed = now - bot.starttime
    seconds = elapsed.seconds
    minutes, seconds = divmod(seconds, 60)
    hours, minutes = divmod(minutes, 60)   

    users = 0
    for guild in bot.guilds:
        try:
            users += guild.member_count
        except:
            pass

    guilds = str(len(bot.guilds))

    invite_link = f"[Invite link]({bot.invite})"
    vote = "Soon"
    
    cpu = str(psutil.cpu_percent())
    boot_time = str(psutil.boot_time() / 100000000)
    boot_time_round = boot_time[:4]

    owner = bot.get_user(427436602403323905)
    embed = discord.Embed(timestamp=bot.starttime ,
        color=0x26fcff,
        description="```asciidoc\n"
                    +"Name: Danime\n"
                    +f"Bot Latency: {round(bot.latency * 1000)}ms\n"
                    +f"Web Socket Latency: {round(bot.latency * 1000, 2)}ms\n"
                    +f"Runtime: {elapsed.days} days, {hours} hours, {minutes} minutes and {seconds} seconds\n"
                    +"```"

        )
    embed.set_author(name=f"Danime's Information")
    embed.add_field(name=f"General ", inline=True, value=f"```asciidoc\nBoot Time: {boot_time_round}s\nUsers: {users}\nServer: {guilds}```\n")
    embed.add_field(name=f"Bot", inline=True, value=f"```asciidoc\nDiscord.py: {discord.__version__}\nPython: 3.8.7\nDanime: 1.3\n```")
    embed.add_field(name=f"System", inline=True, value=f"```asciidoc\nOS: {sys.platform}\nCPU Usage: {cpu}%\n```")
    embed.add_field(name=f"Creator", inline=False, value=f"```asciidoc\nUsername: {owner.name}#{owner.discriminator} [{owner.id}]```")
    embed.add_field(name=f"Links", inline=False, value=f'[Invite]({bot.invite}) |  [Support Server]({bot.support}) |  [Github]({bot.github}) |  [Website]({bot.website_link}) |  [Vote]({vote})')
    embed.set_footer(text=f"Last restart",icon_url=ctx.me.avatar_url)

    await ctx.send(embed=embed)
    


@bot.event
async def on_guild_join(guild):
    if bot.DEFAULT_PREFIX == "&":
        return
    vein= bot.get_guild(802529391808086066).get_member(vein_id)

    await vein.send(f"Joined {guild.name} which has ``{guild.member_count}`` members.")
    for channel in guild.text_channels:
        if channel.permissions_for(guild.me).send_messages:
            embed = discord.Embed(color = 0xff4042)
            embed.description= f"Thanks alot for inviting the bot to the server! The prefix is `dh `. Join [support server]({Bot.support}) if needed."
        break

@bot.event
async def on_guild_remove(guild):
    if bot.DEFAULT_PREFIX == "&":
        return
    vein= bot.get_guild(802529391808086066).get_member(vein_id)

    await vein.send(f"Left {guild.name} which has ``{guild.member_count}`` members.")

# async def bruh():
#     guilds = bot.guilds
#     for guild in guilds:
#         if  guild.member_count < 20:
#             print(f"left {guild.name} which has ``{guild.member_count}")
#             await guild.leave()


extensions = [

	'cogs.anime',
	'cogs.owner',
	'nsfw.hentaii',
	'cogs.help',
	'cogs.api',
	'cogs.mod',
	'cogs.games',
	'cogs.fun',
    # 'cogs.novel',
    # 'cogs.scrapper'
    'cogs.logs',
    'misc.error',
    'cogs.pokemon',
    'misc.config',
    # 'cogs.topics',
    'cogs.stolencode',
    'cogs.sauce',
    'misc.api',
    'cogs.autonsfw',
    'cogs.api2',
    'nsfw.booru',
    "sfw.safe"


]
if __name__ == "__main__":
    for extension in extensions:
        try:
            bot.load_extension(extension)
        except Exception as e:
            print(f"Error loading the {extension}", file=sys.stderr)
            traceback.print_exc()


bot.load_extension("jishaku")

@tasks.loop(seconds=60)
async def status():
    await bot.wait_until_ready()
    await bot.change_presence(status=discord.Status.online, 
        activity=discord.Game(f'dh help || {random.choice(bot.tips)}'))    
    return

bot.db1 = MongoClient(db1_token, tlsCAFile=certifi.where())
bot.db2 = MongoClient(db2_token, tlsCAFile=certifi.where())
bot.run(token)
