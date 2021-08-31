import requests
from bs4 import BeautifulSoup as soup
import asyncio
from utils.utils import DanimeCommands
import discord
from discord.ext import commands
from reactionmenu import ButtonsMenu, ComponentsButton
from pygicord import Paginator, Config
import re
import random
from utils import checks

class premium_commands(commands.Cog):
    def __init__(self, Bot):
        self.Bot = Bot


    @DanimeCommands(premium=True, aliases=['readmanga'])
    @checks.is_premium_guild()
    async def read_manga(self, ctx, *, title):
        info = self.get_manga_info(title.lower())
        mangas = [*info]
        embeds = []
        for key, manga in enumerate(mangas):
            embed = discord.Embed(title=manga)
            embed.set_image(url = info[manga]['thumbnail'])
            embed.description = f"Index : `{key}` -> {manga} has {info[manga]['views']} views and has status {info[manga]['status']}."
            embed.set_footer(text="You can browse around the pages and type the index within 1 minutes to read that manga.")
            embeds.append(embed)
        menu = Paginator(pages = embeds , timeout=60)
        try:
            await menu.start(ctx=ctx)
        except ValueError:
            return await ctx.send("Hey it seems there are no results for your query.")
        try:
            res = await self.Bot.wait_for("message",timeout=60, check= lambda message: message.author == ctx.author )
            check = range(0, len(mangas))
            chapter = int(res.content)
            if chapter in check:
                user_choice = mangas[chapter]
                await ctx.send("Please type the chapter number and I will try to find it for you.")
                res =  await self.Bot.wait_for("message", timeout=60, check = lambda message: message.author == ctx.author)
                chapter = res.content
                url = info[user_choice]['link'] + f"-chap-{chapter}/"
                pages = self.get_manga_pages(url)
                if pages == "Unforseen error occured.":
                    return await ctx.send("Unforseen error occured. Please report it to the support server.")
                menu = ButtonsMenu(ctx, menu_type=ButtonsMenu.TypeEmbed, timeout=90, show_page_director=False)
                for url in pages:
                    em = discord.Embed()
                    em.set_image(url = url)
                    menu.add_page(em)
                buttons = [ComponentsButton(style=ComponentsButton.style.primary, label = '' ,emoji='⏪', custom_id=ComponentsButton.ID_GO_TO_FIRST_PAGE),
                    ComponentsButton(style=ComponentsButton.style.primary, label = '' ,emoji='◀️', custom_id=ComponentsButton.ID_PREVIOUS_PAGE),
                    ComponentsButton(style=ComponentsButton.style.primary, label = '' ,emoji='⏹️', custom_id=ComponentsButton.ID_END_SESSION),
                    ComponentsButton(style=ComponentsButton.style.primary, label = '' ,emoji='▶️', custom_id=ComponentsButton.ID_NEXT_PAGE),
                    ComponentsButton(style=ComponentsButton.style.primary, label = '' ,emoji='⏩', custom_id=ComponentsButton.ID_GO_TO_LAST_PAGE)
                ]
                for button in buttons:
                    menu.add_button(button)
                await menu.start()
        except asyncio.TimeoutError:
            return await ctx.send("Timed out!")

    def get_manga_pages(self, url):
        r = requests.get(url).text
        soup1 = soup(r, "lxml")
        chapter_content = soup1.find("div", {"class" :"chapter-content-inner text-center"}).find("center")
        images = []
        for img in chapter_content.find_all("img"):
            images.append(img['src'])
        if "/content/upload/coming-soon.jpg" not in images:
            return images
        else:
            return "Unforseen error occured."



    def get_manga_info(self, title):
        title = title.replace(" ", "+")
        url = f"{self.Bot.manga_website}?s={title}"
        r = requests.get(url).text
        soup1 = soup(r, "lxml")
        entries = soup1.find_all("div", {"class" : "entry"})
        return_dict = {}
        for key, entry in enumerate(entries):
            try:
                content = entry.find("div", {"class" : "content"})
                title_main = content.find("h3", {"class" : "name"})
                title_link = title_main.find("a")['href']
                title_link = title_link.replace("-1", "")
                title_name = title_main.text.strip()
                status = content.find("div", {"class" : "status"}).find_all("span")[1].text.strip()
                views = content.find("div", {"class" : "view"}).find_all("span")[1].text.strip()
                img = entry.find("a", {"class" : "thumb"}).find("img")['src']
                dict =  {"link" : title_link, "thumbnail" : img ,"status" : status, "views" : views}
                return_dict[title_name] = dict
            except AttributeError:
                continue
        return return_dict

    @DanimeCommands(premium=True, aliases=['readnovel'])
    @checks.is_premium_guild()
    async def read_novel(self, ctx, *, title):
        info = self.get_novel(title)
        novels = [*info]
        embeds = []
        for key, manga in enumerate(novels):
            embed = discord.Embed(title=manga)
            embed.set_image(url = info[manga]['thumbnail'])
            embed.set_author(name=f"{title} has {len(novels)} results.")
            embed.description = f"Index : `{key}` -> {manga} has status {info[manga]['status']}."
            embed.set_footer(text="You can browse around the pages and type the index within 1 minutes to read that manga.")
            embeds.append(embed)
        menu = Paginator(pages = embeds , timeout=60)
        try:
            await menu.start(ctx=ctx)
        except ValueError:
            return await ctx.send("Hey it seems there are no results for your query.")
        try:
            res = await self.Bot.wait_for("message",timeout=60, check= lambda message: message.author == ctx.author )
            check = range(0, len(novels))
            chapter = int(res.content)
            if chapter in check:
                novel = novels[chapter]
                await ctx.send("Please type the chapter number and I will try to find it for you.")
                res =  await self.Bot.wait_for("message", timeout=60, check = lambda message: message.author == ctx.author)
                chapter = res.content
                url = f"{info[novel]['link']}/chapter-{chapter}"
                novel_content = self.get_novel_content(url)
                n = 0
                b = 8
                embeds = []
                color = random.choice(self.Bot.color_list)
                while n <= len(novel_content['text']):
                    text = novel_content['text']
                    embed = discord.Embed(color=color)
                    embed.set_author(name=f"{novel} | {novel_content['title']}")
                    embed.description = "\n\n".join(text[n:b])
                    n = b
                    b = b + 8
                    embeds.append(embed)            
                menu = Paginator(pages = embeds , timeout=300, config=Config.PLAIN)
                await menu.start(ctx=ctx)
                
        except asyncio.TimeoutError:
            await ctx.send("Timed out.")

    @DanimeCommands(premium=True, aliase=['animedl'])
    @checks.is_premium_guild()
    async def anime_dl(self, ctx, query:str):
        query = (re.sub("[-,.]", " ", query))
        info = await self.Bog.get_anime(self, query)
        


    def get_novel(self, title):
        query = (re.sub("[ ,.]", "+", title))
        url = f"{self.Bot.novel_website}search?q={query}"
        r = requests.get(url).text
        soup1 = soup(r, "lxml")
        grid = soup1.find_all("div", {"class": "col-xs-4 col-sm-3 col-md-3"})
        return_dict = {}
        for g in grid:
            a = g.find("a")
            link = a['href']
            title = a['title']
            thumbnail = a.find("img")['src']
            status = g.find("div", {"class" :"caption"}).find("small").text.strip()
            return_dict[title] = {'link' : link, 'thumbnail' : thumbnail, 'status' : status}
        return return_dict
            
    def get_novel_content(self, url):
        r = requests.get(url).text
        soup1 = soup(r, "lxml")
        chapter_title = soup1.find("span", {"class": "chapter-text-detail"}).text.strip()
        chapter_text = soup1.find("div", {"class" :"chapter-content chapter-c"}).find_all("p")
        final = []
        for text_ in chapter_text:
            final.append(text_.text.strip())
        final.pop(0)
        final.append(f"**End Of Chapter** | [Danime]({self.Bot.invite})")
        return {"title" : chapter_title, "text" : final}
        
def setup (Bot):
    Bot.add_cog(premium_commands(Bot))
    print("Premium commands is working.")