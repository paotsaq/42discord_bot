# What this modules does:
# - Prints the "welcome" channel messages
# - Ids the user
# - Gives the user its role (piscineux or 42student, one of the houses)

import discord
import requests
import time
import datetime
from discord.ext import commands
import text_messages as tm

# Switch between prod and dev branches
from bot import switch, branches
if switch == branches[0]:
	import ids_prod as ids
else:
	import ids_dev as ids

# If houses also has the visitor, it's to not over-complicate the remove on_raw_reaction_remove function

house_names = ["order", "federation", "alliance", "assembly", "visitor"]

houses = {
	'visitor': {
		"id": ids.visitor,
		"logo": "🤠"
		},
	'alliance': {
		"id": ids.alliance,
		"logo": ids.alliance_logo
		},
	'assembly': {
		"id": ids.assembly,
		"logo": ids.assembly_logo
		},
	'order': {
		"id": ids.order,
		"logo": ids.order_logo
		},
	'federation': {
		"id": ids.federation,
		"logo": ids.federation_logo
		}
}

house_logos = [houses[house]["logo"] for house in houses]

async def add_reactions_to_message(message, reactions):
	"""Reactions is a list of discord emojis"""
	for reaction in reactions:
		await message.add_reaction(reaction)

class Welcome(commands.Cog):
	def __init__(self, client):
		self.client = client

	async def make_welcome_message(self, channel):
		welcome_message_embed = discord.Embed(
				title=tm.WELCOME_MESSAGE_TITLE,
				colour=discord.Colour(0xf8e71c),
				description=tm.WELCOME_MESSAGE_INTRO, timestamp=datetime.datetime.now())
		welcome_message_embed.set_footer(text="Powered by the community", icon_url=self.client.user.avatar_url)
		welcome_message_embed.add_field(name="1. Login", value="If you are a warrior that already did a piscine:\ntype `.kinit <42 login>`\n\nIf you are just curious about the 42 concept, click on the 🤠 icon", inline=False)
		welcome_message_embed.add_field(name="2. House", value="For _piscineux_, react to this message with the house assigned to you during the piscine! :man_swimming:", inline=False)
		welcome_message = await channel.send(embed=welcome_message_embed)
		await add_reactions_to_message(welcome_message, house_logos)
		# Add 2 attributes to self for the function on_raw_reaction_add
		self.welcome_message = await self.client.get_channel(ids.welcome).fetch_message(welcome_message.id)

	@commands.Cog.listener()
	async def on_ready(self, channel: discord.TextChannel = None):
		channel = discord.utils.get(self.client.get_all_channels(),
									id=ids.welcome)

		# Writing the welcome_message and adding its reactions
		message_count = 0
		async for message in channel.history(limit=None):
			message_count += 1
		if message_count == 0:
			await self.make_welcome_message(channel)
		elif message_count == 1:
			self.welcome_message = await self.client.get_channel(ids.welcome).fetch_message(783402706840190996)
		# Rules Channel
		# Each time the bot starts, he counts the number of messages in the welcome channel
		# If 0, he adds the welcome message and the initial house reactions
		# If 1, he takes the id of the only existing message
		# In each case he saves the first message in self.reaction_message to be used later
		channel = discord.utils.get(self.client.get_all_channels(),
									id=ids.rules)
		rules_count = 0
		async for message_in_rules in channel.history(limit=None):
			rules_count += 1
		if rules_count == 0:
			rules_message = discord.Embed(title=f"Rules for the {ids.school_logo_white} Lisbon Discord!", colour=discord.Colour(0xf8e71c), description=f"We all want the {ids.school_logo_white} Lisbon Discord to be a good place for all. With that in mind, here are some basic guidelines to follow.", timestamp=datetime.datetime.now())
			rules_message.set_footer(text="Powered by the community", icon_url=self.client.user.avatar_url)
			rules_message.add_field(name="1. Be respectful", value="Refrain from personal attacks, derogatory language towards any particular group of people, and in general words that you would not use if not from behind a keyboard.", inline=False)
			rules_message.add_field(name="2. Be honest", value="Don't misrepresent yourself as an 42 Student or piscineur :man_swimming: Visitors are welcome and encouraged - this is also a place to learn about 42 Lisbon.", inline=False)
			rules_message.add_field(name="3. Be kind", value="We all love tech and coding, but we understand that are times when you may want to talk about something else. If so, please be mature while discussing controversial or sensitive topics, such as politics or religion.", inline=False)
			rules_message.add_field(name="4. Be smart", value="If you want to there is content that is particularly sensitive or NSFW, we expect you to follow your best judgement. Be wary of other people's sensitivities.", inline=False)
			rules_message.add_field(name="\u200b", value="We trust you to be an exemplar member of the community. Of course, feel free to reach the staff at #bocal, or through a DM, at any time. Accept these rules by reacting with :white_check_mark:  to the message!", inline=False)
			message_in_rules = await channel.send(embed=rules_message)
			rules_message_id = message_in_rules.id
			await message_in_rules.add_reaction('✅')
		elif rules_count == 1:
			rules_message_id = message_in_rules.id
		self.rules_reaction_message = await self.client.get_channel(ids.rules).fetch_message(rules_message_id)

	# Identication based on whether or not the cdn link with the login inputed works or not
	# If login does work, change its login and add the role of piscineux
	# The input is immediately deleted
	# The output from the moulinette goes away after a few seconds
	@commands.command()
	async def kinit(self, ctx, login="404"):
		await ctx.message.delete()
		url = 'https://cdn.intra.42.fr/users/{}.jpg'.format(login)
		if requests.get(url).status_code == 200:
			# Removing the visitor role (even if he doesn't have it)
			# Creating the attribute guild to self.client. Here guild is the server
			self.client.guild = self.client.get_guild(ids.server)
			role = self.client.guild.get_role(ids.visitor)
			member = self.client.guild.get_member(ctx.message.author.id)
			await member.remove_roles(role)
			# Checking if user already has 42student role. If so, don't add piscineux role
			for role in member.roles:
				if role.id == ids.student:
					msg = await ctx.send(f"<@!{ctx.author.id}>: Already 42 student. Login unnecessary")
					time.sleep(3)
					await msg.delete()
					return
			# Adding the piscineux role, if he does not have the student role
			role = discord.utils.get(ctx.author.guild.roles, id=ids.piscineux)
			await ctx.message.author.edit(nick=login)
			await ctx.message.author.add_roles(role)
			msg = await ctx.send(f"<@!{ctx.author.id}>: {ids.success_kid_emoji}")
			time.sleep(3)
			await msg.delete()
		else:
			msg = await ctx.send(f"<@!{ctx.author.id}>: Login not valid")
			time.sleep(3)
			await msg.delete()

	# Adding the role to the user based on the reaction house in clicks on
	# Removing the role "Check Rules" to the user who react to the rules message
	@commands.Cog.listener()
	async def on_raw_reaction_add(self, payload):
		if payload.member == self.client.user:
			return
		if payload.message_id == self.welcome_message.id:
			# Case where user clicks on visitor
			if payload.emoji.name == '🤠':
				# Parsing user's roles to make sure is neither a student nor a piscineux
				for member_role in payload.member.roles:
					if member_role.id in (ids.piscineux, ids.student):
						await self.welcome_message.remove_reaction(payload.emoji, payload.member)
						return
				# If not student, assign visitor role
				role = discord.utils.get(payload.member.guild.roles, id=ids.visitor)
				await payload.member.add_roles(role)
			# Case where user clicks on a house
			elif payload.emoji.name in houses:
				# Check if user has already a house AND is a student or piscineux
				check = 0
				for member_role in payload.member.roles:
					if str(member_role) in houses:
						await self.welcome_message.remove_reaction(payload.emoji, payload.member)
						return
					elif member_role.id in (ids.piscineux, ids.student):
						check = 1
				if check == 0:
					await self.welcome_message.remove_reaction(payload.emoji, payload.member)
					channel = self.client.get_channel(ids.welcome)
					msg = await channel.send(f"<@!{payload.member.id}>: Not logged in. Please use `.kinit <42 login>`")
					time.sleep(3)
					await msg.delete()
					return
				# If check good, assign house
				role = discord.utils.get(payload.member.guild.roles, id=houses[payload.emoji.name])
				await payload.member.add_roles(role)
		elif payload.message_id == self.congrats_message.id:
			# Parsing user's roles to make sure he is a piscineux
			check = 0
			for member_role in payload.member.roles:
				if member_role.id == ids.piscineux:
					check = 1
			if check == 0:
				await self.congrats_message.remove_reaction(payload.emoji, payload.member)
				channel = self.client.get_channel(ids.welcome)
				msg = await channel.send(f"<@!{payload.member.id}>: Not logged in. Please use `.kinit <42 login>`")
				time.sleep(3)
				await msg.delete()
				return
			else:
				# Remove role piscineux
				# Creating the attribute guild to self.client. Here guild is the server
				self.client.guild = self.client.get_guild(ids.server)
				role = self.client.guild.get_role(ids.piscineux)
				member = self.client.guild.get_member(payload.user_id)
				await member.remove_roles(role)
				# Add role 42student
				role = discord.utils.get(payload.member.guild.roles, id=ids.student)
				await payload.member.add_roles(role)
		elif payload.message_id == self.rules_reaction_message.id:
			if payload.emoji.name == '✅':
				# Creating the attribute guild to self.client. Here guild is the server
				self.client.guild = self.client.get_guild(ids.server)
				role = self.client.guild.get_role(ids.check_rules)
				member = self.client.guild.get_member(payload.user_id)
				await member.remove_roles(role)

	# Removing the role if the user takes away the reaction
	@commands.Cog.listener()
	async def on_raw_reaction_remove(self, payload):
	# Creating the attribute guild to self.client. Here guild is the server
		self.client.guild = self.client.get_guild(ids.server)
		member = self.client.guild.get_member(payload.user_id)
		if payload.message_id == self.welcome_message.id:
			role = self.client.guild.get_role(houses[payload.emoji.name])
			await member.remove_roles(role)
		elif payload.message_id == self.congrats_message.id:
			role_student = self.client.guild.get_role(ids.student)
			role_piscineux = self.client.guild.get_role(ids.piscineux)
			await member.remove_roles(role_student)
			await member.add_roles(role_piscineux)

	# Adds the role "Check Rules" when a new user enters the server
	@commands.Cog.listener()
	async def on_member_join(self, member):
		role = discord.utils.get(member.guild.roles, id=ids.check_rules)
		await member.add_roles(role)

	# Prevent users to send messages on #welcome that are not .kinit or .piscine
	@commands.Cog.listener()
	async def on_message(self, message):
		if message.author == self.client.user:
			return
		elif message.channel.id == ids.welcome and not (message.content.startswith('.kinit') or message.content.startswith('.piscine')):
			await message.channel.purge(limit=1)
			return

def setup(client):
	client.add_cog(Welcome(client))
