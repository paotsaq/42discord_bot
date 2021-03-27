# What this modules does:
# manages relationships among coding buddies!

import discord
from discord.ext import commands
import json

PATH_TO_BUDDIES_DICT = "./cogs/resources/rosters_dict.json"

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
		await ctx.author.send("*beep bop* Do I hear there's going to be a new bot feature soon?... 🤖")

def setup(client):
	client.add_cog(BuddyDatabase(client))
