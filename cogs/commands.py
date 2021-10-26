# What this modules does:
# - Add 2 commands to clear messages
# - Add a stop command

import discord
from discord.ext import commands
import datetime

# Switch between prod and dev branches
from bot import switch, branches
if switch == branches[0]:
	import ids_prod as ids
else:
	import ids_dev as ids

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
		if switch == branches[1] or (switch == branches[0] and ids.staff in [x.id for x in ctx.author.roles]):
			await ctx.channel.send("Logging out!")
			await self.client.close()

	# For staff only, apply a role to all users
	# Was used prior to moulinette launch. Kept for now. Might be useful again
	@commands.command()
	async def add_piscine_role(self, ctx):
		piscine_role = discord.utils.get(ctx.author.guild.roles, id=ids.first_piscine_role)
		if(ids.staff in [x.id for x in ctx.author.roles]):
			async for member in ctx.guild.fetch_members(limit=None):
				if (ids.piscineux in [x.id for x in member.roles]) or (ids.student in [x.id for x in member.roles]):
					await member.add_roles(piscine_role)

	@commands.command()
	async def fixes(self, ctx):
		# Fix first message in #welcome
		# Fetch the message
		welcome_channel = self.client.get_channel(ids.welcome)
		welcome_message = await welcome_channel.fetch_message(ids.welcome_message)


		# Prepare a new message
		new_welcome_message = discord.Embed(title=f"Welcome to the {ids.school_logo_white} Lisbon Discord! :raised_hands:", colour=discord.Colour(0xf8e71c), description="I'm Moulinette, and you probably know me from previous encounters. Was I too harsh with you? :robot:\n\nHere you'll be able to find motivated people to build ambitious projects with, learn a new language, or just play Among Us :video_game: but before going any further, I need to ID you!", timestamp=datetime.datetime(2020, 12, 1, 18, 42, 00))
		new_welcome_message.set_footer(text="Powered by the community", icon_url=self.client.user.avatar_url)
		new_welcome_message.add_field(name="\u200b", value=f"**Step :one:: Login**\n- If you are a warrior that already did a piscine:\ntype `.kinit <42 login>` (e.g. `.kinit moulinette`)\n- If you are just curious about the {ids.school_logo_white} concept, click on the 🤠 icon", inline=False)
		new_welcome_message.add_field(name="\u200b", value="**Step :two:: Select your house** (for piscineux / 42 students)\nReact to this message with the house assigned to you! :house:", inline=False)
		new_welcome_message.add_field(name="\u200b", value=f"**Step :three:: Let me know which piscine you did** (for piscineux / 42 students)\nI've prepared a private channel where you'll be only among your fellow brothers in arms from the piscine :man_swimming:\nIf that's something you would like:\ntype `.piscine <MM/YY>` (e.g. `.piscine 10/20`)\n:warning: If your piscine straddled two months, enter the month when you're piscine started", inline=False)
		new_welcome_message.add_field(name="\u200b", value=f"**Step :four:: Mute this channel**\nThere will be a lot of messages in the <#{ids.welcome}> channel so for your own sanity, I recommend you to mute this channel. To do so:\n- On your computer :computer:: right-click the <#{ids.welcome}> channel > Mute Channel > Until I turn it back on\n- On your phone :mobile_phone:: long-press on the <#{ids.welcome}> channel > Mute <#{ids.welcome}> > Until I turn it back on", inline=False)

		# Edit the message
		await welcome_message.edit(embed=new_welcome_message)

		# Fix second message in #welcome
		# Fetch the message
		congrats_message = await welcome_channel.fetch_message(ids.congrats_message)

		# Prepare a new message
		new_congrats_message = discord.Embed(title="Two weeks have passed since your piscine and the results are up? :scream:", colour=discord.Colour(0xf8e71c), description=f"*If the results have yet to arrive in your inbox (or spam), don't worry, they probably are on their way. In the meantime, feel free to kill some time here* :video_game:\n\nAre you part of the lucky few that got in? On behalf of all the 42 Lisboa community (and my friend the Norminette), we congratulate you for this amazing feat {ids.success_kid_emoji}\n**To change your role from \"piscineux\" to \"42student\", react to this message with the {ids.school_logo_white} logo**\n\nIf not, fear not. The community will always be here for you and you can still try again next year stronger than ever {ids.think_emoji}\n\nN.B. there are no private channels only for 42 students, the role \"42student\" exists only for convinience in case someone wants to mention all 42 students at once {ids.shipit_emoji}", timestamp=datetime.datetime(2020, 12, 1, 18, 42, 00))
		new_congrats_message.set_footer(text="Powered by the community", icon_url=self.client.user.avatar_url)

		# Edit the message
		await congrats_message.edit(embed=new_congrats_message)

	@commands.command()
	async def list_users(self, ctx):
		print(self.client.users)

def setup(client):
	client.add_cog(Commands(client))
