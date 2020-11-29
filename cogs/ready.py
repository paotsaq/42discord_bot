# What this modules does:
# - Displays message if the bot is online
# - Adds a status to the bot and cycles through several status

import discord
from discord.ext import commands, tasks
from itertools import cycle

status = cycle([x + ' with Norminette' for x in [
	'chess', 'csgo', 'lol', 'Among Us', 'Minecraft','CodinGame'
]])

class Ready(commands.Cog):
	def __init__(self, client):
		self.client = client

	@commands.Cog.listener()
	async def on_ready(self):
		self.change_status.start()
		print('We have logged in as {0.user}'.format(self.client))

	@tasks.loop(minutes=5)
	async def change_status(self):
		await self.client.change_presence(activity=discord.Game(next(status)))

def setup(client):
	client.add_cog(Ready(client))
