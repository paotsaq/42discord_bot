import discord
from urllib.request import urlopen
from discord.ext import commands, tasks
from itertools import cycle

status = cycle([
	'chess with Norminette', 'csgo  with Norminette', 'lol with Norminette',
	'Among Us with Norminette'
])


class Main(commands.Cog):
	def __init__(self, client):
		self.client = client

	@commands.Cog.listener()
	async def on_ready(self):
		self.change_status.start()
		print('We have logged in as {0.user}'.format(self.client))

	@tasks.loop(seconds=10)
	async def change_status(self):
		await self.client.change_presence(activity=discord.Game(next(status)))

	# Just playing around with commands
	# Actually I don't think we need it for what we discussed as /nick is already a Discord command. Still handy mecanism for a bot to have
	@commands.command()
	async def ping(self, ctx):
		await ctx.send('Pong!')


def setup(client):
	client.add_cog(Main(client))


# Clears a given number of lines. 1 being the default if no number is given as parameter
# @client.command()
# async def clear(ctx, amount=1):
#     await ctx.channel.purge(limit=amount)

# @client.event
# async def on_message(message):
#     if message.author == client.user:
#         return
#     elif message.content.startswith('Amo-te'):
#         await message.channel.send('só amo o Miguel Gueifão...!')
#     elif "slack" in message.content:
#         await message.channel.send('do you miss the :rotating_light: slack police :rotating_light:')
#     elif "vs code" in message.content:
#         await message.channel.send('Hey! Here are the :rotating_light: top 10 :boom: reasons to use VSCode: \n (null)')
# elif client.event.channel.name == 'welcome':
#     if message.content.startswith('/nick'):
#         nick = message.split()
#         url = 'https://cdn.intra.42.fr/users/%7B0%7D.jpg', nick[1]
#         check = urllib.urlopen(url)

# Line needed at the end of @client.event if we want to run @client.command
# await client.process_commands(message)
