import discord
from discord.ext import commands
# Line of code not needed as the bot.py already does it
# client = discord.Client()

class Roles(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.Cog.Listener()
    async def on_raw_reaction_add(payload):
        massage_id = patload.message_id
        if message_id == 778231967761563669:
            guild_id = payload.guild_id
            guild = discord.utils.find(lambda g : g.id == guild_id, client.guilds)
            role = discord.utils.get(guild.roles, name=payload.emoji.name)  

        if role is not None:
            member = discord.utils.find(lambda m : m.id == payload.user_id, guild.members)
            if memeber is not None:
                await member.add_roles(role)

    @commands.Cog.Listener()
    async def on_raw_reaction_add(payload):
        massage_id = patload.message_id
        if message_id == 778231967761563669:
            guild_id = payload.guild_id
            guild = discord.utils.find(lambda g : g.id == guild_id, client.guilds)
            role = discord.utils.get(guild.roles, name=payload.emoji.name)  

        if role is not None:
            member = discord.utils.find(lambda m : m.id == payload.user_id, guild.members)
            if memeber is not None:
                await member.remove_roles(role)

    @commands.Cog.Listener()
    async def on_raw_reaction_remove(payload):
        pass

def setup(client):
    client.add_cog(Roles(client))
