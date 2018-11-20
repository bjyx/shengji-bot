import discord
from discord.ext import commands
import json
import time
import typing
from random import randint


client = commands.Bot(command_prefix='$')

# strings galore
players = []
winds = ["North (\u5317 b\u011bi)", "East (\u6771 d\014dng)", "South (\u5357 nán)", "West (\u897f x\012b)"]
numbers = ["zero", "one", "two", "three", "four", "five", "six", "seven", "eight", "nine", "keycap_ten", "regional_indicator_j", "regional_indicator_q", "regional_indicator_k", "regional_indicator_a"]
ranks = ["", "", "2", "3", "4", "5", "6", "7", "8", "9", "10", "J", "Q", "K", "A"]
suits = ["C", "D", "H", "S"]
suits_long = ["clubs", "diamonds", "hearts", "spades"]
commandwords = ["intro", "join", "leave", "list", "start", "deal", "call", "kitty", "play", "score", "surrender", "reset"]

#game data
gameStarted = False #if game has started
score = [2, 2] #[NS, WE]
dominantSuit = -1 #0C 1D 2H 3S
dealer = -1 #0N 1E 2S 3W
turn = -1 #0N 1E 2S 3W
turncounter = 0 #0 1 2 3 looping from person with current hand
points = 0 #non-dealer team
cardlist = [] #stores card hierarchy
called = False #True if weakcalled
strongcalled = False #True if strongcalled
dealing = False #True if cards are being or have been dealt
hands = [[],[],[],[]]
reset = [False, False, False, False] #people who want to reset
deleteque = []
deleteque2 = []
kittycards = []

#dominant suit in string form: suits[dominantSuit]
#dominant rank: ranks[score[dealer%2]]

def sendcardssorted(i):
    handembed = discord.Embed(title="Your hand (sorted)", description="", colour=discord.Colour.light_grey())
    playerhand = ["", ""]
    for j in range(54):
        if hands[i].count(cardlist[j])!=0:
            if j < 18:
                if cardlist[j][1] == '+' or cardlist[j][1] == '-':
                    for k in range(hands[i].count(cardlist[j])):
                        playerhand[0] += ":black_joker::small_red_triangle{0}:\n".format("_down" if cardlist[j][1] == '-' else "")
                else:
                    for k in range(hands[i].count(cardlist[j])):
                        playerhand[0] += ":{0}::{1}:\n".format(numbers[ranks.index(cardlist[j][:-1])], suits_long[suits.index(cardlist[j][-1])])
            else:
                for k in range(hands[i].count(cardlist[j])):
                    playerhand[1] += ":{0}::{1}:\n".format(numbers[ranks.index(cardlist[j][:-1])], suits_long[suits.index(cardlist[j][-1])])
#contingency for no trumps/other (rare)
    if playerhand[0] != "":
        handembed.add_field(name="Trumps",value=playerhand[0])
    if playerhand[1] != "":
        handembed.add_field(name="Others",value=playerhand[1])
    client.send_message(players[i], "*TEMPORARY*", em=handembed)

@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))

@client.command(pass_context=True)
async def intro(ctx):
    await client.send_message(ctx.message.channel, 'https://github.com/bjyx/shengji-bot/blob/master/README.md')
    
@client.command(pass_context=True)
async def join(ctx):
    if ctx.message.author in players:
        await ctx.bot.send_message(ctx.message.channel, ':x: ' + ctx.message.author.mention + ' is already in the game!')
        return
    if score[0]==15 or score[1]==15:
        await ctx.bot.send_message(ctx.message.channel, ':x: Please say $reset to reset the game.')
        return
    if len(players) == 4:
        await ctx.bot.send_message(ctx.message.channel, ':x: Adding this player would exceed the player limit of :four:.')
        if gameStarted:
            await ctx.bot.send_message(ctx.message.channel, 'Also, you would be trying to enter a game that has already started. Not cool.')
        return
    await ctx.bot.send_message(ctx.message.channel, ':o: ' + ctx.message.author.mention + ' has joined as ' + winds[len(players)])
    players.append(ctx.message.author)

@client.command(pass_context=True)
async def leave(ctx):
    if not ctx.message.author in players:
        await ctx.bot.send_message(ctx.message.channel, ':x: Cannot leave a game you haven\'t joined yet.')
        return
    if score[0]==15 or score[1]==15:
        await ctx.bot.send_message(ctx.message.channel, ':x: Please say $reset to reset the game.')
        return
    if gameStarted:
        await ctx.bot.send_message(ctx.message.channel, ':x: Cannot leave a game in progress.')
        return
    await ctx.bot.send_message(ctx.message.channel, ':o: ' + ctx.message.author.mention + ' has left the game')
    players.remove(ctx.message.author)

