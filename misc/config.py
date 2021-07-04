import discord
from discord.ext import commands, tasks
import pymongo
from pymongo import MongoClient
import random


class config(commands.Cog, name="config"):
	def __init__(self, Bot):
		self.Bot = Bot
		self.black_list_guilds.start()

	@commands.command(description=f"Removes a certian command from a certain guild.")
	@commands.guild_only()
	@commands.has_permissions(administrator=True)
	async def disablecommand(self, ctx, commandName):
		
		name = []
		for cmd in self.Bot.commands:
			name.append(cmd.name)
		if not f"{commandName}" in name:
			return await ctx.send(f"{ctx.author.mention} it seems that the commandname you entered doesn't exist in the system. If you tried using a aliases then please try again using the command's real name.")
		db = self.Bot.db2['AbodeDB']
		collection= db['Config']
		guildid = ctx.guild.id
		list1_ = []
		list1_.append(commandName)

		if (collection.find_one({"_id": ctx.guild.id})== None):
			guild_data= {"_id": guildid, "command": list1_}
			collection.insert_one(guild_data)
			return await ctx.send(f"Comamnd {commandName} is now blacklisted. It usually takes around 30seconds for this to be saved so hangtight.")
		else:
			list_ = []
			qurey = {"_id": guildid}
			search = collection.find(qurey)
			for result in search:
				for x in result['command']:
					list1_.append(x)
			
			collection.update_one({"_id": ctx.guild.id}, {"$set": {"command": list1_}})
			return await ctx.send(f"Comamnd {commandName} is now blacklisted. It usually takes around 30seconds for this to be saved so hangtight.")


	@commands.command(description=f"Re-adds the removed command from a certain guild.")
	@commands.guild_only()
	@commands.has_permissions(administrator=True)
	async def enablecommand(self, ctx, commandName):
		name = self.Bot.commandName
		if not f"{commandName}" in name:
			return await ctx.send(f"{ctx.author.mention} it seems that the commandname you entered doesn't exist in the system. If you tried using a aliases then please try again using the command's real name.")
		db = self.Bot.db2['AbodeDB']
		collection= db['Config']
		guildid = ctx.guild.id
		list_ = []
		
		qurey = {"_id": guildid}
		search = collection.find(qurey)
		for result in search:
			for x in result['command']:
				list_.append(x)
		
		list_.remove(commandName)
		a = 0
		# try:
		if a ==0:
			collection.update_one({"_id": ctx.guild.id}, {"$set": {"command": list_}})
			return await ctx.send(f"Comamnd {commandName} is now enabled. It usually takes around 30seconds for this to be saved so hangtight.")
		# except:
		# 	return await ctx.send(f"Are you sure the command is disabled? Try checking it through `dh listdisabledcommands`.")

	async def bot_check(self,ctx):
		name = self.Bot.commandName
		if not ctx.guild.id in self.blackListGuilds:
			return True
		else:
			
			command = ctx.command
			db = self.Bot.db2['AbodeDB']
			collection= db['Config']
			qurey = {"_id": ctx.guild.id}
			search = collection.find(qurey)
			
			cmds = []
			for ans1 in search:
				for x in ans1['command']:
					cmds.append(x)
			
			if not f"{command}" in cmds:				
				return True

	@commands.command(description=f"List all the disabled commands on a guild.")
	@commands.guild_only()
	@commands.has_permissions(administrator=True)
	async def listdisabledcommands(self, ctx):
		db = self.Bot.db2['AbodeDB']
		collection= db['Config']
		qurey = {"_id": ctx.guild.id}
		search = collection.find(qurey)
		embed = discord.Embed(color =random.choice(self.Bot.color_list))
		list_ = []
		for result in search:
			for x in result['command']:
				list_.append(x)
		try:
			embed.add_field(name="List of commands", value=f"\n".join(list_[:1023]))
		except:
			embed.description=f"Too long to be displayed here :_:"
		await ctx.send(embed=embed)


	@tasks.loop(seconds=15)
	async def black_list_guilds(self):

		await self.Bot.wait_until_ready()
		db = self.Bot.db2['AbodeDB']
		collection= db['Config']
		self.blackListGuilds =[]
		search = collection.find()
		for guild in search:
			id_ = guild["_id"]
			if not id_ in self.blackListGuilds:
				self.blackListGuilds.append(id_)
		
		return 

def setup (Bot):
	Bot.add_cog(config(Bot)
		)
	print("Config cog is working.")