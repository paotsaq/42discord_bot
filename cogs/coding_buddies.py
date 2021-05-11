# What this modules does:
# manages relationships among coding buddies!

import discord
from discord.ext import commands
import json
import re
import time
import asyncio

PATH_TO_BUDDIES_DICT = "./cogs/resources/rosters_dict.json"
# this dictionary will relate each question to its possible values and a scale.

# [[question, expected format (regex)]]
QUESTIONS_LIST = [
		["From 1 to 5, how comfortable would you be with leading the team?",
			r'''^[1-5]$'''],
		["From 1 to 5, how willing are you to try out a new programming language?",
			r'''^[1-5]$'''],
		["Will you be fully (or mostly) remote during the duration of the assignment?\n1 means yes, 0 means no.",
			r'''^[0|1]$'''],
		["What is the meaning of life, by the way?",
			r'''^[42]$''']
]

# the BuddyDatabase class will organize a database with possible buddies to be matched. The info about each candidate buddy will be collected through DM's.
class BuddyDatabase(commands.Cog):
	def __init__(self, client):
		self.client = client
		self.buddies_dict = {}
		self.dict_loader()

	# dict handling methods can be done with the dictionary script.
	def dict_loader(self):
		json_file = open(PATH_TO_BUDDIES_DICT, 'r')
		self.buddies_dict = json.load(json_file)
		json_file.close()

	def dict_writer(self, action, nick=None):
		if action == 'create':
			self.buddies_dict[game] = []
		elif action == 'delete':
			del self.buddies_dict[game]
		elif action == 'add':
			self.buddies_dict[game].append(nick)
		else:
			self.buddies_dict[game].remove(nick)
		json_file = open(PATH_TO_BUDDIES_DICT, 'w')
		json.dump(self.buddies_dict, json_file, indent=2)
		json_file.close()
		self.dict_loader()

	@commands.command()
	async def codingbuddy(self, ctx):
		await ctx.channel.purge(limit=1)
		await ctx.author.send("*beep bop* Do I hear you want to join the *Coding Buddy* programme?... 🤖")
		async with ctx.channel.typing():
			time.sleep(3)
		await ctx.author.send("Do you know what the programme is about?")
		async with ctx.channel.typing():
			time.sleep(2)
		await ctx.author.send("Of course you do. But please, if you ever run into any sort of problem, let the Discord voluntary staff help you out! So, I need you to answer some questions...")
		answers = []
		for question_pair in QUESTIONS_LIST:
			async with ctx.channel.typing():
				time.sleep(2)
			await ctx.author.send(question_pair[0])
			try:
				message = await self.client.wait_for('message', timeout=40.0)
			except asyncio.TimeoutError:
				await channel.send("Oh my...you took too long and I got distracted :yawning_face: Please trigger this dialogue again!")
			print(message)
			# if regex_match(message,

def setup(client):
	client.add_cog(BuddyDatabase(client))
