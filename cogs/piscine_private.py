# What this modules does:
# - Add the possibility for users to have a private space to chat among a piscine (text and voice)

import discord
from discord.ext import commands
import re
import time

# Switch between prod and dev branches
from bot import switch, branches
if switch == branches[0]:
	import ids_prod as ids
else:
	import ids_dev as ids


# Check if the month argument passed with .piscine command is valid
def arg_valid(arg):
	regex = "^\d{2}/\d{2}$"
	return re.match(regex, arg)

# List of past piscines. As 2 functions:
# 1. Check if the month passed in as parameter by user is valid
# 2. See the index of the piscine to have a unique number
piscines = ["10/20", "11/20", "01/21", "06/21", "07/21"]

def piscine_exists(month):
	if month in piscines:
		return True
	else:
		return False

def role_exists(name_role, ctx):
	if name_role in [role.name for role in ctx.guild.roles]:
		return True
	else:
		return False

def user_has_piscine(ctx):
	regex = "^piscine-\d{2}$"
	for role in ctx.author.roles:
		if re.match(regex, role.name):
			return True
	return False

class Piscine_private(commands.Cog):
	def __init__(self, client):
		self.client = client

	@commands.command()
	async def piscine(self, ctx, month=""):
		await ctx.message.delete()
		if month == "":
			msg = await ctx.send(f"<@!{ctx.author.id}>: Missing the `month` parameter")
			time.sleep(3)
			await msg.delete()
		elif not arg_valid(month):
			msg = await ctx.send(f"<@!{ctx.author.id}>: \"{month}\" is not a valid argument. Example of valid argument: \"10/20\"")
			time.sleep(3)
			await msg.delete()
		elif not piscine_exists(month):
			msg = await ctx.send(f"<@!{ctx.author.id}>: No piscine started in {month}")
			time.sleep(3)
			await msg.delete()
		elif user_has_piscine(ctx):
			msg = await ctx.send(f"<@!{ctx.author.id}>: You already have a piscine. If needed, contact the <@&{ids.staff}>")
			time.sleep(3)
			await msg.delete()
		else:
			index = piscines.index(month)
			name_role = f"piscine-{index}" if index >= 10 else f"piscine-0{index}"
			msg = await ctx.send(f"<@!{ctx.author.id}>: {ids.success_kid_emoji}")
			time.sleep(3)
			await msg.delete()
			if not role_exists(name_role, ctx):
				# Creating role
				piscine_role = await ctx.guild.create_role(name=name_role)
				# Creating the text channel
				community = discord.utils.get(ctx.guild.categories, id=ids.community)
				new_text_channel = await ctx.guild.create_text_channel(name_role, category=community, topic=f"A cosier place to discuss with your fellow brothers in arms from the piscine :man_swimming: but remember that if you need help fixing a bug or look for people to play lol, you'll find more people available on the general channels {ids.think_emoji}")
				# Changing the permissions of the channel
				# Taking away the access to the channel from every role
				for role in ctx.guild.roles:
					await new_text_channel.set_permissions(role, read_messages=False)
				# Giving back access only to name_role (e.g. piscine-00)
				await new_text_channel.set_permissions(piscine_role, read_messages=True)
			# Assigning the role
			# Outside if statement because the assignement needs to take place either the role exists or not
			role = discord.utils.get(ctx.guild.roles, name=name_role)
			await ctx.message.author.add_roles(role)

def setup(client):
	client.add_cog(Piscine_private(client))