@client.command(pass_context=True)
async def list(ctx):
    playerlist = discord.Embed(title="Players", description="", colour = discord.Colour.light_grey())
        
    for i in range(len(players)):
        playerlist.add_field(name = winds[i], value = players[i])
    await ctx.bot.send_message(ctx.message.channel, embed=playerlist)

@client.command(pass_context=True)
async def start(ctx):
    if score[0]==15 or score[1]==15:
        await ctx.bot.send_message(ctx.message.channel, ':x: Please say $reset to reset the game.')
        return
    if len(players) > 4:
        await ctx.bot.send_message(ctx.message.channel, ':x: Too many playe-- wait. How did you even do that?')
        return
    if len(players) != 4:
        await ctx.bot.send_message(ctx.message.channel, ':x: Not enough players! You need :{0}: more.'.format(numbers[4-len(players)]))
        return
    if score[0]==15 or score[1]==15:
        await ctx.bot.send_message(ctx.message.channel, ':x: Please say $reset to reset the game.')
        return
    if gameStarted:
        await ctx.bot.send_message(ctx.message.channel, ':flower_playing_cards: Game has already started.')
        return
    await ctx.bot.send_message(ctx.message.channel, ':flower_playing_cards: Game has started! Please type $deal :flower_playing_cards:')
    gameStarted = True

@client.command(pass_context=True)
async def deal(ctx):
    if dealing:
        await ctx.bot.send_message(ctx.message.channel, ':x: We\'re already doing that!')
    if not ctx.message.author in players:
        await ctx.bot.send_message(ctx.message.channel, ':x: Who are you?')
        return
    if score[0]==15 or score[1]==15:
        await ctx.bot.send_message(ctx.message.channel, ':x: Please say $reset to reset the game.')
        return
    if not gameStarted:
        await ctx.bot.send_message(ctx.message.channel, ':x: Game needs to start first.')
        return
#   game setup area
    dealing = True
    cardFile = open('cards.txt', 'r')
    cardlist.clear()
    for i in range(108):
        cardlist.append(cardFile.readline())
#   success message
    await ctx.bot.send_message(ctx.message.channel, ':{0}: Dealing cards. :{0}:'.format(numbers[score[dealer%2]]))
#   card dealer
    for i in range(25):
        for j in range(4):
            x = random.randint(0, len(cardlist))
            hands[j].append(cardlist.pop(x))
            if len(deleteque)>=4:
                await ctx.bot.delete_message(deleteque.pop(0))
            sendcardssorted(j)
            time.sleep(0.5) #deals each person a card every two seconds
    if dominantSuit == -1:
        await ctx.bot.send_message(ctx.message.channel, 'You have `30` seconds to call a trump suit. ')
    for i in range(6):
        time.sleep(5)
        if dominantSuit == -1:
            await ctx.bot.send_message(ctx.message.channel, '`{0}` seconds left.'.format((5-i)*5))
        else:
            break
#   contingency for no one calling a trump suit
    if dominantSuit == -1:
        x = random.randint(0, len(cardlist))
        if cardlist[x][1] != '+' and cardlist[x][1] != '-':
            dominantSuit = suits.index(x[1])
            await ctx.bot.send_message(ctx.message.channel, 'Auto-call:')
        else:
            await ctx.bot.send_message(ctx.message.channel, 'No trump called. Type $deal to redeal.')
            for j in range(4):
                hands[j].clear()
            dealing = False
            return
    await ctx.bot.send_message(ctx.message.channel, 'The trump suit is :{0}: `{0}`.'.format(suits_long[dominantSuit]))
    turn = dealer
    for i in range(8):
        hands[dealer].append(cardlist.pop(0))
#   kitty reorganization - see kitty command later
#   card sort by priority (Trumps in front, rest in back)
    for i in range(54):
        reader = cardFile.readline()
        if reader[:-1] != ranks[score[dealer%2]] and reader[-1] != suits[dominantSuit]:
            cardlist.append()
        cardlist.insert("{0}{1}".format(ranks[score[dealer%2]],suits[dominantSuit]), 2)
    for i in range(4):
        if i != dominantSuit:
            cardlist.insert("{0}{1}".format(ranks[score[dealer%2]],suits[i]),3)
    for i in range(13):
        if i+2 != score[dealer%2]:
            cardlist.insert("{0}{1}".format(ranks[i+2],suits[dominantSuit]),6)
    for i in range(4):
        sendcardssorted(i)


