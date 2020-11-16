import discord

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
        await message.channel.send('do you miss the 🚨 slack police 🚨')

    if "vs code" in message.content:
        await message.channel.send('Hey! Here are the 🚨 top 10 💥 reasons to use VSCode: \n (null)')

client.run("Nzc3NjQwNDQ0NDk4MjgwNDU4.X7GYGQ.N7yiq0mVef0Y8Va4NKIecFz4hqk")
