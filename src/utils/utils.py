import discord
from discord.ext import commands
from discord.ext.buttons import Paginator
import re
color = 0xa100f2


class DanimeCommandsFinal(commands.Command):
    def __init__(self, func, **kwargs):
        super().__init__(func, **kwargs)
        self.premium = True if  kwargs.pop("premium") == True else False



def DanimeCommands(*args, **kwargs):
    return commands.command(*args, **kwargs, cls=DanimeCommandsFinal)

class Pag(Paginator):
    async def teardown(self):
        try:
            await self.page.delete()

        except discord.HTTPException:
            pass

time_regex = re.compile("(?:(\d{1,5})(h|s|m|d))+?")
time_dict = {'h': 3600, 's': 1, 'm': 60, 'd': 86400}
class Convert(commands.Converter):
    async def convert(self, ctx, argument):
        args = argument.lower()
        matches = re.findall(time_regex, args)
        time = 0
        for key, value in matches:
            try:
                time += time_dict[value] * float(key)
            except KeyError:
                raise commands.BadArgument(f"Please use a valid timeframe.")
            except ValueError:
                raise commands.BadArgument(f"Only numbers!")
        return time






