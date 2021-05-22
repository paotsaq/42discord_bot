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
		self.sent_text_message = await ctx.message.channel.send("For better readability and syntax formatting, please format your code accordingly! 🤖\n`` ``` [language]\n[code]\n``` ``\n where ``[language]`` can be ``C``, ``Python``, etc. and ``[code]`` is... well, your code. ⌨️\nClick on ✅ to remove the message when you're done.")
		self.sent_image_message = await ctx.message.channel.send("https://bzzzzzzz.buzz/static/print.png")
		await self.sent_image_message.add_reaction('✅')

	@commands.Cog.listener()
	async def on_raw_reaction_add(self, ctx):
		if ctx.member == self.client.user:
			return
		if ctx.emoji.name == '✅' and ctx.message_id == self.sent_image_message.id:
			await self.sent_text_message.delete()
			await self.sent_image_message.delete()

def setup(client):
	client.add_cog(CodeFormat(client))
