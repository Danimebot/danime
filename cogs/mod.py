import discord
from discord.ext import commands
from discord import User
import datetime
import typing
import random
from datetime import datetime

color = 0xa100f2
guild = 757098499836739594


class vein(commands.Cog, name="moderation"):
    def __init__(self, Bot):
        self.Bot = Bot

    @commands.Cog.listener()
    async def on_message(self, ctx):
        if self.Bot.DEFAULT_PREFIX == "&":
            return
        
        if ctx.content.startswith("<@!861117247174082610>"):
            embed = discord.Embed()
            embed.description = f"Hello, my prefix is `dh ` you can [invite me]({self.Bot.invite}) from here or join the [support]({self.Bot.support}) server."
            await ctx.channel.send(embed= embed)

    @commands.command()
    @commands.has_permissions(manage_roles=True)
    @commands.guild_only()
    async def role(self, ctx, member: discord.Member, *, arg):
        if ctx.guild.me.top_role < member.top_role:
            return await ctx.send("Admin :(")
        if ctx.message.author.top_role < member.top_role:
            return await ctx.send("You  have lower roles.")
        role = discord.utils.get(ctx.guild.roles, name=f"{arg}")

        if role not in member.roles:
            await member.add_roles(role)
            await ctx.send(f"{member} was given role ``{arg}``.")
        else:
            await member.remove_roles(role)
            await ctx.send(f"{member} was removed from the role ``{arg}``.")

    @commands.command()
    @commands.guild_only()
    @commands.has_permissions(manage_nicknames=True)
    async def cnick(self, ctx, member: discord.Member, *, arg):
        if ctx.guild.me.top_role < member.top_role:
            return await ctx.send("Admin :(")
        if ctx.message.author.top_role < member.top_role:
            return await ctx.send("You  have lower roles.")
        else:
            await member.edit(nick=arg)
            await ctx.send(f'{member} nickname was changed to {arg} by {ctx.message.author}')

    @commands.command(aliases=['rinfo'], )
    @commands.has_permissions(manage_roles=True)
    async def roleinfo(self, ctx, *, rolename):
        allowed = []
        try:
            role = discord.utils.get(ctx.message.guild.roles, name=rolename)
            permissions = role.permissions

            for name, value in permissions:
                if value:
                    name = name.replace('_', ' ').replace(
                        'guild', 'server').title()
                    allowed.append(name)
        except:
            return await ctx.send(f"Couldn't find the role")
        time = role.created_at
        em = discord.Embed(description=f'', color=color, timestamp=time)
        em.set_author(name=f'{rolename}')
        em.set_thumbnail(url=f'{ctx.guild.icon_url}')
        em.add_field(name='__Info__', value=f'**ID :** {str(role.id)} \n'
                                            f'**Color :** {role.color}\n'
                                            f'**Hoisted :** {str(role.hoist)}\n'
                                            f'**Position :** {str(role.position)}\n'
                                            f'**Is mentionable :** {str(role.mentionable)}\n'
                                            f'**Members in role :** {str(len(role.members))}\n')
        em.add_field(name='__Role permissions__',
                     value=f', '.join(allowed), inline=False)
        em.set_footer(text="Role created on")
        await ctx.send(embed=em)

  

    @commands.command( aliases=['cstats'])
    @commands.guild_only()
    @commands.has_permissions(kick_members=True)
    async def channelstats(self, ctx):
        channel = ctx.channel
        tmembers = str(len(channel.members))
        nsfw = (ctx.channel.is_nsfw())
        news = (ctx.channel.is_news())
        embed = discord.Embed(color=color)
        embed.set_thumbnail(url=f'{ctx.guild.icon_url}')
        embed.add_field(name="__Information__", value=f'**Server name: ** {ctx.guild.name} \n'
                        f'**Channel name :** {channel.name}\n'
                        f'**Channel ID : ** {channel.id} \n'
                        f'**Channel type : **{channel.type}\n'
                        f'**Channel category : ** {channel.category}\n'
                        f'**Topic : ** {channel.topic}\n'
                        f'**Channel position :** {channel.position}\n'
                        f'**Created at :** {channel.created_at.strftime("%a, %#d %B %Y, %I:%M %p ")}\n'
                        f'**Slowmode :** {channel.slowmode_delay}\n'
                        f'**Channel Permissions :** {channel.permissions_synced}\n'
                        f'**Channel members :** {tmembers}\n'
                        f'**Is nsfw : ** {nsfw}\n'
                        f'**Is news : ** {news}', inline=False)

        embed.set_author(name="** **", icon_url=f'{ctx.me.avatar_url}')
        embed.set_footer(
            text=f" Requested by {ctx.author}", icon_url=ctx.author.avatar_url)
        embed.timestamp = datetime.utcnow()
        await ctx.send(embed=embed)

    @commands.command()
    @commands.guild_only()
    @commands.has_permissions(manage_roles=True)
    async def slowmode(self, ctx, time:int=None):
        self.Bot.log_channel = self.Bot.get_channel(759583119396700180)
        if time == None:
            await ctx.channel.edit(slowmode_delay=0)
            await ctx.send(f'Slowmode removed.')
        else:

            await ctx.channel.edit(slowmode_delay=time)
            await ctx.send(f'{time}s of slowmode was set on the current channel.')


    @commands.command()
    @commands.guild_only()
    @commands.has_permissions(manage_roles =True, manage_channels=True)
    async def brazilled(self, ctx, user:discord.Member):
        url = "https://cdn.discordapp.com/attachments/847136168088829975/854217852533735424/images.png"
        role = discord.utils.get(ctx.guild.roles, name=f"Brazilled")
        channel = discord.utils.get(ctx.guild.channels, name=f"brazil")
        await user.add_roles(role)
        await ctx.send(f"{user.name} \n{url}")
        await channel.send(f"{user.mention}, welcome to brazil.")



def setup(Bot):
    Bot.add_cog(vein(Bot))
    print("Mod cog is working.")
