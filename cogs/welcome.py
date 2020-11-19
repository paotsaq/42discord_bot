import discord
import requests
import time
import datetime
from discord.ext import commands

welcome_channel_id = 778322115010494544
visitor_role_id = 778636804319608852
alliance_role_id = 778267876083761163
assembly_role_id = 778273424736649230
federation_role_id = 778273424605839381
order_role_id = 778273424727605309
student_role_id = 778636830416306216
piscineux_role_id = 778556642287026177
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
	async def on_member_join(self, member):
		channel = member.guild.system_channel
		if channel is not None:
			await channel.send('Welcome {0.mention}.'.format(member))
	# async def on_member_join(self, member):
	# 	channel = member.guild.system_channel
	# 	if channel is not None:
	# 		await channel.send('Welcome {0.mention}.'.format(member))
		# print("test")
		# role = discord.utils.get(member.server.roles, id=visitor_role_id)
		# print(role)
		# await discord.Member.add_roles(member, role)

	@commands.Cog.listener()
	async def on_ready(self, channel: discord.TextChannel = None):
		channel = discord.utils.get(self.client.get_all_channels(),
									id=welcome_channel_id)
		count = 0
		async for message in channel.history(limit=None):
			count += 1
		if count == 0:
			welcome_message = discord.Embed(title="Welcome to the <:42_logo_white:777980207038201928> Lisbon Discord!  :raised_hands:", colour=discord.Colour(0xf8e71c), description="I'm Moulinette, and you probably know me from previous encounters. Was I too harsh with you? :robot:\n\nHere you'll be able to find motivated people to build ambitious projects with, learn a new language, or just play Among Us :video_game: but before going any further, I need to ID you!", timestamp=datetime.datetime.now())
			welcome_message.set_footer(text="Powered by the community", icon_url=self.client.user.avatar_url)
			welcome_message.add_field(name="Login", value="If you are a warrior that managed to survive a piscine:\ntype `.kinit <42 login>`", inline=False)
			welcome_message.add_field(name="House", value="For _piscineux_, react to this message with the house assigned to you during the piscine! :man_swimming:", inline=False)
			message = await channel.send(embed=welcome_message)
			welcome_message_id = message.id
			await message.add_reaction('<:alliance:778315592368914464>')
			await message.add_reaction('<:assembly:778315588481187900>')
			await message.add_reaction('<:federation:778315572583989258>')
			await message.add_reaction('<:order:778315568612638730>')
		elif count == 1:
			welcome_message_id = message.id
		self.reaction_message = await self.client.get_channel(welcome_channel_id).fetch_message(welcome_message_id)

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

	@commands.Cog.listener()
	async def on_raw_reaction_add(self, payload):
		if payload.message_id == self.reaction_message.id:
			role = discord.utils.get(payload.member.guild.roles, id=houses[payload.emoji.name])
			# print(role)
			await payload.member.add_roles(role)

	@commands.Cog.listener()
	async def on_raw_reaction_remove(self, payload):
		if payload.message_id == self.reaction_message.id:
			# member = self.get_member(payload.user_id)
			# member = discord.utils.get(self.client.get_all_members(), id=payload.user_id)
			member = await self.client.fetch_user(payload.user_id)
			# print(member)
			# print(payload.user_id)
			# guild = self.client.get_guild(discord.server)
			# member = guild.get_member(payload.user_id)
			# member = discord.utils.get(discord.Member, id=payload.user_id)
			# print("test")
			# role = await .Guild.get_role(self, role_id=houses[payload.emoji.name])
			# role = discord.utils.get(member.guild.roles, id=houses[payload.emoji.name])
			# print(role)
			# await member.remove_roles(role)

def setup(client):
	client.add_cog(Welcome(client))
