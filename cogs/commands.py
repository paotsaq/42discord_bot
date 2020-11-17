import discord
from discord.ext import commands


class Commands(commands.Cog):
    def __init__(self, client):
        self.client = client

    # Actually I don't think we need it for what we discussed as /nick is already a Discord command. Still handy mecanism for a bot to have
    @commands.command()
    async def ping(self, ctx):
        await ctx.send('Pong!')

    # Clears a given number of lines. 1 being the default if no number is given as parameter
    @commands.command()
    async def clear(self, ctx, amount=1):
        await self.ctx.channel.purge(limit=amount)


def setup(client):
    client.add_cog(Commands(client))