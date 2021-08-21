import discord
from discord.ext import commands
from discord.ext.commands import errors
import datetime
from utils import checks
cross = ":x:"
class Exceptor(commands.Cog, name="Exceptor"):
    def __init__(self, Bot):
        self.Bot = Bot
    
    @commands.Cog.listener()
    async def on_command_error(self, ctx, error):
        if hasattr(ctx.command, 'on_error'):
            return
        
        elif isinstance(error, errors.MissingRequiredArgument):
            await ctx.send(f"{cross} | You missed the `{error.param.name}` argument.")
        
        elif isinstance(error, commands.BadArgument):
            if isinstance(error, commands.MessageNotFound):
                await ctx.send(f"{cross} | A message for the argument `{error.argument}` was not found.")
            elif isinstance(error, commands.MemberNotFound):
                await ctx.send(f"{cross} | A member for the argument `{error.argument}` was not found.")
            elif isinstance(error, commands.UserNotFound):
                await ctx.send(f"{cross} | A user for the argument `{error.argument}` was not found.")
            elif isinstance(error, commands.ChannelNotFound):
                await ctx.send(f"{cross} | A channel/category for the argument `{error.argument}` was not found.")
            elif isinstance(error, commands.RoleNotFound):
                await ctx.send(f"{cross} | A role for the argument `{error.argument}` was not found.")
            elif isinstance(error, commands.EmojiNotFound):
                await ctx.send(f"{cross} | A emoji for the argument `{error.argument}` was not found.")
            elif isinstance(error, commands.ChannelNotReadable):
                await ctx.send(f"{cross} | I do not have permission to view the channel `{error.argument}`")
            elif isinstance(error, commands.PartialEmojiConversionFailure):
                await ctx.send(f"{cross} | The argument `{error.argument}` did not match the partial emoji format.")
            elif isinstance(error, commands.BadInviteArgument):
                await ctx.send(f"{cross} | The invite that matched that argument was not valid or expired.")
            elif isinstance(error, commands.BadBoolArgument):
                await ctx.send(f"{cross} | The argument `{error.argument}` was not a vald True/False value.")
            elif isinstance(error, commands.BadColourArgument):
                await ctx.send(f"{cross} | The argument `{error.argument}` was not a valid color.")
        
            else:
                pass
        
            return
    
        elif isinstance(error, commands.MaxConcurrencyReached):
            await ctx.send(f"{cross} | This command is already running in this server. Please wait for it to finish.")
            return

        elif isinstance(error, commands.CommandNotFound):
            return
        
        elif isinstance(error, errors.CommandOnCooldown):
            if ctx.guild.id in self.Bot.premium_guilds:
                return await ctx.reinvoke()
            return await ctx.send(f"{cross} | This command is on cooldown. Try again in {error.retry_after:.2f} seconds.")
        
        elif isinstance(error, commands.NoPrivateMessage):
            return

        elif isinstance(error, commands.MissingPermissions):
            permissions ='\n'.join(
                [f'> {permission}' for permission in error.missing_perms])
            await ctx.send(f"{cross} | You lack **`{permissions}`** permissions to run this command.")
        
        elif isinstance(error, commands.BotMissingPermissions):
            permissions ='\n'.join(
                [f'> {permission}' for permission in error.missing_perms])
            message = f"{cross} | I am missing **`{permissions}`** to run the comand `{ctx.command}`.\n"
            try:
                await ctx.send(message)
            except discord.Forbidden:
                try:
                    await ctx.author.send(f"Hey it looks like I can't send messages in that channel.\nAlso I am missing **`{permissions}`** to run the command.")
                except discord.Forbidden:
                    pass
            return
        
        elif isinstance(error, commands.CheckFailure):
            return
        
        elif isinstance(error, discord.Forbidden):
            return

        else:
            em = discord.Embed(title=f" Error encountered!",description="A bug or error is detected!",color=discord.Color.orange())
            em.add_field(name="Bug/Error : ",value=f"```{error}```",inline=False)
            em.add_field(name="Support Server Link",value=f"Please report it here : [Support Server]({self.Bot.support})",inline=False)
            em.set_footer(text=f"Bug Hunter: {ctx.message.author}")
            await ctx.send(embed=em)

def setup(Bot):  
    Bot.add_cog(Exceptor(Bot))
    print("Error cog is working.")