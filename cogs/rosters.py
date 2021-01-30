# What this modules does:
# manages a dictionary with the playerbases on the server

import discord
from discord.ext import commands
import json

PATH_TO_ROSTERS_DICT = "./cogs/resources/rosters_dict.json"

class Rosters(commands.Cog):
	def __init__(self, client):
		self.client = client
		self.rosters_dict = {}
		self.dict_loader()

	def dict_loader(self):
		json_file = open(PATH_TO_ROSTERS_DICT, 'r')
		self.rosters_dict = json.load(json_file)
		json_file.close()

	def dict_writer(self, action, game, nick=None):
		if action == 'create':
			self.rosters_dict[game] = []
		elif action == 'delete':
			del self.rosters_dict[game]
		elif action == 'add':
			self.rosters_dict[game].append(nick)
		else:
			self.rosters_dict[game].remove(nick)
		json_file = open(PATH_TO_ROSTERS_DICT, 'w')
		json.dump(self.rosters_dict, json_file, indent=2)
		json_file.close()
		self.dict_loader()

	def roster_printer(self, game):
		if game not in self.rosters_dict.keys():
			return ("This game was not yet added...maybe you should reach staff at #bocal? :pensive:")
		else:
			number_of_players = len(self.rosters_dict[game])
			if number_of_players == 0:
				return (f"There is no one in the {game} roster! What a shame... :pensive:")
			else:
				res_string = f"**This is the current {game} roster:**\n"
				if number_of_players == 1:
					res_string += f"The very lonely {self.rosters_dict[game][0]}. Let's fix that!"
				elif number_of_players == 2:
					res_string += f"{self.rosters_dict[game][0]} and {self.rosters_dict[game][1]}."
				else:
					for name_index in range(number_of_players - 1):
						res_string += self.rosters_dict[game][name_index] + ", "
					res_string += f"and {self.rosters_dict[game][number_of_players - 1]}."
				return (res_string)

	@commands.command(aliases = ['r'])
	async def roster(self, ctx, action, game="None"):
		#TODO REMOVE BOT!!!!!!!!!!!!!!!!!!!!!!!!!!!
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
