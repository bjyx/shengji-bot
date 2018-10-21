import discord
import json

client = discord.Client()

@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))

@client.event
async def on_message(message):
    if message.author == client.user:
        return
    
    if message.content.startswith('$intro'):
        await client.send_message(message.channel, 'https://github.com/bjyx/shengji-bot/blob/master/README.md')

with open('test.json') as f:
    token = json.load(f)

client.run(token["token"])
