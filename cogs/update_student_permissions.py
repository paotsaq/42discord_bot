# What this modules does:
# awaits for a trigger to build new user database
# after getting the database, assigns permissions to view cursus channels

import logging
import discord
from discord.ext import commands
import os.path
import json

# Switch between prod and dev branches
from bot import ids

def get_database(path_to_database):
    json_file = open(path_to_database) 
    loaded_dict = json.load(json_file)
    json_file.close()
    return loaded_dict

class AssignsRole(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command()
    async def attribute_42student(self, ctx):
        logging.info("Deploying attribution of 42student role ⚙️ ")
        if ids.staff in [x.id for x in ctx.author.roles]:
            if not os.path.exists('./users_id_database.json'):
                logging.info("Database is not ready! 🚩")
                return
            users = get_database('./users_id_database.json')
            guild = self.client.get_guild(ids.guild_id)
            for user in guild.members:
                logging.info("Checking user %s\n", user.display_name)
                if user.display_name in users.keys():
                    snowflake = discord.Object(ids.student42)
                    await user.add_roles(snowflake)

def setup(client):
    client.add_cog(AssignsRole(client))
