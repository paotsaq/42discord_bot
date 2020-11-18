import discord
import os
from discord.ext import commands

# The second client assignation seems to work as the first but also allows to set the command prefix
# client = discord.Client()
client = commands.Bot(command_prefix = '.')

intents = discord.Intents.default()
intents.members = True

@client.event
async def on_member_join(member):
	await member.send("Welcome!")

@client.command()
async def load(ctx, extension):
	client.load_extension(f'cogs.{extension}')

@client.command()
async def unload(ctx, extension):
	client.unload_extension(f'cogs.{extension}')

@client.command()
async def reload(ctx, extension):
	client.unload_extension(f'cogs.{extension}')
	client.load_extension(f'cogs.{extension}')

for filename in os.listdir('./cogs'):
	if filename.endswith('.py'):
		client.load_extension(f'cogs.{filename[:-3]}')

client.run("Nzc3NjQwNDQ0NDk4MjgwNDU4.X7GYGQ.N7yiq0mVef0Y8Va4NKIecFz4hqk")
