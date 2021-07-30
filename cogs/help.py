import discord 
from discord.ext import commands 
from pygicord import Paginator
import datetime
import random
import psutil
from misc import emoji
import datetime
import sys
from core import danime

ban = 'https://cdn.discordapp.com/attachments/782161513825042462/793136610619293726/ban_and_unban.gif'
slowmode = 'https://cdn.discordapp.com/attachments/782161513825042462/793136512699072522/slowmode.gif'
role = 'https://cdn.discordapp.com/attachments/782161513825042462/793136557489127464/role.gif'
nickname = 'https://cdn.discordapp.com/attachments/782161513825042462/793136558529314876/nick.gif'
poll = 'https://cdn.discordapp.com/attachments/764393920381190144/793138667207262289/Poll.gif'


class vein9(commands.Cog, name='Help'):
    def __init__(self, Bot):
        self.Bot = Bot
        self.cmds_per_page = 10





    @commands.command(aliases=['commands', 'h'])
    @commands.guild_only()
    async def help(self, ctx, *, entity=None):
        check = ['1', '2', '2.5' , '3', '4', '5']

        if entity == None:
            em =  discord.Embed(color = random.choice(self.Bot.color_list))
            em.description= f"Konichiwa {ctx.author.name}-sama, I'm **Danime**. The following embed lists out all of the major categories that I  can currently do. It also lists out common syntax for commands. Feel free to browse around the pages <a:wink:863703322115178546>.\n"
            em.add_field(name="Help usage", value =f"`dh help [commmand name]`  to get help on specific command.\n"
                                                    "`dh help [category]` to get help about a certian category from below.")
            em.add_field(name="__Available categories__",
                value = f"{emoji.love} Anime : `dh help 1`\n"
                        f"{emoji.think} NSFW : `dh help 2`\n"
                        f"{emoji.yay} NSFW2 : `dh help 2.5` \n"
                        f"{emoji.approved}SFW : `dh help 3`\n"
                        f"{emoji.hmmm} Settings : `dh help 4`\n"
                        f"{emoji.gun} Handy/Usefull : `dh help 5`\n",
                inline = False
                )
            em.add_field(name = "[Policy]", value="See `dh ip` and `dh privacypolicy` before you use the bot.")
            await ctx.send(embed = em)
        elif  entity == "1" :

            em = discord.Embed(color = random.choice(self.Bot.color_list))
            em.description = "Anime related commands. Remove the <> during usage."
            # em.description =f"The embed is in the order of : \nCommandName Synatx Description"
            em.add_field(name="Anime", value=f"Description : You can search anime. \nUasge : `dh anime <your anime name>`", inline=False)
            em.add_field(name="Doujin", value=f"Description : You can search, read, download doujin from nhentai.net. \nUsage : `dh doujin <nhentai_id>`")
            em.add_field(name=f"Manga", value=f"Description: You can search any manga. \nUsage: `dh manga <your manga name>`", inline= False)
            em.add_field(name = f"Character", value = "You can search most of the characters. \nUsage : `dh character <your favourite character>`")
            em.add_field(name=f"Sauce", value="It's a given but `dh help sauce` for more info.", inline=False)
            await ctx.send(embed = em)

        elif entity == "2":
            if not ctx.channel.is_nsfw():
                return await ctx.send("Use this command in a nsfw channel please.")
            em = discord.Embed(color = random.choice(self.Bot.color_list))                                            
            em.description = f"Lists all the nsfw commands, each tag mentioned is a command. Do note only 80% of the tags are from DanimeAPI, I'm migrating every tag soon.\nFor example : `dh yuri`"
            # em1.add_field(name=f"__nsfw command usuage__", value=f"dh `command_name`", inline=False)
            em.add_field(name=f"[Commands/Tags]", value =f"**You can pass in the amount of pictures like, `dh nsfw 10`**\n `nsfw`, `blowjob`, `anal`, `ass`, `milf` , `neko`, `oppai`, `glasses`, `panties`, `elves`, `bdsm`, `pussy`, `solo`, `cum`, `uniform`, `public`, `thighs`, `creampie`, `cuckold`, `gangbang`, `boobjob`, `erofeet`, `pantyhose` `stockings`, `bunnygirl`,`hairy`,`femdom`, `fitness`", inline=False)
            em.add_field(name=f"[Specific Character]", value=f"`zerotwo`, `rem` , `tsunade`", inline=False)
            em.add_field(name= f"[Specific Anime/Source]", value=f"`konosuba`, `dragonball`, `naruto`, `fate`, `quintuplets`, `league`")
            em.set_footer(text=f"Use [dh whatis nsfw] to get detail to know what is expected under nsfw commands.")

            em1 = discord.Embed()
            em1.add_field(name="[Autonsfw]", value=f"Can be used to set up a channel where the bot will send a nsfw pic every given minute\n\n"
                                                    "**enable** \n  dh `autonsfw enable <tag> <time>` Enables the feature, `<tag>` and `<time>` are optional, time will be in minutes(1-30) and tags are all the commands/tags listed above. Example `dh autonsfw enable stockings 5`\n\n"
                                                    "**disable**\n  dh `autonsfw disable`   Disables the feature for the channel.\n", inline=False)
            
            
            em1.set_footer(text=f"Join the support server if you want to contribute or just enjoy some pictures.")
            

            embeds = [em, em1]
            paginator = Paginator(pages=embeds, timeout=90.0)
            await paginator.start(ctx)
        elif entity == "2.5":
            if not ctx.channel.is_nsfw():
                return await ctx.send("Use this command in a nsfw channel please.")
            em = discord.Embed(color = random.choice(self.Bot.color_list))
            em.description= f"Lists the next page of nsfw section. Needs nsfw toggled turned on, `dh nsfwtoggle enable` if you're an admin."
            em.add_field(name=f"[Booru/Sites]", value = f"`danbooru`, `gelbooru`, `realbooru`, `yandere`, `konachan`, `realbooru`, `safebooru`, `e621`, `rule34`", inline= False)
            em.add_field(name = f"[Booru Usage]", value=f"`dh Site tags amount`"
                )
            em.add_field(name = "Example", value =f"`dh yandere 1girl 10`")
            em.set_footer(text = "The images from this commands are not monitored by the bot, please be sure before you enable them.")
            await ctx.send(embed =em)

        elif entity == "3":
            em = discord.Embed(color = random.choice(self.Bot.color_list))
            em.description = f"The following contains SFW commands of the bot. "
            em.add_field(name = "[Specific/Tags]", value=f"`sfwneko`,`sfwoppai` ,`sfwswimsuit`,`waifu`, `megumin`, `animememes` , `animefood`, ", inline=False)
            em.add_field(name=f"[Action]", value=
                                       f"`sex`, `tickle`, `baka`, `lewd`, `bully`,`cuddle`, `kiss`, `smug`, `bonk`, `slap`,`kill` ,`cringe`, `blush`, `headpat`, `facepalm`, `wink` ,`hug`" )            
            await ctx.send(embed=em)     

        elif entity == "4":
            em = discord.Embed(color = random.choice(self.Bot.color_list))
            em.add_field(name=f"__Configuration commands__ | Admins only|", value = f"disablecommand  : dh disablecommand `commandname`\n"
                                        " enablecommand  : dh enablecommand `commandname`\n" 
                                        "listdisabledcommands : Lists the currently disabled commands ^ ^", inline=False)
            await ctx.send(embed=em)
        elif entity =="5":
            em = discord.Embed(color = random.choice(self.Bot.color_list))
            em.add_field(name=f"__Handy commands__", value=f"`reddit`,`addemoji`, `welcome`, `ping`, `invite`, `lenny`, `f`, `hi`, `flip`, `calc`, `owofy`, `wallpaper`, `enlarge`, `topic`, `stats`, `userinfo`, `serverinfo`, `privacypolicy`, `imagepolicy`", inline=False)
            em.add_field(name=f"__Fact commands__", value=f"`dogfact`, `catfact`, `pandafact`, `numberfact`, `yearfact`, `aquote`")
            em.set_footer(text="This category has conditional nsfw commands, meaning sfw or nsfw depends on the condition.")
            await ctx.send(embed=em)
        
        elif not entity in check:
            command = self.Bot.get_command(entity)
            if command:
                await self.send_command_help(ctx, command)

            else:
                await ctx.send(f"Couldn't find {entity}.")

    async def send_command_help(self, ctx, command):
        commandDescription = command.description
        if commandDescription == "":
            commandDescription = "A nice command."
        commandName : str = f"{command.name}"
        
        commandUsage = command.usage
        if command.usage == None: commandUsage = "Not given"
        commandAliase = ", ".join(command.aliases) or f"{command.name}"
        embed = discord.Embed(color = random.choice(self.Bot.color_list))
        embed.set_author(name =f"Extra information on the command {commandName}")
        # embed.description = f"🗒️Description : {command.description} "
        embed.add_field(name = f"<:notes:856427200555384842> Description", value=f"`{commandDescription}`", inline =False)
        embed.add_field(name=f"Example", value = f"`{commandUsage}`")
        embed.add_field(name = f"Aliases", value= f"`{commandAliase}`", inline = False)
        # embed.add_field(name = f"Cooldown" , value=f"{command.cooldown_after_parsing}")
        embed.set_footer(text = "Join the support server if you are facing issues.")
        await ctx.send(embed = embed)

    @commands.command()
    @commands.is_owner()
    async def rules(self, ctx):
        bullet = "‣"
        embed = discord.Embed()
        embed.add_field(name="Rules", 
            value = f"{bullet} No racism, racist slurs. They are not allowed.*\n"
            f"{bullet} No nsfw content in main chat.\n"
            f"{bullet} Use channels for their own sake.\n"
            f"{bullet} Don't leak personal information.*\n"
            f"{bullet} No server promoting, any other scam/ip grabber links.*\n"
            f"{bullet} Don't bother any staff members in dms unless there is a reason behind it.\n"
            f"{bullet} No spamming and flooding channels.\n"
            f"{bullet} Follow [Discord TOS](https://discord.com/terms).\n"
            f"{bullet} Get NSFW access from <#856616092251193404>, Don't bother staff.")
        embed.set_footer(text="Rules ending with * may result ban.")
        await ctx.send(embed=embed)


    @commands.command(aliases=['ip'])
    @commands.guild_only()
    async def imagepolicy(self, ctx):
        bullet = "‣"
        embed = discord.Embed(timestamp = datetime.datetime.fromisoformat("2021-07-11 16:16:21.513794"))
        embed.add_field(name=f"[Intro]", value="DAnime bot isn't managed by some professionals so there will be many things that may not be applied.", inline=False)
        embed.add_field(name=f"[Information]", value=f"{bullet} The bot doesn't own any of the used image resources.\n"
                                                    f"{bullet} Images are handpicked from trusted users or by the creator myself.\n"
                                                    f"{bullet} If bad images are passed through, you can report that on the [support server]({self.Bot.support}).\n"
                                                    f"{bullet} If you want to contribute to the bot, you can do so by sending the images on the support server.\n"
                                                    f"{bullet} I try to not include \"some\" tags on images but i'm still a human, I can't provide 100% reassureance.\n"
                                                    f"{bullet} If you have turned on nsfw toggle then the bot shall not be responsive for the images sent.\n", inline=False)
        embed.add_field(name = f"[प्रतिलिपि अधिकार ऐन, २०५९ and DMCA]", value=f"Since the bot is of origin Nepal, the primary policy shall be of [The Copyright Act, 2002](https://en.wikipedia.org/wiki/Copyright_law_of_Nepal). That doesn't mean [DMCA](https://en.wikipedia.org/wiki/Digital_Millennium_Copyright_Act) claims are to be ignored. You can report your claims in the [support server]({self.Bot.support}). Your claim shall be resloved within a few business days.", inline=False)
        embed.add_field(name=f"[Personal Opinion]", value=f"Many are upset about some \"l*li\" pics passing through and yea I too am angry for the fact, I try to pass images that are under discord TOS, still i'm just one person. If you do find one, please take your time and report it, I will remove it asap.")
        embed.set_footer(text="Last updated")
        await ctx.send(embed=embed)
        if self.Bot.DEFAULT_PREFIX == "&":
            message = await self.Bot.get_channel(856616084040056873).fetch_message(863714401902002196)
            await message.edit(embed=embed)

    @commands.command(aliases=['pp'])
    async def privacypolicy(self, ctx):
        embed= discord.Embed(timestamp = datetime.datetime.fromisoformat("2021-07-11 14:16:21.513794"))
        embed.add_field(name = f"[Intro]", value=f"Danime bot only saves the data collected in configuration. Data is auto-deleted if the configurations are turned off. We have no interested in storing data."
            , inline=False)
        embed.add_field(name = f"[Logs]", value = f"Commands logs are kept, that only have the user id and the command used, with the args. This data can only be viewd by the developers and is only used to ban \"some\" users.", inline=False)
        embed.add_field(name = f"[Data Removal]", value=f"Simple join the support server and DM any of the developers, data shall be deleted NO QUESTIONS ASKED.", inline=False)
        embed.add_field(name = f"[Public Data]", value="Danime will not sell, trade, or rent Users personal identification to anyone, data to be public may only include collective data such as most searched terms, etc. Any data leading to an individual won't be known to public.", inline=False)
        embed.add_field(name = f"[Acceptance]", value="Users are to read this before using the bot, if you don't comply with our policy, you are free to not use the bot and if you do use Danime that signifies you agree to our terms.", inline=False)
        embed.add_field(name = f"[Contact]", value=f"If one has any questions regarding the policy or the bot itself, feel free to join the [support server]({self.Bot.support}).")
        embed.set_footer(text="Last updated")
        await ctx.send(embed=embed)

    @commands.command()
    async def website(self, ctx):
        embed = discord.Embed(description=f"You can find our website [here]({self.Bot.website_link}).")
        await ctx.send(embed=embed)
        
    @commands.command(aliases=['botinfo'])
    @commands.guild_only()
    async def stats(self, ctx):
        now = datetime.datetime.utcnow()
        elapsed = now - self.Bot.starttime
        seconds = elapsed.seconds
        minutes, seconds = divmod(seconds, 60)
        hours, minutes = divmod(minutes, 60)   

        users = 0
        for guild in self.Bot.guilds:
            try:
                users += guild.member_count
            except:
                pass

        guilds = str(len(self.Bot.guilds))

        invite_link = f"[Invite link]({self.Bot.invite})"
        vote = "Soon"
        
        cpu = str(psutil.cpu_percent())
        boot_time = str(psutil.boot_time() / 100000000)
        boot_time_round = boot_time[:4]

        owner = self.Bot.get_user(427436602403323905)
        embed = discord.Embed(timestamp=self.Bot.starttime ,
            color=0x26fcff,
            description="```asciidoc\n"
                        +"Name: Danime\n"
                        +f"Bot Latency: {round(self.Bot.latency * 1000)}ms\n"
                        +f"Web Socket Latency: {round(self.Bot.latency * 1000, 2)}ms\n"
                        +f"Runtime: {elapsed.days} days, {hours} hours, {minutes} minutes and {seconds} seconds\n"
                        +"```"

            )
        embed.set_author(name=f"Danime's Information")
        embed.add_field(name=f"General ", inline=True, value=f"```asciidoc\nBoot Time: {boot_time_round}s\nUsers: {users}\nServer: {guilds}```\n")
        embed.add_field(name=f"Bot", inline=True, value=f"```asciidoc\nDiscord.py: {discord.__version__}\nPython: 3.8.7\nDanime: 1.4\n```")
        embed.add_field(name=f"System", inline=False, value=f"```asciidoc\nOS: {sys.platform}\nCPU Usage: {cpu}%\n```")
        embed.add_field(name=f"Creator", inline=False, value=f"```asciidoc\nUsername: {owner.name}#{owner.discriminator} [{owner.id}]```")
        embed.add_field(name=f"Links", inline=False, value=f'[Invite]({self.Bot.invite}) |  [Support Server]({self.Bot.support}) |  [Github]({self.Bot.github}) |  [Website]({self.Bot.website_link}) |  [Vote]({vote})')
        embed.set_footer(text=f"Last restart")

        await ctx.send(embed=embed)

def setup(Bot: danime.Danime) -> None: 
    Bot.add_cog(vein9(Bot))
    Bot.logger.info("Help cog is working.")
