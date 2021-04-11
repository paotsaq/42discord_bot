# What this modules does:
# prints a tutoring message for clean code on Discord!

import discord
from discord.ext import commands
import datetime

# Switch between prod and dev branches
from bot import switch, branches
if switch == branches[0]:
	import ids_prod as ids
else:
	import ids_dev as ids

class CodeFormat(commands.Cog):
	def __init__(self, client):
		self.client = client

	@commands.command()
	async def code(self, ctx):
		await ctx.message.delete()
		await ctx.message.channel.send("For better readability and syntax formatting, please format your code accordingly! 🤖\nInsert `` ``` [language] [code] ``` ``, where ``[language]`` can be ``C``, ``Python``, etc. and ``[code]`` is, well, your code.")
		await ctx.message.channel.send("https://bzzzzzz.buzz/static/print.png")

def setup(client):
	client.add_cog(CodeFormat(client))
