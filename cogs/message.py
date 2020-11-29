# What this modules does:
# - Sends funny messages to users based on their message

import discord
from discord.ext import commands

class Message(commands.Cog):
	def __init__(self, client):
		self.client = client

	@commands.Cog.listener()
	async def on_message(self, message):
		if message.author == self.client.user:
			return
		elif message.content.startswith('Amo-te'):
			await message.channel.send('Só amo o Miguel Gueifão...!')
		elif "slack" in message.content:
			await message.channel.send(
				'do you miss the :rotating_light: slack police :rotating_light:'
			)
		elif "vs code" in message.content:
			await message.channel.send(
				'Hey! Here are the :rotating_light: top 10 :boom: reasons to use VSCode: \n(null)'
			)

def setup(client):
	client.add_cog(Message(client))
