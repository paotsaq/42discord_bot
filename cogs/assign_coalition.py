# What this modules does:
# - Assigns a coalition (role) to each user in the server.

import discord
from discord.ext import commands
import re
import time
import json

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
	'119': "jetsons",
	'120': "simpsons",
	'121': "flinstones"
}

class AssignsRole(commands.Cog):
	def __init__(self, client):
		self.client = client

	@commands.command()
	async def attribute_roles(self, ctx):
		await ctx.message.delete()
		for user in self.list_users:
			for team in users.keys():
				if user.nick in users[team]:
					self.client.user.add_roles(match_coalition_to_id[team])



def setup(client):
	client.add_cog(AssignsRole(client))
