# What this modules does:
# - Add 2 commands to clear messages
# - Add a stop command

import ids
import discord
from discord.ext import commands

class Commands(commands.Cog):
	def __init__(self, client):
		self.client = client

	# For everyone, clears the user's last sent message
	@commands.command(aliases=['c'])
	async def clear(self, ctx):
		await ctx.message.delete()
		async for message in ctx.channel.history(limit=None):
			if message.author.id == ctx.author.id:
				await message.delete()
				return

	# For staff only, clears a given number of lines. 1 being the default if no number is given as parameter
	@commands.command(aliases=['fc'])
	async def fclear(self, ctx, amount=1):
		if(ids.staff in [x.id for x in ctx.author.roles]):
			await ctx.channel.purge(limit=amount + 1)

	@commands.command()
	async def stop(self, ctx):
		if(ids.staff in [x.id for x in ctx.author.roles]):
			await ctx.channel.send("Logging out!")
			await self.client.close()

def setup(client):
	client.add_cog(Commands(client))
