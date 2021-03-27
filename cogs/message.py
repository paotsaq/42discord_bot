# What this modules does:
# - Sends funny messages to users based on their message

import discord
from discord.ext import commands
import random
import time

class Message(commands.Cog):
	def __init__(self, client):
		self.client = client

	@commands.Cog.listener()
	async def on_message(self, message):
		if message.author == self.client.user:
			return
		elif "amor" in message.content:
			odd = random.randint(0, 500)
			if odd in range(3):
				await message.channel.send('I wish deepthought would desire me just in the same way... ')
				time.sleep(3)
				await message.channel.send('... :smiling_face_with_3_hearts: as mgueifao does his VS Code :vscode: :vscode_insider:')

		elif "slack" in message.content:
			odd = random.randint(0, 1000)
			if odd in range(1):
				await message.channel.send(
					'do you miss the :rotating_light: slack police :rotating_light:'
				)
				time.sleep(3)
				await message.channel.send(
					'...I\'m sorry, everyone. I get bored. :sleeping: There\'s nothing to police around here anymore...'
				)
			elif odd in range(1, 2):
				await message.channel.send(
					"I have been a very naughty bot :yum: and I'm not allowed to react to slack anymore :japanese_goblin:"
				)
		elif "vscode" in message.content or "vs code" in message.content:
			odd = random.randint(0, 500)
			if odd in range(1):
				await message.channel.send(
					'Hey! Here are the :rotating_light: top 3 :boom: reasons to use VSCode: \n'
				)
				time.sleep(2)
				await message.channel.send(
					'(null)\n'
				)
		elif "moulinette" in message.content:
			odd = random.randint(0, 200)
			if odd in range(1):
				await message.channel.send(
					'Whoa! You are so lucky! :four_leaf_clover: You just triggered the 42 LISBOA DISCORD raffle! :moneybag:\n'
					'to win IMMEDIATELY, just respond with `let me win, moulinette!` :100:\n'
					':medal: the user with MOST REPLIES, wins! :partying_face: GO :bangbang:\n'
				)
				time.sleep(11)
				await message.channel.send(
					'OMG this is so exciting!!1! \nPlease click the link! :point_right: <https://bit.ly/3qgV6jf> :rocket:\n'
				)


def setup(client):
	client.add_cog(Message(client))
