import discord
from urllib.request import urlopen
client = discord.Client()

@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.content.startswith('Amo-te'):
        await message.channel.send('só amo o Miguel Gueifão...!')

    if "slack" in message.content:
        await message.channel.send('do you miss the :rotating_light: slack police :rotating_light:')

    if "vs code" in message.content:
        await message.channel.send('Hey! Here are the :rotating_light: top 10 :boom: reasons to use VSCode: \n (null)')

    if client.event.channel.name == "general"
        if "/nick"in message.content:
            nick = message.split()
            url = 'https://cdn.intra.42.fr/users/%7B0%7D.jpg', nick[1]
            check = urllib.urlopen(url)
client.run("Nzc3NjQwNDQ0NDk4MjgwNDU4.X7GYGQ.N7yiq0mVef0Y8Va4NKIecFz4hqk")
