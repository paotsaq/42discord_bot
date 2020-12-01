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

	# For test server only, kills the bot even if it's running on someone else's computer
	# To be used, only when someone has forgot to kill the bot
	@commands.command()
	async def stop(self, ctx):
		test_server_id = 777686265600540682
		if ctx.author.guild.id == test_server_id:
			await ctx.channel.send("Logging out!")
			await self.client.close()

	# For staff only, removes every role for every user that is not staff or bot
	# Once cleaned of its role, user receives check_rules role
	@commands.command()
	async def reset_roles(self, ctx):
		check_rules_role = discord.utils.get(ctx.author.guild.roles, id=ids.check_rules)
		if(ids.staff in [x.id for x in ctx.author.roles]):
			async for member in ctx.guild.fetch_members(limit=None):
				if not (ids.staff in [x.id for x in member.roles]) and not (ids.bot_role in [x.id for x in member.roles]):
					self.client.guild = self.client.get_guild(ids.server)
					memberObj = self.client.guild.get_member(member.id)
					for role in memberObj.roles:
						if not role.name == '@everyone':
							await memberObj.remove_roles(role)
					await member.add_roles(check_rules_role)



def setup(client):
	client.add_cog(Commands(client))
