# What this modules does:
# - Prints the "welcome" channel messages
# - Ids the user
# - Gives the user its role (piscineux or 42student, one of the houses)

import discord
import requests
import time
import datetime
from discord.ext import commands

# IDs taken from the server (to be updated once we go over to the real server)
server_id = 777686265600540682
welcome_channel_id = 778322115010494544
rules_channel_id = 779708218812137493
visitor_role_id = 778636804319608852
alliance_role_id = 778267876083761163
assembly_role_id = 778273424736649230
federation_role_id = 778273424605839381
order_role_id = 778273424727605309
student_role_id = 778636830416306216
piscineux_role_id = 778556642287026177
check_rules_id = 779748257261551617
welcome_message_id = 0
houses = {
	'alliance': alliance_role_id,
	'assembly': assembly_role_id,
	'federation': federation_role_id,
	'order': order_role_id,
}

class Welcome(commands.Cog):
	def __init__(self, client):
		self.client = client


	@commands.Cog.listener()
	async def on_ready(self, channel: discord.TextChannel = None):

		# Welcome Channel
		# Each time the bot starts, he counts the number of messages in the welcome channel
		# If 0, he adds the welcome message and the initial house reactions
		# If 1, he takes the id of the only existing message
		# In each case he saves the first message in self.reaction_message to be used later
		channel = discord.utils.get(self.client.get_all_channels(),
									id=welcome_channel_id)
		welcome_count = 0
		async for message_in_welcome in channel.history(limit=None):
			welcome_count += 1
		if welcome_count == 0:
			welcome_message = discord.Embed(title="Welcome to the <:42_logo_white:777980207038201928> Lisbon Discord!  :raised_hands:", colour=discord.Colour(0xf8e71c), description="I'm Moulinette, and you probably know me from previous encounters. Was I too harsh with you? :robot:\n\nHere you'll be able to find motivated people to build ambitious projects with, learn a new language, or just play Among Us :video_game: but before going any further, I need to ID you!", timestamp=datetime.datetime.now())
			welcome_message.set_footer(text="Powered by the community", icon_url=self.client.user.avatar_url)
			welcome_message.add_field(name="Login", value="If you are a warrior that managed to survive a piscine:\ntype `.kinit <42 login>`", inline=False)
			welcome_message.add_field(name="House", value="For _piscineux_, react to this message with the house assigned to you during the piscine! :man_swimming:", inline=False)
			message_in_welcome = await channel.send(embed=welcome_message)
			welcome_message_id = message_in_welcome.id
			await message.add_reaction('<:alliance:778315592368914464>')
			await message.add_reaction('<:assembly:778315588481187900>')
			await message.add_reaction('<:federation:778315572583989258>')
			await message.add_reaction('<:order:778315568612638730>')
		elif welcome_count == 1:
			welcome_message_id = message_in_welcome.id
		self.welcome_reaction_message = await self.client.get_channel(welcome_channel_id).fetch_message(welcome_message_id)


		# Rules Channel
		# Each time the bot starts, he counts the number of messages in the welcome channel
		# If 0, he adds the welcome message and the initial house reactions
		# If 1, he takes the id of the only existing message
		# In each case he saves the first message in self.reaction_message to be used later
		channel = discord.utils.get(self.client.get_all_channels(),
									id=rules_channel_id)
		rules_count = 0
		async for message_in_rules in channel.history(limit=None):
			rules_count += 1
		if rules_count == 0:
			rules_message = discord.Embed(title="Rules for the <:42_logo_white:777980207038201928> Lisbon Discord!", colour=discord.Colour(0xf8e71c), description="We all want the :42_logo_white: Lisbon Discord to be a good place for all. With that in mind, here are some basic guidelines to follow.", timestamp=datetime.datetime.now())
			rules_message.set_footer(text="Powered by the community", icon_url=self.client.user.avatar_url)
			rules_message.add_field(name="1. Be respectful", value="Refrain from personal attacks, derogatory language towards any particular group of people, and in general words that you would not use if not from behind a keyboard.", inline=False)
			rules_message.add_field(name="2. Be honest", value="Don't misrepresent yourself as an 42 Student or piscineur :man_swimming: Visitors are welcome and encouraged - this is also a place to learn about 42 Lisbon.", inline=False)
			rules_message.add_field(name="3. Be kind", value="We all love tech and coding, but we understand that are times when you may want to talk about something else. If so, please be mature while discussing controversial or sensitive topics, such as politics or religion.", inline=False)
			rules_message.add_field(name="4. Be smart", value="If you want to there is content that is particularly sensitive or NSFW, we expect you to follow your best judgement. Be wary of other people's sensitivities.", inline=False)
			rules_message.add_field(name="a", value="We trust you to be an exemplar member of the community. Of course, feel free to reach the staff at #bocal, or through a DM, at any time. Accept these rules by reacting with :white_check_mark:  to the message!", inline=False)
			message_in_rules = await channel.send(embed=rules_message)
			rules_message_id = message_in_rules.id
			await message_in_rules.add_reaction('✅')
		elif rules_count == 1:
			rules_message_id = message_in_rules.id
		self.rules_reaction_message = await self.client.get_channel(rules_channel_id).fetch_message(rules_message_id)

	# Identication based on whether or not the cdn link with the login inputed works or not
	# If login does work, change its login and add the role of piscineux
	# The input is immediately deleted
	# The output from the moulinette goes away after a few seconds
	@commands.command()
	async def kinit(self, ctx, login="404"):
		await ctx.channel.purge(limit=1)
		role = discord.utils.get(ctx.author.guild.roles, id=piscineux_role_id)
		url = 'https://cdn.intra.42.fr/users/{}.jpg'.format(login)
		if requests.get(url).status_code == 200:
			await ctx.message.author.edit(nick=login)
			await ctx.message.author.add_roles(role)
			await ctx.send("<:success:778612467567558667>")
			time.sleep(1)
			await ctx.channel.purge(limit=1)
		else:
			await ctx.send("Login not valid")
			time.sleep(2)
			await ctx.channel.purge(limit=1)

	# Adding the role to the user based on the reaction house in clicks on
	# Removing the role "Check Rules" to the user who react to the rules message
	@commands.Cog.listener()
	async def on_raw_reaction_add(self, payload):
		if payload.message_id == self.welcome_reaction_message.id:
			role = discord.utils.get(payload.member.guild.roles, id=houses[payload.emoji.name])
			await payload.member.add_roles(role)
		elif payload.message_id == self.rules_reaction_message.id:
			self.client.guild = self.client.get_guild(server_id)
			role = self.client.guild.get_role(check_rules_id)
			member = self.client.guild.get_member(payload.user_id)
			await member.remove_roles(role)

	# Removing the role if the user takes away the reaction
	@commands.Cog.listener()
	async def on_raw_reaction_remove(self, payload):
		if payload.message_id == self.welcome_reaction_message.id:
			self.client.guild = self.client.get_guild(server_id)
			role = self.client.guild.get_role(houses[payload.emoji.name])
			member = self.client.guild.get_member(payload.user_id)
			await member.remove_roles(role)

	# Adds the role "Check Rules" when a new user enters the server
	@commands.Cog.listener()
	async def on_member_join(self, memeber):
		await payload.member.add_roles(check_rules_id)

def setup(client):
	client.add_cog(Welcome(client))
