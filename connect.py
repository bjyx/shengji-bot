import discord
import discord.ext
import json

client = discord.Client()

players = []
winds = ["North (\u5317 b\u011bi)", "East (\u6771 d\014dng)", "South (\u5357 nán)", "West (\u897f x\012b)"]
numbers = ["zero", "one", "two", "three", "four", "five", "six", "seven", "eight", "nine", "one::zero", "regional_indicator_j", "regional_indicator_q", "regional_indicator_k", "regional_indicator_a"]
gameStarted = false
score = [2, 2]
dominantSuit = 0
dealer = -1 #0 for N and so forth

@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))

@client.event
async def on_message(message):
    if message.author == client.user:
        return
    
    if message.content.startswith('$intro'):
        await client.send_message(message.channel, 'https://github.com/bjyx/shengji-bot/blob/master/README.md')

    if message.content.startswith('$join'):
        if message.author.mention in players:
            await client.send_message(message.channel, ':x: ' + message.author.mention + ' is already in the game!')
            return
        if len(players) == 4:
            await client.send_message(message.channel, ':x: Adding this player would exceed the player limit of :four:.')
            return
        await client.send_message(message.channel, ':o: ' + message.author.mention + ' has joined as ' + winds[len(players)])
        players.append(message.author.mention)

    if message.content.startswith('$leave'):
        if not message.author.mention in players:
            await client.send_message(message.channel, ':x: Cannot leave a game you haven\'t joined yet.')
            return
        if gameStarted:
            await client.send_message(message.channel, ':x: Cannot leave a game in progress.')
            return
        await client.send_message(message.channel, ':o: ' + message.author.mention + ' has left the game')
        players.remove(message.author.mention)

    if message.content.startswith('$list'):
        playerlist = discord.Embed(title="Players", description="")
        for i in range(len(players)):
            playerlist.description += winds[i] + ' ' + players[i] + '\n'
        await client.send_message(message.channel, embed=playerlist)

    if message.content.startswith('$start'):
        if len(players) != 4:
            await client.send_message(message.channel, ':x: Not enough players! You need :four: total.')
            return
        if gameStarted:
            await client.send_message(message.channel, ':x: Game has already started.')
            return
        await client.send_message(message.channel, ':two: Starting game... :two:')
        gameStarted = true


with open('test.json') as f:
    token = json.load(f)

client.run(token["token"])
