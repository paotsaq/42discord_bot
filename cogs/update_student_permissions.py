# What this modules does:
# awaits for a trigger to build new user database
# after getting the database, assigns permissions to view cursus channels

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

class AssignsRole(commands.Cog):
	def __init__(self, client):
		self.client = client

	@commands.command()
	async def attribute_42student(self, ctx):
		# users[coalition_id] is a list of all usernames on that given coalition
		if(ids.staff in [x.id for x in ctx.author.roles]):
			users = fetch_users("database/users_id_database.json")
			await ctx.message.delete()
			guild = self.client.get_guild(ids.guild_id)
			for user in guild.members:
				if user.display_name in users.keys():
					snowflake = discord.Object(ids.student42)
					await user.add_roles(snowflake)

def setup(client):
	client.add_cog(AssignsRole(client))
