# What this modules does:
# - Cycles through all the cogs and runs them
# - Gives the users 3 commands (load, unload, reload) to work with the cogs

# Each cog has the same structure:
# class cog_name(commands.Cog):
# 	def __init__(self, client):
# 		self.client = client

# Whatever you want him to do

# def setup(client):
# 	client.add_cog(cog_name(client))

# There are two main types of events:
# - @commands.command(): response to a command following the pattern defined in bot.py (i.e. .<command name>)
# - @commands.Cog.listener(): basically every other event like a message is sent or the bot starts

from scripts.make_user_database import *
from dotenv import load_dotenv
import discord
import os, sys
from discord.ext import commands
import logging_setup

load_dotenv()

# Define environments in dictionary to allow for scaling
environments = {
	'prod': {
		'Branch': 'Production',
		'Token': 'TOKEN_PROD'},
	'dev': {
		'Branch': 'Development',
		'Token': 'TOKEN_DEV',}}

# Verify that only one argument was passed and exit if more than one or none.
provided_args = len(sys.argv)
if provided_args > 2:
	logging.error("Too many arguments provided. Enter exactly one argument.")
	exit()
elif provided_args == 1:
	logging.error("Please provide an environment to work in.")
	exit()

# Verify that the provided argument is a working environment
# Log the environment being used and grab the matching token
if sys.argv[1] in list(environments.keys()):
	argument = sys.argv[1]
	logging.info(f"Running on {environments[argument]['Branch']}")
	token = os.environ.get(environments[argument]['Token'])
else:
	logging.error(f"Unrecognized environment: {sys.argv[1]}")
	exit()

# Gives the bots additionnal permissions
# Defines the prefix for commands
intents = discord.Intents().all()
client = commands.Bot(command_prefix = '.', intents=intents)

@client.command()
async def load(ctx, extension):
	client.load_extension(f'cogs.{extension}')

@client.command()
async def unload(ctx, extension):
	if('staff' in [x.name for x in ctx.author.roles]):
		client.unload_extension(f'cogs.{extension}')

@client.command()
async def reload(ctx, extension):
	client.unload_extension(f'cogs.{extension}')
	client.load_extension(f'cogs.{extension}')

for filename in os.listdir('./cogs'):
	if filename.endswith('.py'):
		client.load_extension(f'cogs.{filename[:-3]}')

create_user_database()
client.run(token)
