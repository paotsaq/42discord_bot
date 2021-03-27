# What this modules does:
# manages relationships among coding buddies!

import discord
from discord.ext import commands
import json

PATH_TO_BUDDIES_DICT = "./cogs/resources/rosters_dict.json"

# initializes the BuddyDatabase class, with some dictionary handling methods, that handles read/write to the dictionaries.
class BuddyDatabase(commands.Cog):
	def __init__(self, client):
		self.client = client
		self.buddies_dict = {}
		self.dict_loader()

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

	@commands.command(aliases = ['r'])
	async def codingbuddy(self, ctx, action, game="None"):
		await ctx.channel.purge(limit=1)

		if action in {'create', 'delete'}:
			if ('staff' in [x.name for x in ctx.author.roles] or 'bot' in [x.name for x in ctx.author.roles]):
				verb = 'add' if action == create else 'remove'
				await ctx.send(f"They brought the big guns! :scream: Let's {verb} {game} to the rosters...my master {ctx.author.nick}!")
				self.dict_writer(action, game)
			else:
				await ctx.send(f"I cannot pursue the actions you so tenderly wish...remember that I am *very* strict and mean!")
		# assumes game
		elif action in {'add', 'remove'}:
			self.dict_writer(action, game, name)
			verb = 'added' if action == 'add' else 'removed'
			await ctx.send(f"We are led to believe you, {name}, were {verb} to the {game} roster!")
		elif action == 'show':
			await ctx.send(self.roster_printer(game))

def setup(client):
	client.add_cog(Rosters(client))
