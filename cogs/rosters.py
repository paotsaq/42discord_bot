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
fetch_role_name = lambda game: f'roster_{game}'

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
		return "roster syntax: ``.r action [activity] [user]``"

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

	def dict_writer(self, action, activity, nick=None):
		if action == 'create':
			self.rosters_dict[activity] = []
		elif action == 'delete':
			del self.rosters_dict[activity]
		elif action == 'add':
			self.rosters_dict[activity].append(nick)
		else:
			self.rosters_dict[activity].remove(nick)
		json_file = open(PATH_TO_ROSTERS_DICT, 'w')
		json.dump(self.rosters_dict, json_file, indent=2)
		json_file.close()
		self.dict_loader()

	async def checks_valid_input(self, ctx, activity, action, nickname):
		print(f'{nickname} perms: {valid_perms(ctx.author.roles)}')
		if valid_perms(ctx.author.roles):
			if activity is not None:
				if activity not in self.rosters_dict.keys():
					return True
				else:
					await ctx.send(f"{activity} was already added to the rosters!")
			else:
				await ctx.send(f"⚠️ That's a no no...because the activity parameter was null!!\n{self.help_string()}")
		else:
			await ctx.send(f"⚠️ That's a no no... you, {ctx.author.nick}, do not have ``{action}`` permissions!")


	# TODO this could be a lot shorter? maybe design a way to generalize something here?
	# command syntax:
	# .r [action] [name_of_roster]
	@commands.command(aliases = ['r'])
	async def roster(self, ctx, action, activity=None, nickname=None):
		name = nickname if valid_perms(ctx.author.roles) and nickname else ctx.author.nick
		# await ctx.channel.purge(limit=1)
		if action == 'create' and await self.checks_valid_input(ctx, activity, action, nickname):
			activity_role = await ctx.guild.create_role(name=fetch_role_name(activity), color=ROLE_COLOR, mentionable=True)
			self.dict_writer(action, activity)
			await ctx.send(f"{activity} was added to the rosters!")
		elif action == 'delete' and valid_perms(ctx.author.roles):
			role = discord.utils.get(ctx.guild.roles, name=fetch_role_name(activity))
			try:
				self.dict_writer(action, activity)
				await ctx.send(f"Roster for {activity} successfully deleted (if it existed)!")
			except KeyError:
				await ctx.send(f"Roster for {activity} didn't exist!")
			try:
				await role.delete()
				await ctx.send(f"Role for {activity} successfully deleted!")
			except AttributeError:
				print(f"The role {fetch_role_name(activity)} didn't exist!")
		elif action in {'add', 'remove'}:
			if activity and activity != ctx.message.author.nick:
				if activity in self.rosters_dict.keys():
					role = discord.utils.get(ctx.guild.roles, name=fetch_role_name(activity))
					if action == 'add':
						if name not in self.rosters_dict[activity]:
							self.dict_writer(action, activity, name)
							await ctx.send(f"{name} was added to the {activity} roster!")
							await ctx.message.author.add_roles(role)
						else:
							await ctx.send(f"{name} was already previously added to the {activity} roster!")
					elif action == 'remove':
						if name in self.rosters_dict[activity]:
							self.dict_writer(action, activity, name)
							await ctx.message.author.remove_roles(role)
							await ctx.send(f"{name} was removed from the {activity} roster!")
						else:
							await ctx.send(f"{name} wasn't in the {activity} roster...!")
				else:
					await ctx.send(f"⚠️ That's a no no...because the activity doesn't exist on the roster!!\n{self.help_string()}")
			else:
				await ctx.send(f"⚠️ That's a no no...because the activity parameter was null!\n{self.help_string()}")
		elif action == 'show':
			await ctx.send(self.roster_printer(activity))
		elif action in ['help', 'h']:
			await ctx.send(f"You requested help! ``.r help``\n{self.help_string()}")

	def roster_printer(self, activity=None):
		if not activity:
			if not self.rosters_dict:
				return "There are no rosters!"
			else:
				return "These are the current rosters:\n" + " | ".join(list(self.rosters_dict.keys())) + "| "
		elif activity not in self.rosters_dict.keys():
			return ("This activity was not yet added...request the help of someone with permissions (try #bocal-but-not-really!)")
		else:
			number_of_players = len(self.rosters_dict[activity])
			if number_of_players == 0:
				return (f"There is no one in the {activity} roster! What a shame... :pensive:")
			else:
				res_string = f"**This is the current {activity} roster:**\n"
				if number_of_players == 1:
					res_string += f"The very lonely {self.rosters_dict[activity][0]}. Let's fix that!"
				elif number_of_players == 2:
					res_string += f"{self.rosters_dict[activity][0]} and {self.rosters_dict[activity][1]}."
				else:
					for name_index in range(number_of_players - 1):
						res_string += self.rosters_dict[activity][name_index] + ", "
					res_string += f"and {self.rosters_dict[activity][number_of_players - 1]}."
				return (res_string)

def setup(client):
	client.add_cog(Rosters(client))
