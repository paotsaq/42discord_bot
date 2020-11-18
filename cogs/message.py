import discord
import requests
from discord.ext import commands

welcome_channel_id = 778322115010494544
piscineux_role_id = 778556642287026177


class Message(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author == self.client.user:
            return
        elif message.content.startswith('Amo-te'):
            await message.channel.send('só amo o Miguel Gueifão...!')
        elif "slack" in message.content:
            await message.channel.send(
                'do you miss the :rotating_light: slack police :rotating_light:'
            )
        elif "vs code" in message.content:
            await message.channel.send(
                'Hey! Here are the :rotating_light: top 10 :boom: reasons to use VSCode: \n(null)'
            )
        elif message.channel.id == welcome_channel_id:
            if message.content.startswith('.nick'):
                role = discord.utils.get(message.author.guild.roles,
                                         id=piscineux_role_id)
                nick = message.content.split()
                url = 'https://cdn.intra.42.fr/users/{}.jpg'.format(nick[1])
                if requests.get(url).status_code == 200:
                    await message.channel.send("You actually did the piscine!")
                    await message.author.edit(nick=nick[1])
                    await message.author.add_roles(role)
                else:
                    await message.channel.send("Login not valid")

        # Line needed at the end of @client.event if we want to run @commands.command in this file
        # await self.client.process_commands(message)


def setup(client):
    client.add_cog(Message(client))
