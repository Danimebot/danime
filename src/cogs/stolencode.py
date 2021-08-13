import discord
from discord.ext import commands
import random
import requests
from core.danime import Danime

class stolen(commands.Cog, name="stolen"):
    def __init__(self, Bot):
       self.Bot = Bot
       self.after = ""

    @commands.command(aliases=["animemes"])
    @commands.guild_only()
    @commands.cooldown(1, 10, commands.BucketType.user)
    async def animememes(self, ctx: commands.Context):

	    no = random.randint(0, 1)
	    if no == 0:
	        def fetch_meme():
	            data = requests.get(
	                "https://www.reddit.com/r/goodanimemes.json",
	                params={"limit": 1, "after": self.after},
	                headers={"user-agent": "lhs-moe/rewrite"},
	            ).json()
	            self.after = data["data"]["after"]
	            return data["data"]["children"][0]["data"]

	        async with ctx.typing():
	            meme = fetch_meme()

	            count = 0
	            while (
	                meme["is_self"]
	                or meme["is_video"]
	                or meme["over_18"]
	                and (count := count + 1) <= 20
	            ):
	                meme = fetch_meme()

	            embed = discord.Embed(title=meme["title"], color = random.choice(self.Bot.color_list))
	            embed.set_footer(text=f"Requested by {ctx.author.name}")
	            embed.set_image(url=meme["url"])

	        await ctx.send(embed=embed)
	    if no == 1:
	    	url = "https://memes.blademaker.tv/api/animemes"
	    	data = requests.get(f"{url}").json()
	    	if data['nsfw'] != True:
	    		url = data['image']
	    		await self.waifu_embed(ctx=ctx, link =url, dl = url)


    async def waifu_embed(self, ctx, link, dl = None):
        embed = discord.Embed(color =random.choice(self.Bot.color_list))
        if dl != None:
            embed.description=f"[Link]({dl})"
        embed.set_footer(text=f"Requested by {ctx.author}")
        embed.set_image(url=f"{link}")
        await ctx.send(embed=embed)
        return

def setup (Bot: Danime):
	Bot.add_cog(stolen(Bot))
	Bot.logger.info("Stolen commands is working.")
