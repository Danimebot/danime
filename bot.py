from discord.ext import commands, tasks
from core.danime import Danime

bot = Danime()

@bot.event
async def on_ready():
    for cmd in bot.commands:
        bot.commandName.append(cmd.name)
    print("Bot is running, don't forget to run other processes too.")

bot.bootup()
