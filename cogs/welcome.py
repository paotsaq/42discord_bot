import discord
import requests
import time
from discord.ext import commands

welcome_channel_id = 778322115010494544
visitor_role_id = 778636804319608852
student_role_id = 778636830416306216
piscineux_role_id = 778556642287026177
welcome_message = "***Welcome to the <:42_logo_white:777980207038201928> Lisbon Discord!  :raised_hands:***\nI'm Moulinette, and you probably know me from previous encounters. Was I too harsh with you? :robot:\n\nHere you'll be able to find motivated people to build ambitious projects with, learn a new language, or just play Among Us :video_game: but before going any further, I need to ID you!\n\n**Login**\nIf you are a warrior that managed to survive a piscine:\nsend `.nick <42 login>`\n\nIf you have yet to do the piscine or are just curious about 42:\nsend `.role visitor`\n\n**House**\nFor *piscineux*, react to this message with the house assigned to you during the piscine! :man_swimming:"


class Welcome(commands.Cog):
	def __init__(self, client):
		self.client = client

	welcome_message_id = 0

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
			message = await channel.send(welcome_message)
			welcome_message_id = message.id
		await message.add_reaction('<:alliance:778315592368914464>')
		await message.add_reaction('<:assembly:778315588481187900>')
		await message.add_reaction('<:federation:778315572583989258>')
		await message.add_reaction('<:order:778315568612638730>')

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


def setup(client):
	client.add_cog(Welcome(client))
