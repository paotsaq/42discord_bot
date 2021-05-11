# What this modules does:
# manages a dictionary with the playerbases on the server

import discord
from discord.ext import commands
import json

PATH_TO_ROSTERS_DICT = "./rosters_dict.json"
#TODO remove bot from perms
#TODO introduce alias to games
ACTIONS = ['create', 'delete', 'add', 'remove', 'show']
ROLE_COLOR = discord.colour.Colour.from_rgb(212, 247, 49)
VALID_ROLES = ['staff', 'bot']
is_valid_role = lambda role: role.name in VALID_ROLES
fetch_roster_role = lambda role: role.name in VALID_ROLES
fetch_role_name = lambda game: f'game_roster_{game}'

def valid_perms(roles):
	return any(map(is_valid_role, roles))

def role_exists(name_role, ctx):
	return name_role in [role.name for role in ctx.guild.roles]

class Rosters(commands.Cog):
	def __init__(self, client):
		self.client = client
		self.rosters_dict = {}
		self.dict_loader()

	def help_string(self):
		return "roster syntax: ``.r action game [user]``"

	#TODO wrap this on dictionary
	def dict_loader(self):
		try:
			json_file = open(PATH_TO_ROSTERS_DICT, 'r')
			self.rosters_dict = json.load(json_file)
			print(self.rosters_dict)
			json_file.close()
		except FileNotFoundError:
			json_file = open(PATH_TO_ROSTERS_DICT, 'w')
			json.dump({}, json_file)
			print(f"""There is no file for {PATH_TO_ROSTERS_DICT}!\n Backup is recreating rosters from discord roles""")

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

	async def checks_valid_input(self, ctx, game, action, nickname):
		print(f'{nickname} perms: {valid_perms(ctx.author.roles)}')
		if valid_perms(ctx.author.roles):
			if game is not None:
				if game not in self.rosters_dict.keys():
					return True
				else:
					await ctx.send(f"{game} was already added to the rosters!")
			else:
				await ctx.send(f"⚠️ That's a no no...because the game parameter was null!!\n{self.help_string()}")
		else:
			await ctx.send(f"⚠️ That's a no no... you, {ctx.author.nick}, do not have ``{action}`` permissions!")

	# command syntax:
	# .r [action] [name_of_roster]
	@commands.command(aliases = ['r'])
	async def roster(self, ctx, action, game=None, nickname=None):

		name = nickname if valid_perms(ctx.author.roles) and nickname else ctx.author.nick
		# await ctx.channel.purge(limit=1)
		if action == 'create' and await self.checks_valid_input(ctx, game, action, nickname):
			game_role = await ctx.guild.create_role(name=fetch_role_name(game), color=ROLE_COLOR, mentionable=True)
			self.dict_writer(action, game)
			await ctx.send(f"{game} was added to the rosters!")
		elif action == 'delete' and valid_perms(ctx.author.roles):
			role = discord.utils.get(ctx.guild.roles, name=fetch_role_name(game))
			try:
				self.dict_writer(action, game)
				await ctx.send(f"Roster for {game} successfully deleted (if it existed)!")
			except KeyError:
				await ctx.send(f"Roster for {game} didn't exist!")
			try:
				await role.delete()
				await ctx.send(f"Role for {game} successfully deleted!")
			except AttributeError:
				print(f"The role {fetch_role_name(game)} didn't exist!")
		elif action in {'add', 'remove'}:
			if game and game != ctx.message.author.nick:
				if game in self.rosters_dict.keys():
					role = discord.utils.get(ctx.guild.roles, name=fetch_role_name(game))
					if action == 'add':
						if name not in self.rosters_dict[game]:
							self.dict_writer(action, game, name)
							await ctx.send(f"{name} was added to the {game} roster!")
							await ctx.message.author.add_roles(role)
						else:
							await ctx.send(f"{name} was already previously added to the {game} roster!")
					elif action == 'remove':
						if name in self.rosters_dict[game]:
							self.dict_writer(action, game, name)
							await ctx.message.author.remove_roles(role)
							await ctx.send(f"{name} was removed from the {game} roster!")
						else:
							await ctx.send(f"{name} wasn't in the {game} roster...!")
				else:
					await ctx.send(f"⚠️ That's a no no...because the game doesn't exist on the roster!!\n{self.help_string()}")
			else:
				await ctx.send(f"⚠️ That's a no no...because the game parameter was null!\n{self.help_string()}")
		elif action == 'show':
			await ctx.send(self.roster_printer(game))
		elif action in ['help', 'h']:
			await ctx.send(f"You requested help! ``.r help``\n{self.help_string()}")

	def roster_printer(self, game=None):
		if not game:
			if not self.rosters_dict:
				return "There are no rosters!"
			else:
				return "These are the current rosters:\n" + " | ".join(list(self.rosters_dict.keys())) + "| "
		elif game not in self.rosters_dict.keys():
			return ("This game was not yet added...request the help of someone with permissions (try #bocal-but-not-really!)")
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

def setup(client):
	client.add_cog(Rosters(client))