@client.command(pass_context=True)
async def call(ctx, suit, strong: typing.Optional[int] = 0):
    if not gameStarted:
        await ctx.bot.send_message(ctx.message.channel, ':x: Can\'t call a trump suit if there\'s no game to call the trump suit for.')
        return
    if score[0]==15 or score[1]==15:
        await ctx.bot.send_message(ctx.message.channel, ':x: Please say $reset to reset the game.')
        return
    if not ctx.message.author in players:
        await ctx.bot.send_message(ctx.message.channel, ':x: Who are you?')
        return
    if not suit in suits:
        await ctx.bot.send_message(ctx.message.channel, ':x: {0} is not a suit.'.format(suit))
        return
    if strongcalled:
        await ctx.bot.send_message(ctx.message.channel, ':x: Call is no longer possible!')
        return

    if strong != 0:
        if hands[players.index(ctx.message.author)].count("{0}{1}".format(ranks[score[dealer%2]],suit)) != 2:
            await ctx.bot.send_message(ctx.message.channel, ':x: No {0}{1} pair detected'.format(ranks[score[dealer%2]],suit))
            return
        if dealer == -1:
            dealer = players.index(ctx.message.author)
        dominantSuit = suits.index[suit]
        strongcalled = True
        called = True
        await ctx.bot.send_message(ctx.message.channel, ':o Strong declaration for `{0}` from {1}!!!'.format(suit, ctx.message.author.mention))
    else:
        if called:
            await ctx.bot.send_message(ctx.message.channel, ':x: Weak declaration already used. Type anything after a fully-phrased call command for a strong declaration.')
            return
        if hands[players.index(ctx.message.author)].count("{0}{1}".format(ranks[score[dealer%2]],suit))==0:
            await ctx.bot.send_message(ctx.message.channel, ':x: You don\'t even have {0}{1}.'.format(ranks[score[dealer%2]],suit))
            return
        if dealer == -1:
            dealer = players.index(ctx.message.author)
        dominantSuit = suits.index[suit]
        called = True
        await ctx.bot.send_message(ctx.message.channel, ':o Declaration for `{0}` from {1}!'.format(suit, ctx.message.author.mention))

@client.command(pass_context=True)
async def kitty(ctx, *cards):
    if not gameStarted:
        await ctx.bot.send_message(ctx.message.channel, ':x: No game in progress. Command unusable.')
        return
    if score[0]==15 or score[1]==15:
        await ctx.bot.send_message(ctx.message.channel, ':x: Please say $reset to reset the game.')
        return
    if not ctx.message.author in players:
        await ctx.bot.send_message(ctx.message.channel, ':x: Who are you?')
        return
    if ctx.message.author != players[dealer]:
        await ctx.bot.send_message(ctx.message.channel, ':x: You\'re not the dealer...')
        return
    if not dealing:
        await ctx.bot.send_message(ctx.message.channel, ':x: Where are your cards?')
        return
    if len(cards) != 8:
        await ctx.bot.send_message(ctx.message.channel, ':x: There must be exactly eight cards in the kitty.')
        return
    for c in cards:
        if cards.count(c) != hands[dealer].count(c):
            await ctx.bot.send_message(ctx.message.channel, ':x: You don\'t have enough `{0}` to do this.'.format(c))
            return
    kittycards = list(cards)
    for c in kittycards:
        hands[dealer].remove(c)
    await ctx.bot.send_message(ctx.message.channel, ':cat: Kitty set. You start the game (type `$play [card]`).')

@client.command(pass_context=True)
async def reset(ctx):
    if not gameStarted:
        await ctx.bot.send_message(ctx.message.channel, ':x: No game in progress. Command unusable.')
        return
    if not ctx.message.author in players:
        await ctx.bot.send_message(ctx.message.channel, ':x: Who are you?')
        return
    if reset[players.index(ctx.message.author)] == False:
        reset[players.index(ctx.message.author)] = True
        await ctx.bot.send_message(ctx.message.channel, ':ballot_box: Reset vote recorded. :{0}: more required.'.format(numbers[3-reset.count(True)]))
        if reset.count(True)==3:
        #initiate reset
            await ctx.bot.send_message(ctx.message.channel, ':gear: Reset complete.')
    else:
        reset[players.index(ctx.message.author)] = False
        await ctx.bot.send_message(ctx.message.channel, ':ballot_box: Reset vote removed. :{0}: more required.'.format(numbers[3-reset.count(True)]))

#@client.command(pass_context=True)
#async def help(ctx, command="help"):
#   if command == "help":
#       return
#   if not command in commandwords:
#        await ctx.bot.send_message(ctx.message.channel, ':x: Command not found. Use $help with no parameters to see a list of all commands.')
#        return

@client.event
async def on_message(message):
    if message.author != client.user:
        await client.process_commands(message)
    else:
        if "*TEMPORARY*" in message.content:
            deleteque.append(message.id)
        if "__TEMPORARY__" in message.content:
            deleteque2.append(message.id)

with open('test.json') as f:
    token = json.load(f)

client.run(token["token"])
