import discord

client = discord.Client()

@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))

@client.event
async def on_message(message):
    if message.content.startswith('$hello'):
        await message.channel.send('Hello!')


client.run("Nzc3NjQwNDQ0NDk4MjgwNDU4.X7GYGQ.N7yiq0mVef0Y8Va4NKIecFz4hqk")
