import discord
from urllib.request import urlopen
from discord.ext import commands


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

        # elif client.event.channel.name == 'welcome':
        #     if message.content.startswith('/nick'):
        #         nick = message.split()
        #         url = 'https://cdn.intra.42.fr/users/%7B0%7D.jpg', nick[1]
        #         check = urllib.urlopen(url)

        # Line needed at the end of @client.event if we want to run @commands.command in this file
        # await self.client.process_commands(message)


def setup(client):
    client.add_cog(Message(client))