from discord.ext import commands, tasks
from core.danime import Danime
import os
from dislash import *
import logging
import contextlib

os.environ["JISHAKU_HIDE"] = "True"
os.environ["JISHAKU_NO_UNDERSCORE"] = "True"
os.environ["JISHAKU_NO_DM_TRACEBACK"] = "True"

class RemoveNoise(logging.Filter):
    def __init__(self):
        super().__init__(name='discord.state')

    def filter(self, record):
        return (
            record.levelname != 'WARNING'
            or 'referencing an unknown' not in record.msg
        )

# For discord.py basic logging
@contextlib.contextmanager
def setup_logging():
    try:
        logging.getLogger('discord').setLevel(logging.INFO)
        logging.getLogger('discord.http').setLevel(logging.WARNING)
        logging.getLogger('discord.state').addFilter(RemoveNoise())

        log = logging.getLogger()
        log.setLevel(logging.INFO)
        handler = logging.StreamHandler()
        dt_fmt = "%Y-%m-%d %H:%M:%S"
        fmt = logging.Formatter('[{asctime}] [{levelname:<7}] {name}: {message}', dt_fmt, style='{')
        handler.setFormatter(fmt)
        log.addHandler(handler)

        yield
    finally:
        handlers = log.handlers[:]
        for hdlr in handlers:
            hdlr.close()
            log.removeHandler(hdlr)

bot = Danime()
SlashClient(bot)
@bot.event
async def on_ready() -> None:
    for cmd in bot.commands:
        bot.commandName.append(cmd.name)
    bot.logger.info("Bot is running, don't forget to run other processes too.")

if __name__ == "__main__":
    with setup_logging():
        bot.bootup()
