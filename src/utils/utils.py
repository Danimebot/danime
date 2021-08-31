import discord
from discord.ext import commands
from discord.ext.buttons import Paginator
import re
import requests 
from bs4 import BeautifulSoup as soup1
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


def get_sauce(url, embed:bool=False):
    r = requests.get(url).content
    soup = soup1(r, "lxml")
    results = soup.find_all("div", {"class" : "result"})
    return_list = []
    for result in results:
        try:
            tables = result.find_all("table", {"class" : "resulttable"})
            for table in tables:
                img_url = table.find("div", {"class" : "resultimage"}).find("a").find("img")['src']
                similarity = table.find("div", {"class" : "resultmatchinfo"}).find("div", {"class" :"resultsimilarityinfo"}).text.strip()[:-1]
                sauce_urls_raw = table.find("div", {"class" : "resultmatchinfo"}).find("div", {"class" : "resultmiscinfo"}).find_all("a")
                sauce_urls = []
                title = table.find("div", {"class" : "resulttitle"}).text.strip()

                is_anime  = False
                is_manga = False
                for x in sauce_urls_raw:
                    if x['href']:
                        sauce_urls.append(x['href'])
                if not float(similarity) > 50:
                    continue
                sauce_dict = {}
                sauce_dict['thumbnail'] = img_url
                sauce_dict['similarity'] = similarity
                sauce_dict['title'] = title
                sauce_dict['sauce_urls'] = sauce_urls
                for key, x in enumerate(sauce_urls):
                    if x.startswith("https://anidb.net"):
                        is_anime = True
                        content_table = table.find("div", {"class" : "resultcontentcolumn"}).find_all("span", {"class" : "subtext"})
                        timestamp = content_table[2].text.strip()
                        episode = table.find("div", {"class" : "resulttitle"}).find("strong").text.strip()
                        sauce_dict['episode'] = episode
                        sauce_dict['timestamp'] = timestamp
                    if x.startswith("https://manga"):
                        is_manga = False
                        title = table.find("div", {"class" : "resulttitle"}).text.strip()
                        artist_info = table.find("div", {"class" : "resultcontentcolumn"}).text.strip()
                        sauce_dict['chapter'] = title[:-1]
                        sauce_dict['artist_info'] = artist_info
                    
                    sauce_dict['is_anime'] = is_anime
                    sauce_dict['is_manga'] = is_manga
                    return_list.append(sauce_dict)
        except:
            pass         
    if embed == False:
        return return_list
    else:
        embeds = []
        for sauce in return_list:
            embed = discord.Embed()
            embed.set_thumbnail(url = sauce['thumbnail'])
            embed.description = f"Sucessfully found closest image(`{sauce['title']}`) with the following information."
            embed.add_field(name="Similarity", value=sauce['similarity'])
            embed.add_field(name="Sauce(s)", value="\n".join(sauce['sauce_urls']), inline=False)

            if sauce['is_anime'] == True:
                embed.add_field(name="Episode", value=sauce['episode'], inline=False)
                embed.add_field(name="Timestamp", value=sauce['timestamp'], inline=False)
            if sauce['is_manga'] == True:
                embed.add_field(name="Chapter", value=sauce['chapter'], inline=False)
                embed.add_field(name="Artist Info", value=sauce['artist_info'], inline=False)

            embeds.append(embed)


        return embeds