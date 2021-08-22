import discord
from discord import channel
from discord.ext import commands, tasks
from discord.ext.commands import clean_content
from discord.ext.tasks import loop
import traceback
import collections
import datetime
from random import choice, randint
from disputils import BotEmbedPaginator,BotMultipleChoice
import time
from ago import human
import pymongo
from pymongo import MongoClient
import random
from random import choice, randint
from core import danime
import asyncio
from typing import Union



guild = 757098499836739594
color = 0xa100f2

class vein2(commands.Cog, name= "fun"):
    def __init__(self, Bot: danime.Danime):
        self.Bot = Bot
        


    @commands.command(aliases=['Hi', 'Namaste'], description=f'Get greetings from over 60 languages.')
    @commands.guild_only()
    async def hello(self,ctx):
        '''Nothing special just some greetings'''
        greetings = ['Hello', 'Hiya', 'nĭ hăo', 'Namaste', 'Konichiwa', 'Zdravstvuyte', 'Bonjour', 'Guten tag',
                     'Anyoung haseyo', 'Asalaam alaikum', 'Goddag', 'Selamat siang','hola', 'marhabaan  ', 'hyālō',
                     'Sata srī akāla', 'Nggoleki', 'Vandanalu', '   Xin chào', 'Namaskār', 'Vaṇakkam', 'Salām', 'Merhaba', 'Ciao'
                     , 'Sà-wàt-dii', 'Kaixo', 'Cześć’', 'Namaskāra', 'Prannam', 'Kamusta', 'Hallo', 'Yasou', 'Hej', 'oi', 'Wazza', 'kem cho',
                     'Hai', 'doki-doki', 'meow meow ', 'Lí-hó', 'Vitaju' , 'Bok', 'Hej', 'Moi', 'Sveika /Sveiks ', 'God dag',
                     'Moïen ', 'Vitayu ', 'Aloha ', 'Wassup', 'Howdy!']
        reply = random.choice(greetings)
        await ctx.send(f'{reply}, {ctx.message.author.mention} How is it going for you? No need to ask me, but I am mostly good.')



    @commands.command(description='Show Danime\'s ping.')
    @commands.guild_only()
    async def ping (self, ctx):
        # yay ping 

            latency = round(self.Bot.latency *1000)
            await ctx.send  ( f'{ctx.message.author.name}, Pong! `{latency}`ms')



    @commands.command(aliases=['av'])
    @commands.guild_only()
    async def avatar(self, ctx,*, user: discord.Member=None):
        # user as the mention
        if not user:
            user = ctx.author
            # self-explainatory
        embed = discord.Embed( title=f"{user.name}'s avatar",color=self.Bot.color)
        embed.description = f'[PNG]({user.avatar_url_as(format="png")}) | [JPEG]({user.avatar_url_as(format="jpeg")}) | [WEBP]({user.avatar_url_as(format="webp")})'
        embed.set_image(url=str(user.avatar_url_as(format='png')))
        embed.set_footer(text=f'Requested by {ctx.author.name}')
        # Nitro users :Eyes:
        if user.is_avatar_animated():
            embed.description += f' | [GIF]({user.avatar_url_as(format="gif")})'
            embed.set_image(url=str(user.avatar_url_as(format='gif')))

        return await ctx.send(embed=embed)




    @commands.command(aliases=['whois', 'ui'], description='To see information of a user.')
    @commands.guild_only()
    async def userinfo(self,ctx, member: discord.Member=None):

        member = member or ctx.author
        a = 0
        if a == 0:

            uroles = []
            for role in member.roles[1:]:
                if role.is_default():
                    continue
                uroles.append(role.mention)

                uroles.reverse()
            timestamp = 'ㅤ'
            time = member.created_at
            time1= member.joined_at
            if member.status == discord.Status.online:
                status= '<:online:769826555073003521>'
            elif member.status == discord.Status.idle:
                status= '<:idle:769826555479588864>'
            elif member.status== discord.Status.dnd:
                status = '<:dnd:769826555865989153>'
            else:
                status = '<:offline:769826555643691041>'
            if member.activity == None:
                activity = 'None'
            else:
                activity = member.activities[-1].name
                try:
                    timestamp = member.activities[0].details
                except:
                    timestamp ='ㅤ'
            embed=discord.Embed(color=color, timestamp=ctx.message.created_at, type="rich")
            embed.set_thumbnail(url= f"{member.avatar_url}")
            embed.set_author(name=f"{ctx.author.name}'s information",icon_url=f'{ctx.me.avatar_url}')
            embed.add_field(name="__General information__",value=f'**Nickname :** {member.display_name}\n'
                                                            f'**ID :** {member.id}\n'
                                                            f'**Account created :** {human(time, 4)}\n'
                                                            f'**Server joined :** {human(time1, 3)}\n'
                                                            ,inline=False)
            embed.add_field(name="__Role info__", value= f'**Highest role :** {member.top_role.mention}\n'
                                                        f'**Color** : {member.color}\n'
                                                        f'**Role(s) :** {", ".join(uroles)}\n'
                                               , inline=False)

            embed.add_field(name="__Presence__", value =f'**Status : ** {status}\n'
                                                        f'**Activity : ** {activity}  \nㅤㅤㅤㅤ{timestamp}')
            embed.set_footer(text=f"Requested by {ctx.author.name}",  icon_url=ctx.author.avatar_url)
            await ctx.send(embed=embed)
            return








    @commands.command(aliases= ['8ball', 'question'], description='Play 8ball game with Dhentai.')
    async def _8ball (self,ctx, *, question ):
        # normal 8ball command, it's fun 
        responses = [' It is certain.',
                    'It is decidedly so.',
                    ' Without a doubt.',
                    'Yes – definitely.',
                    'You may rely on it.',
                    'As I see it, yes.',
                    'Most likely.',
                    'Outlook good.',
                    'Yes.',
                    'Sings point to yes.',
                    'I know this is off topic but, master Vein is the best.',
                    'Reply hazy, try again.',
                    'Ask again later.',
                    'Better not tell you now.',
                    'Cannot predict now.',
                    'concentrate and ask again.',
                    'Donot count on it.',
                    'My reply is no.',
                    'My sources say no.',
                    'Outlook not so good.', 
                    'Very doubtful.']
        await ctx.send (f'{ctx.message.author.name}, **{random.choice(responses)}**')







    @commands.command(aliases=['wel'], description='To welcome your new firends.')
    @commands.guild_only()
    async def welcome(self,ctx):
        # gotta welcome the new guys
        await ctx.send(f'<:Cuppedfist:769143163414773760> Welcome to {ctx.guild.name}, enjoy your stay here!')

    @commands.command(aliases=['servercount','membercount'], description='Count the total number of users on the server.')
    @commands.guild_only()
    async def members(self,ctx):
        # get the total no of members of a server
        embed=discord.Embed(color=0x529dff)
        embed.add_field(name="Total members", value=f"{ctx.guild.member_count}", inline=False)
        embed.timestamp = datetime.datetime.utcnow()
        await ctx.send(embed=embed)

    @commands.command(aliases=['si'], description='To get the server information.')
    @commands.guild_only()
    # a cool server info command gets most of the basic things you would need to know about a server :)
    async def serverinfo(self, ctx):


        if ctx.channel.id ==757108786497585172:
            return

        guild= ctx.guild
        emojis = str(len(guild.emojis))

        channels = str(len(guild.channels))
        roles= str(len(guild.roles))
        time= ctx.guild.created_at.strftime("%a, %#d %B %Y, %I:%M %p ")
        voice= str(len(guild.voice_channels))
        text= str(len(guild.text_channels))
        statuses = collections.Counter([member.status for member in guild.members])

        online = statuses[discord.Status.online]
        idel = statuses[discord.Status.idle]
        dnd = statuses[discord.Status.dnd]
        offline= statuses[discord.Status.offline]

        embed= discord.Embed(
                                timestamp= ctx.message.created_at, color=color )

        embed.set_thumbnail(url=ctx.guild.icon_url)
        embed.set_author(name=f"Information for  {ctx.guild.name}")
        embed.add_field(name="__General information__\n", value= f'**Server name : ** {guild.name}\n'
                                                               f'**Server region : ** {guild.region}\n'
                                                               f'**Server ID : ** {guild.id}\n'
                                                               f'**Created at : ** {time}\n'
                                                               f'**Verification level : ** {guild.verification_level} \n'
                                                               f'**Server owner : ** {guild.owner.name} \n'
                                                               , inline=False)


        embed.add_field(name="\n\n\n__Statistics__", value= f'**Member count : ** {ctx.guild.member_count}\n'
                                                 f'**Role count : ** {roles} \n'
                                                 f'**Channel count : ** {channels}\n'
                                                 f'**Text channels :** {text}\n'
                                                 f'**Voice channels :** {voice}\n'
                                                 f'**Emoji count : ** {emojis}\n'
                                                 f'**Server boosts : ** {guild.premium_subscription_count}\n')

        embed.add_field(name="__Activity__", value= f'Online : {online}\n'
                                                    f'Idle : {idel}\n'
                                                    f'DND : {dnd}\n'
                                                    f'offline : {offline}')


        embed.set_footer(text=f"Requested by {ctx.author}",  icon_url=ctx.author.avatar_url)
        await ctx.send(embed=embed)


    # @serverinfo.error
    # # an example of an error hander for you :)
    # async def command_name_here_error(self,ctx, e):
    #     tb = '\n'.join(traceback.format_exception(type(e), e, e.__traceback__))
    #     await ctx.send(tb[:2000])


    @commands.command()
    async def enlargepp(self, ctx):
        return await ctx.send(f"Enlarged your pp by {random.randint(1, 100)}% <:lipbite:858395166250631168>")

    @commands.command()
    @commands.guild_only()
    async def enlarge(self, ctx, emoji: Union[discord.Emoji, discord.PartialEmoji]):
        if emoji == None:
            return await ctx.send(":_: add a emoji will you")    
        if emoji != None:
            await ctx.send(emoji.url)


    @commands.command(aliases=['serverinvite', 'support'], description='Get Dhentai\'s invite link.')
    async def invite(self,ctx):
        em= discord.Embed()
        em.description= f"You can invite the bot from [here]({self.Bot.invite}) or join the [support server]({self.Bot.support})"
        await ctx.send(embed= em)



    @commands.command()
    @commands.has_permissions(manage_messages=True)
    @commands.guild_only()
    # echo hehe boi    
    async def echo(self, ctx,*, arg):
        embed = discord.Embed(color=color , timestamp=ctx.message.created_at)
        embed.set_author(name=f'{arg}')
        embed.set_footer(text=f'{ctx.author.name}')
        await ctx.send(embed=embed)




    @commands.command(aliases=['lennyface', "lerry"], description='Send a random lenny face.')
    @commands.guild_only()
    # sends a random lenny from my collection 

    async def lenny( self, ctx):
        lennys= ['( ͡° ͜ʖ ͡°)', 'ಠ_ಠ', '( ͡ʘ ͜ʖ ͡ʘ)', '(▀̿Ĺ̯▀̿ ̿)', '( ͡°( ͡° ͜ʖ( ͡° ͜ʖ ͡°)ʖ ͡°) ͡°)', '( ͡ᵔ ͜ʖ ͡ᵔ )',
                 '(╯ ͠° ͟ʖ ͡°)╯┻━┻', 'ᕙ(▀̿̿Ĺ̯̿̿▀̿ ̿) ᕗ', '(✿╹◡╹)', 'щ（ﾟДﾟщ） < "Dear god why‽ )', '(人◕ω◕)', '(*бωб)', 'ヽ(͡◕ ͜ʖ ͡◕)ﾉ',
                 '(⌐▀͡ ̯ʖ▀)︻̷┻̿═━一-', 'ᕕ(╯°□°)ᕗ' ]
        await ctx.send(random.choice(lennys))
        await ctx.message.delete()

    @commands.command(aliases=['coin'], description='Flip a coin.')
    @commands.guild_only()

    async def flip(self,ctx):
        # tails
        value=['Heads', 'Tails']
        await ctx.send (random.choice(value))

    @commands.command(description="Fetches the latest changelogs for you.")
    async def changelog(self,ctx):
        channel = self.Bot.get_channel(856616086325297172)
        async for message in channel.history(limit =1):
            message = message.content
        embed = discord.Embed(color =random.choice(self.Bot.color_list))
        embed.description = message[:2000]
        await ctx.send(embed=embed)
        




    @commands.command(description='Oh boy!, a meter that calculates love between two parties.')
    @commands.guild_only()
    @commands.cooldown(1, 15, commands.BucketType.user)
    # uwu sempai do you lowe mew??
    async def lovemeter(self, ctx, name1: clean_content, name2: clean_content ):
        # clean_content is a handy thing you may need it :)
        percentage = random.randint(0, 100)

        if 0 <= percentage <= 10:
            result= ['Friendzone',
                     'You sure it was love-metre not friend-metre ',
                     'Dude that is insultingly low.]',
                     'Ahh the classic ``one sided love``',
                     'Just friends?',
                     'Is my metre off today? Can not pick any numbers']

        elif 10<= percentage <= 30:
            result=['Huh, just started dating?',
                     'I guess friendzone never ends',
                     'Best-friend zone?',
                     'My metre picked something up']

        elif 30 <= percentage <=50:
            result=['Still one sided, next time bud',
                     'There is still alot room for love',
                     'I mean it is a good start',
                     'There is potential']


        elif 50<= percentage <= 70:
            result= ['I sense love here',
                     'Oh... love birds?',
                     'Love is in the air',
                     'My metre picked something big',
                     'There is still a long road ahead, stay strong :D',
                     'I mean acceptable']

        elif 70<= percentage <=90:
            result= ['Just got wed?',
                     'Very good relationship',
                     'I do not talk much with love birds',
                     'My metre says it is looking good ',
                     'Just steps below the perfect match']

        elif 90<= percentage <=100:
            result= ['Yoo dude that iss real love',
                     'Romeo and Juliet?',
                     'My metre nearly exploded',
                     'Adam and Eve?',
                     'Match made in heavens']


        if percentage <= 33:
            shipColor = 0x000000
        elif 33 < percentage < 66:
            shipColor = 0xe3ff00
        else:
            shipColor = 0xee66ee

            # ik ik my gif taste is the best no need to appriciate me 
        if percentage <= 10:
            gif =  "https://media.tenor.com/images/8eb3ea6f8b8e05115a37df84ba03144a/tenor.gif"
        if 10 < percentage <=30:
            gif= "https://media.tenor.com/images/d9f4ebad1365272d2605a1a5151d501a/tenor.gif"
        if 30 < percentage <=50:
            gif = "https://media.tenor.com/images/12414d69b8a99bd6dc19275363e17554/tenor.gif"
        if 50 <percentage <= 70:
            gif = "https://64.media.tumblr.com/09efd576d1e31d6dbf2a66eaa07ef6af/tumblr_n52l5bmodz1tt23n5o1_500.gif"
        if 70 < percentage <= 100:
            gif = "https://media.tenor.com/images/d85ef0ba33daf46de0838eba3efe8d08/tenor.gif"


        final_result= random.choice(result)

        embed= discord.Embed(color=shipColor,
                             title= f"Love metre of {name1} and {name2}")
        embed.set_thumbnail(url=f'{gif}')
        embed.add_field(name="Results:", value=f'{percentage}% ', inline=True)

        embed.add_field(name="Personal opinion :", value=f'{final_result}', inline=False)

        embed.set_author(name="Dhentai")
        embed.set_footer(text=f'Requested by {ctx.author}', icon_url=ctx.author.avatar_url)
        await ctx.send(embed=embed)




    @commands.command(description='Send .F to pay respects. ')
    @commands.guild_only()
    async def f(self, ctx):
        # f in the chats bois 
        await ctx.send(f'{ctx.author.display_name} paid their respects.')


    @commands.command(description='Send an embeded message.')
    @commands.guild_only()
    @commands.has_permissions(manage_messages=True)
    @commands.cooldown(1, 3, commands.BucketType.user)
    async def embed(self, ctx, *, string):
        # a quick embed thingy

        embed=discord.Embed(description=f'{string}', color=ctx.author.color)
        await ctx.send(embed=embed)






    @commands.command(description='Advanced ping command for the nerds out there.')
    async def pingadv(self, ctx):
        # nerdy stufss here
        msg = await ctx.send("Pinging bot\'s latency...")
        times = []
        counter=0
        embed = discord.Embed(title="More information:", description="Pinged 3 times and calculated the average.", color = color)


        for _ in range(3):
            counter += 1
            start = time.perf_counter()
            await msg.edit(content=f"Pinging... {counter}/3")
            end = time.perf_counter()
            speed = round((end - start) * 1000)
            times.append(speed)
            embed.add_field(name=f"Ping {counter}:", value=f"{speed}ms", inline=True)

        embed.set_author(name="Pong!", icon_url= ctx.author.avatar_url)
        embed.add_field(name="Bot latency", value=f"{round(self.Bot.latency * 1000)}ms", inline=True)
        embed.add_field(name="Average speed", value=f"{round((round(sum(times)) + round(self.Bot.latency * 1000))/4)}ms")
        embed.set_thumbnail(url= ctx.guild.icon_url)
        embed.set_footer(text=f"Estimated total time elapsed: {round(sum(times))}ms")
        await msg.edit(content=f":ping_pong: {round((round(sum(times)) + round(self.Bot.latency * 1000))/4)}ms", embed=embed)




    @commands.command(aliases = ["calculator"],description="Calculate BODMAS here :)")
    @commands.guild_only()
    @commands.cooldown(1, 15 ,commands.BucketType.user)
    # ever doubt yourself then clac your thoughts out 
    # this uses the in built eval of python to do things like DMAS
    async def calc(self, ctx, *, query : str = None):
        if query is None:
            await ctx.send("What to evaluate?")
        else:
            allowed = set('0123456789+-*/()')
            clean = ''.join(char for char in query if char in allowed)
            try:
                await ctx.send(f'``{query}`` ``=`` ``{eval(clean)}\n``')
            except Exception:
                await ctx.send('Please a write valid equation.')


    @commands.command(aliases=["Code"])
    @commands.guild_only()
    # lemme promote my repo will you?
    async def github(self,ctx,dir_=None ,file= None):
        if file ==None and dir_ ==None:
            await ctx.send(f"<:github:768713047501963294> <{self.Bot.github}>\nNote: This is my parent directory which has many other features.")
        else:
            await ctx.send(f"https://github.com/Vein05/Dhentai/blob/main/{dir_}/{file}.py")



    @commands.command(aliases=["dice"])
    @commands.guild_only()
    # ludo
    async def roll(self, ctx):
        responses = ['<:one:776678357567668225>',
                        '<:two:776678358041755688>',
                        '<:three:776678358380838912>',
                        '<:four:776678357861138452>',
                        '<:five:776678357068283905>',
                        '<:six:776678357478670357>']
        await ctx.send (f"The dice rolls to {random.choice(responses)}")


    @commands.command()
    @commands.guild_only()
    # 69% bot boi
    async def howbot(self, ctx, member: discord.Member= None):
        x = random.randint(0, 100)
        if member!= None and not member.bot:
            
            await ctx.send(f"{member.name} is ``{x}%`` <:bot:773959362120646706>.")
        if member!= None and member.bot:
            
            await ctx.send(f"Yo real bot!")           
        
        else:
            await ctx.send(f"{ctx.author.name} is ``{x}%`` <:bot:773959362120646706>.")





def setup (Bot: danime.Danime) -> None:
     Bot.add_cog(vein2(Bot))
     Bot.logger.info("Fun cog is working.")
