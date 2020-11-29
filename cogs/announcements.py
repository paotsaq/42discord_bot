# What this modules does:
# - Lets the admins send prerecorded messages through the bot

import discord
from discord.ext import commands
import ids
import time

class Announcements(commands.Cog):
	def __init__(self, client):
		self.client = client

	@commands.command()
	async def send(self, ctx, filename):
		f = None
		await ctx.message.delete()
		if(ids.staff in [x.id for x in ctx.author.roles]):
			try:
				f = open(f"./messages/{filename}.txt", 'r')
			except IOError:
				error_message = await ctx.channel.send("Filename invalid")
				time.sleep(2)
				await error_message.delete()
			else:
				message = f.read()
				f.close()
				for var in vars(ids):
					if var in message:
						message = message.replace(str(var), str(vars(ids)[var]))
				await ctx.channel.send(message)
			finally:
				if f:
					f.close()

def setup(client):
	client.add_cog(Announcements(client))
