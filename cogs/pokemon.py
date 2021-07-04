
import discord
from discord.ext import commands

class pokemon(commands.Cog, name="pokemon"):
	def __init__(self, Bot):
		self.Bot = Bot

	@commands.command()
	@commands.cooldown(1,15, commands.BucketType.user)
	@commands.guild_only()
	async def pokemon(self, ctx, *, title):
		pokemon = pokepy.V2Client().get_pokemon(f"{title.lower()}")
		name = pokemon.name
		weight = pokemon.weight
		type_ = pokemon.types[0].type.name
		
		print(type_)
		





def setup (Bot):
	Bot.add_cog(pokemon(Bot))
	print("Pokemon cog is working.")