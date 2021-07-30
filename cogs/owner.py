import discord
import datetime
from datetime import datetime
from discord.ext import commands
# import PIL.Image
# import PIL.ImageDraw
# import PIL.ImageFont
# import PIL.ImageFilter
from io import BytesIO
import asyncio
import random
from pygelbooru import Gelbooru
starttime = datetime.utcnow()
from core import danime


class owner(commands.Cog, name='owner'):
    def __init__(self, Bot):
        self.Bot = Bot

    @commands.command(hidden=True)
    @commands.is_owner()
    async def runtime(self, ctx):
        now = datetime.utcnow()
        elapsed = now - starttime
        seconds = elapsed.seconds
        minutes, seconds = divmod(seconds, 60)
        hours, minutes = divmod(minutes, 60)
        embed = discord.Embed(color=self.Bot.color, timestamp=starttime,
                              description=f'**Abode has been running for ``{elapsed.days}`` days ``{hours}`` hours ``{minutes}`` mminutes and ``{seconds}`` seconds**')
        embed.set_author(name='Runtime', icon_url=ctx.me.avatar_url)
        embed.set_footer(text=f'Last restart')

        await ctx.send(embed=embed)

    @commands.is_owner()
    @commands.guild_only()
    @commands.command(hidden=True)
    async def sayin(self, ctx, channel: discord.TextChannel, *, text: str):
        x = await channel.send(text)


    '''@commands.command(aliases=['mc'])
    @commands.is_owner()
    async def messagecount(self, ctx):
        channel = ctx.channel
        a = 0
        msg = ctx.message
        await msg.add_reaction(':arrow_forward:')
        async for msg in channel.history(limit = None):
            a+= 1

        await msg.add_reaction(":white_check_mark: ")
        await ctx.send(f'{a} messages.')'''

    @commands.command()
    @commands.guild_only()
    @commands.is_owner()
    async def emojilist(self, ctx):
        emojis = sorted([e for e in ctx.guild.emojis if len(
            e.roles) == 0 and e.available], key=lambda e: e.name.lower())
        paginator = commands.Paginator(suffix='', prefix='')
        channel = ctx.channel

        for emoji in emojis:
            paginator.add_line(f'{emoji} ↳ `{emoji}`\n')

        for page in paginator.pages:
            await channel.send(page)

        await ctx.send(ctx.tick(True))

    @commands.command()
    @commands.guild_only()
    @commands.cooldown(1, 10, commands.BucketType.user)
    async def image_info(self, ctx, user: discord.Member = None):
        if user is None:
            user = ctx.message.author
        img = PIL.Image.open("assets/imges/247.jpg")
        asset = user.avatar_url_as(size=128)
        data = BytesIO(await asset.read())
        pfp = PIL.Image.open(data)
        pfp = pfp.resize((835, 911))

        img.paste(pfp, (2407, 53))

        draw = PIL.ImageDraw.Draw(img)
        font = PIL.ImageFont.truetype(
            "assets/fonts/Modern_Sans_Light.otf", 100)
        fontbig = PIL.ImageFont.truetype("assets/fonts/litfont.ttf", 400)

        draw.text((200, 0), "Information:", (255, 255, 255), font=fontbig)
        draw.text((50, 500), "Username:  {}".format(
            user), (255, 255, 255), font=font)
        draw.text((50, 700), "ID:  {}".format(
            user.id), (255, 255, 255), font=font)
        draw.text((50, 900), "Status Type:  {}".format(
            user.status), (255, 255, 255), font=font)
        #draw.text((50,1100), "User Status: {}".format(user.activity.name), (255, 255, 255), font=font)
        draw.text((50, 1100), "Nickname:  {}".format(
            user.display_name), (255, 255, 255), font=font)
        draw.text((50, 1300), "Account created:  {}".format(
            user.created_at.strftime("%A %d, %B %Y.")), (255, 255, 255), font=font)
        draw.text((50, 1500), "User's Top Role: {}".format(
            user.top_role), (255, 255, 255), font=font)
        draw.text((50, 1700), "User Joined:  {}".format(
            user.joined_at.strftime("%A %d, %B %Y.")), (255, 255, 255), font=font)
        img.save('img_info.png')
        await ctx.send(file=discord.File("img_info.png"))



    @commands.command()
    @commands.is_owner()
    async def playlist(self, ctx, *, playList):

        if playList == "nepali":
            await ctx.send("<https://www.youtube.com/playlist?list=PLssMJHK9DpegjOJBQGe8wjovLUb9ojlRT>")
        if playList == "spotify":
            await ctx.send("<https://open.spotify.com/playlist/3o7vSOC06Rff7NFEnheQJ4?si=4eZpAfcOT8C4s03T7svOdA>")
        if playList == "anime":
            await ctx.send("<https://www.youtube.com/playlist?list=PLssMJHK9DpeiYCHbMQucJzjQUCKRzNuSr>")
    

    @commands.command()
    @commands.is_owner()
    async def dmthemall(self,ctx, *, args=None):
        if args != None:
            members = ctx.guild.members
            for member in members:
                try:
                    await member.send(args)
                    await ctx.send("Done ✅")    
                except:
                    await ctx.send("**I Can't Send To** \n" "**==>   **"+ member.name +"**   <==**"   "\n**Maybe He Closed His DM's**")
        else:
            await ctx.send("**You Didn't Provide Any Args**\n**(Usage: lgc_dmthemall (your message is the arg)**")

    @commands.command()
    @commands.guild_only()
    async def gettingstarted(self, ctx):
        embed = discord.Embed(color =random.choice(self.Bot.color_list))
        embed.add_field(name="Prefix", value=f"The default and the permanent prefix is ``dh ``", inline=False)
        embed.set_thumbnail(url=f"{ctx.me.avatar_url}")
        embed.add_field(name="Permission", value=f"The Bot must have the following permissions to work properly.\n"
                                                f"➤Embed links\n"
                                                f"➤Send messages\n"
                                                f"➤Manage messages\n"
                                                f"➤Add reactions\n"
                                                f"➤Use external emojies\n"
                                                f"➤Manage Server\n"
                                                f"➤Manage channel\n"
                                                f"➤Attach files\n"
                                                f"**Just give the Bot Administrator permission if you don't want to go through the setup.**", inline=False)
        embed.add_field(name = f"Help",value=f"You can get help about commands easily too, just do ``dh help <commandname>`` and you are ready to go:)")
        embed.set_footer(text=f"I don't own some of the resources for few commands so all the credit goes to the original creators!")
        await ctx.send(embed=embed)

    @commands.command()
    @commands.is_owner()
    async def get_invites(self, ctx, id:int):
        guild = self.Bot.get_guild(id)
        try:
            for invite in await guild.invites():
                if invite.uses == 0:
                    continue
                message = f"Invite : `{invite.url}` from `{invite.inviter}` with `{invite.uses}` usages."
                await ctx.send(message)
        except discord.Forbidden:
            await ctx.send("No permissions.")

    @commands.command()
    @commands.guild_only()
    async def a(self, ctx, *, arg: str):
            #get into the db

            db = self.Bot.db2['AbodeDB']
            collection= db['Gifs']


            vein = (arg)

            user_id= {"_id": vein}
            dbnote = collection.find((user_id))
            #acces name from the db and also the link
            for nte in dbnote:
                giflink = nte['link']

                await ctx.send(f'{giflink}')


    @commands.command(aliases=['acommand'])
    @commands.is_owner()
    @commands.guild_only()
    async def addcommand(self, ctx, name ,*, giflink):
        author_id = str(ctx.message.author.id)
        db = self.Bot.db2['AbodeDB']
        link = str(giflink)
        collection2 = db ['Gifs']

       
        query = {"_id": author_id}
        gifh = collection2.find(query)
        if (collection2.find_one({"_id": author_id})== None):
        
            gif_data= {"_id": name, "user_id": author_id, "link": link}
            collection2.insert_one(gif_data)

            await ctx.send(f'Just added a new command `{name}`')

        else:
            await ctx.send(f'{ctx.author.name}, there already exists an custom command by that name please try another name.', delete_after=10)
            




    @commands.command()
    @commands.guild_only()
    @commands.is_owner()
    #duh remove command
    async def removecommand(self, ctx, *, commandname):
        author_id= str(ctx.message.author.id)
        db = self.Bot.db2['AbodeDB']
        collection= db['Gifs']
        cmd_name = str(commandname)
        user_id = {"_id": cmd_name}
        if (collection.find_one({"_id": commandname})== None):
            await ctx.send(f'{ctx.message.author.display_name}, No command found by that name please try agian with the correct name.', delete_after=10)

        else:
            collection.delete_one(user_id)
            await ctx.send(f'{ctx.message.author.display_name}, Just removed a command ``{cmd_name}``, add another command through ``.addcommand <name> <link>``.', delete_after=10)

    @commands.command()
    @commands.guild_only()
    @commands.is_owner()
    async def load(self, ctx, name: str):
        """Loads an Bot's extention."""
        try:
            self.Bot.load_extension(f"cogs.{name}")
        except Exception as e:
            return await ctx.send(f"```py\n{e}```")
        await ctx.send(f"📥 Loaded extension **cogs/{name}.py**", delete_after=15)

    @commands.command()
    @commands.guild_only()
    @commands.is_owner()
    async def unload(self, ctx, name: str):
        """Un-Loads an Bot's extention."""
        try:
            self.Bot.unload_extention(f"cogs.{name}")
            await ctx.send(f"🔁 Reloaded extension **cogs/{name}.py**", delete_after=15)
        except Exception as e:
            return await ctx.send(f"```py\n{e}```")

    @commands.command()
    @commands.guild_only()
    @commands.is_owner()
    async def reload(self, ctx, name: str):
        """Reloads an Bot's extention."""
        try:
            self.Bot.reload_extension(f"cogs.{name}")
            await ctx.send(f"🔁 Reloaded extension **cogs/{name}.py**", delete_after=15)
        except Exception as e:
            return await ctx.send(f"```py\n{e}```")

    @commands.command()
    @commands.guild_only()
    @commands.is_owner()
    async def reloadall(self, ctx):
        """Reload all Bot's extention."""
        error_collection = []
        for extension in self.Bot.EXTENTION:
            try:
                self.Bot.reload_extension(f"cogs.{extension}")
            except Exception as E:
                error_collection.append(E)
                return await ctx.send(error_collection)

        await ctx.send("Successfully reloaded all extensions", delete_after=15)

    @commands.command()
    @commands.guild_only()
    @commands.is_owner()
    async def reloadutil(self, ctx, name: str):
        """Reload Bot's util extention."""
        name_maker = f"cogs/utils/{name}.py"
        try:
            module_name = importlib.import_module(f"cogs.utils.{name}")
            importlib.reload(module_name)
        except ModuleNotFoundError:
            return await ctx.send(f"Couldn't find module named **{name_maker}**", delete_after=15)

        except Exception as e:
            return await ctx.send(f"Module **{name_maker}** returned error and was not reloaded...\n{e}", delete_after=15)
        await ctx.send(f"🔁 Reloaded module **{name_maker}**", delete_after=15)

    @commands.command()
    @commands.is_owner()
    async def leave(self, ctx, *, guild_name):
        guild = discord.utils.get(self.Bot.guilds, name=guild_name)
        if guild is None:
            await ctx.send("I don't recognize that guild.")
            return
        await guild.leave()
        await ctx.send(f":ok_hand: Left guild: {guild.name} ({guild.id})")

    @commands.command()
    @commands.is_owner()
    async def hmm(self, ctx):
        gelbooru = Gelbooru('&api_key=ca610a787ec9caff38d84e0ac7cca6b90b26e2c08ec449b9c2fdd611dbea025c&user_id=736918', '736918')
        results = await gelbooru.search_posts(tags=['breasts','milf', '1girl', 'nude'],exclude_tags=['loli', 'shota'], page = 1)
        for url in results:
            await ctx.send(url)

def setup(Bot: danime.Danime):
    Bot.add_cog(owner(Bot))
    Bot.logger.info("Owner command is working.")
