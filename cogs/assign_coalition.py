# What this modules does:
# - Assigns a coalition (role) to each user in the server.

import discord
from discord.ext import commands
import re
import time

# Switch between prod and dev branches
from bot import switch, branches
if switch == branches[0]:
	import ids_prod as ids
else:
	import ids_dev as ids

def role_exists(name_role, ctx):
	return name_role in [role.name for role in ctx.guild.roles]:

def fetch_users(path_to_database):
    json_file = open(path_to_database, 'r')
    loaded_dict = json.load(json_file)
    json_file.close()
    return loaded_dict

users = fetch_users("database/coalition_users.json")


await ctx.message.author.add_roles(role)

class AssignsRole(commands.Cog):
	def __init__(self, client):
		self.client = client

	@commands.command()
	async def piscine(self, ctx, month=""):
		await ctx.message.delete()

