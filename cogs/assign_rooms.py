# What this modules does:
# - Assigns a coalition (role) to each user in the server.

import discord
from discord.ext import commands
import re
import time
import json
import datetime

# Switch between prod and dev branches
from bot import switch, branches
if switch == branches[0]:
	import ids_prod as ids
else:
	import ids_dev as ids

def fetch_users(path_to_database):
    json_file = open(path_to_database, 'r')
    loaded_dict = json.load(json_file)
    json_file.close()
    return loaded_dict

# this is a dictionary!
# users[coalition_id] is a list of all usernames on that given coalition
users = fetch_users("database/coalition_users.json")

match_coalition_to_id = {
	'119': ids.jetsons,
	'120': ids.simpsons,
	'121': ids.flintstones
}

class AssignsRole(commands.Cog):
	def __init__(self, client):
		self.client = client

	@commands.command()
	async def attribute_roles(self, ctx):
		if(ids.staff in [x.id for x in ctx.author.roles]):
			await ctx.message.delete()
			guild = self.client.get_guild(ids.guild_id)
			for user in guild.members:
				for team in users.keys():
					if user.display_name in users[team]:
						snowflake = discord.Object(match_coalition_to_id[team])
						await user.add_roles(snowflake)

def setup(client):
	client.add_cog(AssignsRole(client))
