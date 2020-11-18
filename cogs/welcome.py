import discord
import requests
from discord.ext import commands

welcome_channel_id = 778322115010494544
piscineux_role_id = 778556642287026177
welcome_message = "***Welcome to the <:42_logo_white:777980207038201928> Lisbon Discord! :raised_hands:***\nI'm Moulinette, and you probably know me from previous encounters. Was I too harsh with you? :robot:\n\nHere you'll be able to find motivated people to build ambitious projects with, learn a new language, or just play Among Us :video_game: but before going any further, I need to ID you!\n\n**Login**\nIf you are a warrior that managed to survive a piscine:\nsend `.nick <42 login>`\n\nIf you have yet to do the piscine or are just curious about 42:\nsend `.role visitor`\n\n**House**\nFor *piscineux*, choose the house assigned to you during the piscine! :man_swimming:"


class Welcome(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_ready(self, channel: discord.TextChannel = None):
        channel = discord.utils.get(self.client.get_all_channels(),
                                    name='welcome')
        count = 0
        async for message in channel.history(limit=None):
            count += 1
        if count == 0:
            await channel.send(welcome_message)


def setup(client):
    client.add_cog(Welcome(client))