import discord
from discord.ext import commands, tasks

import pymongo
from pymongo import MongoClient
import random



class topic(commands.Cog, name="topic"):
    def __init__(self, Bot):
        self.Bot = Bot
        self.fetch_topic.start()
        self.raw_topics=[
	        'Which is your favourite anime and why?',
	        'If you had a change to go back in time will you and why?',
	        'Whom do you aspire the most and why?',
	        'Which is the best hmanga?',
	        'If you didn\'t know about anime how would it change your life?',
	        'Now you look back, is there anything you regret?',
	        'Do you have a crush and did you ever think of going forward to him/her?',
	        'What type of people do you hate the most?',
	        'If you could tell something to your younger self what would it be?',
	        'If the world was ending tomorrow what things would you do?',
	        'What gets you most annoyed?',
	        'If you found 1 million $ in a bag what would you do?',
	        'Have you ever been rejected and if yes what did you learn from that experience?',
	        'Which is the best game and why?',
	        'What is the thing that everyone hates but you love the most?',
	        'If you were a parent how would you care for your child?',
	        'If your gender gets swapped what\'s the first thing you\'d do?',
	        'What do you aspire to become in the future?',
	        'Which is the best anime OP in your point of view?',
	        'For which anime would you clear your memory to watch again?',
	        'Who is the best actor/actress in your opinion?',
	        'Who is the best waifu in your opinion?',
	        'Who is the best husbando in your opinion?',
	        'For which actor/actress you will even change you gender?',
	        'What\'s the best kink?',
	        'Which fictional character has the best personality?',
	        'What was your most embarrassing moment.',
	        'Why does water taste better at 1am?',
	        'What is the best snack to eat at 1am?',
	        'At what time period do you find yourself more productive?',
	        'Who are your favorite anime couple?',
	        'What was the first anime you ever watched and what impact did that have in your life?',
	        'Do you regret watching anime?',
	        'What was your favorite video game as a child?',
	        'Do you think you’ll ever stop watching anime?',
	        'What makes an anime stand out from the rest?',
	        'What is the best persent that you have ever gotten?',
	        'What is your favorite thing about anime?',
	        'If you could meet an anime character who would it be?',
	        'Would you rather be rich or famous?',
	        'Who is the most OP anime character?',
	        'Which is the best anime weapon?',
	        'Which is the sadest anime you have ever watched?',
	        'Which is the anime you are ashamed of enjoying?',
	        'Is flat chest the justice?',
	        'Flat or Boing?',
	        'Which anime has the best plot and why?',
	        'How are you really?',
	        'What is the thing you are most afraid of?'
        ]

    @commands.command(aliases=['topics', 'questions'])
    @commands.guild_only()
    async def topic(self, ctx):  
        topic = random.choice(self.raw_topics)
        await ctx.send(f"{topic}")

    @commands.command(aliases=['atopic'])
    @commands.is_owner()
    @commands.guild_only()
    async def addtopic(self, ctx, *, topic):
        
        db = self.Bot.db2['AbodeDB']
        collection2 = db ['Topics']

        if (collection2.find_one({"_id": topic})== None):
            gif_data= {"_id": topic}
            collection2.insert_one(gif_data)
            await ctx.send(f'Just added a new topic `{topic}`')

        else:
            await ctx.send(f'{ctx.author.name}, there already exists a topic by that name please try another name.', delete_after=10)    

    @tasks.loop(seconds= 3600)
    async def fetch_topic(self):
    	db = self.Bot.db2['AbodeDB']
    	collection= db['Topics']

    	result = collection.find()
    	for ans in result:
    		topic1 = ans['_id']
    		self.raw_topics.append(topic1)
    	return 


def setup (Bot):
	Bot.add_cog(topic(Bot))
	print("Topic cog is working.")
