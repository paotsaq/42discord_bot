import discord
from discord.ext import commands, tasks
from itertools import cycle

status = cycle([
    'chess with Norminette', 'csgo  with Norminette', 'lol with Norminette',
    'Among Us with Norminette'
])


class Ready(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_ready(self):
        self.change_status.start()
        print('We have logged in as {0.user}'.format(self.client))

    @tasks.loop(seconds=10)
    async def change_status(self):
        await self.client.change_presence(activity=discord.Game(next(status)))


def setup(client):
    client.add_cog(Ready(client))