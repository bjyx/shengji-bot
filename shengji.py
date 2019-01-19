import discord
from discord.ext import commands
import json
import time
import typing
from random import randint


client = commands.Bot(command_prefix='$')

# strings galore
players = []
winds = ["North (\u5317 b\u011bi)", "West (\u897f x\012b)", "South (\u5357 nán)", "East (\u6771 d\014dng)"]
numbers = ["zero", "one", "two", "three", "four", "five", "six", "seven", "eight", "nine", "keycap_ten", "regional_indicator_j", "regional_indicator_q", "regional_indicator_k", "regional_indicator_a", "trophy"]
ranks = ["", "", "2", "3", "4", "5", "6", "7", "8", "9", "10", "J", "Q", "K", "A"]
suits = ["C", "D", "H", "S"]
suits_long = ["clubs", "diamonds", "hearts", "spades", "joker"]
commandwords = ["intro", "join", "leave", "list", "start", "deal", "call", "kitty", "play", "score", "surrender", "reset"]

#settings
ruleset = 0 #bitmath... explained below
# least significant - 1: scores for 5, 10, K are now mandatory to play
# 2: chao di pi
# 4: multiply kitty by number of cards used to win last score for opponents
# 8: hook-back
# most significant - 16: red 5 rule - no implementation yet

#game data
gameStarted = False #true if game has started
score = [2, 2] #[NS, WE]
dominantSuit = -1 # “主牌” 0C 1D 2H 3S 4N
currentSuit = -1 # 0C 1D 2H 3S 4T
dealer = -1 # “庄” 0N 1W 2S 3E
turn = -1 #0N 1W 2S 3E
turncounter = 0 #0 1 2 3 looping from person with current hand
shuai = False
singles = []
doubles = []
points = 0 # “分” for non-dealer team only
cardlist = [] #temporary storage unit for the card hierarchy for card sorting purposes in sendcardssorted; determining winners goes in a different category
called = False #True if weakcalled
strongcalled = False #True if strongcalled
dealing = False #True if cards are being or have been dealt

hands = [[],[],[],[]]
plays = []
reset = [False, False, False, False] #people who want to reset
deleteque = []
deleteque2 = []
kittycards = []

#dominant suit in string form: suits[dominantSuit]
#dominant rank: ranks[score[dealer%2]]

async def sendcardssorted(i):
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
#contingency for no trumps/other (more near the end game)
    if playerhand[0] != "":
        handembed.add_field(name="Trumps",value=playerhand[0])
    if playerhand[1] != "":
        handembed.add_field(name="Others",value=playerhand[1])
    await client.send_message(players[i], "*TEMPORARY*", em=handembed)

def singledouble(cards):
	for c in cards:
		if cards.count(c) == 1:
			singles.append(c)
		elif not cardlist.index(c) in doubles:
		 	doubles.append(c)
	singles.sort(key = hierarchy(str)) #hopefully able to sort cards by order in hierarchy ._.
	doubles.sort(key = hierarchy(str))
	if len(singles) > 0:
		return False #shuǎi
	for i in range(len(doubles)-1):
		if hierarchy(doubles[i]) != hierarchy(doubles[i+1]) - 1:	#Tractor handling
			return False #shuǎi
	return True #doubles or consecutive doubles

def insuit(card, suit):
	if suit == dominantSuit:
		return hierarchy(card) > 15
	else:
		return card[1]==suits[suit]

def hierarchy(card):
	if card == "J+":
		return 31
	if card == "J-":
		return 30
	if card == ranks[score[dealer%2]] + suits[dominantSuit]: #dominant rank of dominant suit
		return 29
	if card[0] == ranks[score[dealer%2]]: #indistinguishable dominant ranks
		return 28 + (1 if dominantSuit = 4) #wú zhǔ
	if card[1] == suits[dominantSuit]:
		return 14 + ranks.index(card[0]) - (1 if ranks.index(card[0]) > score[dealer%2])
	if card[1] == suits[currentSuit]:
		return ranks.index(card[0]) - (1 if ranks.index(card[0]) > score[dealer%2])
	return 0
	#0 (not current suit not trump, cannot form tractor), 2 3 4 5 6 7 8 9 10 11 12 13 (skip trump rank), then 16, 17, 18... 27 (again skip trump rank), 28, 29, 30 (J-), 31 (J+)

def comparestructure(cards, cardcount, doublecount, tractorcount):


@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))
    await client.change_status(game=discord.Game(name="Tractor"))

async def on_server_join(server):
    dealerRole = create_role(server, name="Dealer", colour=discord.Colour.default())
    everyone_perms = discord.PermissionOverwrite(read_messages=False)
	my_perms = discord.PermissionOverwrite(read_messages=True)
    dealerChannel = create_channel(server, "dealer-den", (server.default_role, everyone_perms), (dealerRole, my_perms))

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
    if len(players) == 0:
        await ctx.bot.send_message(ctx.message.channel, 'No one to list. :shrug:')
        return
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
        await ctx.bot.send_message(ctx.message.channel, ':x: Too many playe-- wait. How did you even do that? I\'m `{0}.{1}%` confident that I had a safeguard against this scenario...'.format(randint(90,100), randint(0, 10)))
        return
    if len(players) != 4:
        await ctx.bot.send_message(ctx.message.channel, ':x: Not enough players! You need :{0}: more.'.format(numbers[4-len(players)]))
        return
    if gameStarted:
        await ctx.bot.send_message(ctx.message.channel, ':flower_playing_cards: Game has already started.')
        return
    await ctx.bot.send_message(ctx.message.channel, ':flower_playing_cards: Game has started! Please type $deal :flower_playing_cards:')
    gameStarted = True

@client.command(pass_context=True)
async def deal(ctx):
    global dealing
    if dealing:
        await ctx.bot.send_message(ctx.message.channel, ':x: We\'re already doing that!')
    if score[0]==15 or score[1]==15:
        await ctx.bot.send_message(ctx.message.channel, ':x: Please say $reset to reset the game.')
        return
    if not gameStarted:
        await ctx.bot.send_message(ctx.message.channel, ':x: Game needs to start first.')
        return
    if not ctx.message.author in players:
        await ctx.bot.send_message(ctx.message.channel, ':x: Who are you?')
        return
#   game setup area
    dealing = True
    cardFile = open('cards.txt', 'r')
    cardlist.clear()
    for i in range(54):
        cardlist.append(cardFile.readline())
	cardlist *= 2
#   success message
    await ctx.bot.send_message(ctx.message.channel, ':{0}: Dealing cards. The dominant rank is :{0}:'.format(numbers[score[dealer%2]]))
#   card dealer
    for i in range(25):
        for j in range(4):
            x = random.randint(0, len(cardlist))
            hands[(dealer+j)%4].append(cardlist.pop(x))
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
    if not dominantSuit == -1 and not strongcalled:
        await ctx.bot.send_message(ctx.message.channel, 'You have `30` seconds to override this trump suit with a double.')
        for i in range(6):
            time.sleep(5)
            if dominantSuit == -1:
                await ctx.bot.send_message(ctx.message.channel, '`{0}` seconds left.'.format((5-i)*5))
            else:
                break
#   contingency for no one calling a trump suit
    if dominantSuit == -1:
        x = random.randint(0, len(cardlist))
        if cardlist[x][-1] != '+' and cardlist[x][-1] != '-':
            dominantSuit = suits.index(x[-1])
            await ctx.bot.send_message(ctx.message.channel, 'Auto-call:')
        else:
            await ctx.bot.send_message(ctx.message.channel, 'No trump called. Type $deal to redeal.')
            for j in range(4):
                hands[j].clear()
            dealing = False
            return
    await ctx.bot.send_message(ctx.message.channel, 'The trump suit is :{0}: `{0}`.'.format(suits_long[dominantSuit]))
    await ctx.bot.add_roles(players[dealer], dealerRole)
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
	if ctx.message.channel != dealerChannel:
		await ctx.bot.delete_message(ctx.message)
		await ctx.bot.send_message(ctx.message.channel, ':x: This is the wrong place for that. Go to {0}.'.format(dealerChannel))
        return
    if len(cards) != 8:
        await ctx.bot.send_message(ctx.message.channel, ':x: There must be exactly eight cards in the kitty.')
        return
    for c in cards:
        if cards.count(c) > hands[dealer].count(c):
            await ctx.bot.send_message(ctx.message.channel, ':x: You don\'t have enough `{0}` to do this.'.format(c))
            return
    kittycards = list(cards)
    for c in kittycards:
        hands[dealer].remove(c)
    await ctx.bot.send_message(ctx.message.channel, ':o: Kitty set. You start the game (type `$play [cards]`).')
    global turn
    turn = dealer

@client.command(pass_context=True)
async def play(ctx, *cards):
    if not gameStarted:
        await ctx.bot.send_message(ctx.message.channel, ':x: No game in progress. Command unusable.')
        return
    if score[0]==15 or score[1]==15:
        await ctx.bot.send_message(ctx.message.channel, ':x: Please say $reset to reset the game.')
        return
    if not ctx.message.author in players:
        await ctx.bot.send_message(ctx.message.channel, ':x: Who are you?')
        return
    if turn == -1:
        await ctx.bot.send_message(ctx.message.channel, ':x: Please wait for the kitty to be set.')
        return
    if players[(turn+turncounter)%4] != ctx.message.author:
        await ctx.bot.send_message(ctx.message.channel, ':x: It is not your turn!')
        await ctx.bot.delete_message(ctx.message)
        return
    for c in cards:
    	if not c in cardlist:
			await ctx.bot.send_message(ctx.message.channel, ':x: That\'s not a card.'.format(c))
            return
        if cards.count(c) > hands[dealer].count(c):
            await ctx.bot.delete_message(ctx.message)
            await ctx.bot.send_message(ctx.message.channel, ':x: You don\'t have enough `{0}` to do this.'.format(c))
            return
    #card setsuit - initial
    EmbedPlay = discord.Embed(title="Played cards", description="", colour=discord.Colour.light_grey)
    if turncounter==0:
    	#determine if all cards in one suit
    	currentSuit = dominantSuit if hierarchy(cards[0]) > 15 else cards[0][1]
    	for c in cards:
    		if hierarchy(c) == 0:
				await ctx.bot.delete_message(ctx.message)
            	await ctx.bot.send_message(ctx.message.channel, ':x: Cards must be of the same suit.'.format(c))
            	return
			else if currentSuit != dominantSuit and hierarchy(c) > 15:
				await ctx.bot.delete_message(ctx.message)
            	await ctx.bot.send_message(ctx.message.channel, ':x: Cards must be of the same suit.'.format(c))
            	return
		#determine if singles, doubles, or tractor
		shuai = False if len(cards)==1 else not singledouble(cards)
		#if none of the above, make sure shuǎi is permissible
		#if not permissible, play one card/pair of cards depending on what is matched
		if shuai == True:
			for i in cardlist:
				if hierarchy(i) > hierarchy(singles[0]) and (hierarchy(singles[0]) > 15 or hierarchy(i) < 14): #same suit, and i > c
					if i in hands[1] or i in hands[3]:
						EmbedPlay.add_field(name="Shuǎi denied!", value="Another person has a card higher than `{0}`. You are now forced to play this card.".format(singles[0]))
						plays.append([singles[0]])
						break
				if hierarchy(i) > hierarchy(doubles[0]) and (hierarchy(doubles[0]) > 15 or hierarchy(i) < 14):
					if hands[1].count(i)==2 or hands[3].count(i)==2:
						EmbedPlay.add_field(name="Shuǎi denied!", value="Another person has a pair of cards higher than `{0}`. You are now forced to play this pair.".format(doubles[0]))
						plays.append([doubles[0],doubles[0]])
						break
		#play the hand
		if len(plays)==0:
			plays.append(cards)
    else:
    	#make sure they match card number else disaster happens
    	if len(cards) != len(plays[0])
		#look at cards in suit in player hand, and count cards, doubles, and tractors... (can you do that when the game starts to reduce runtime?)
		#if cards in suit >= total card count in initial hand, must match with cards in suit; else play all cards of that suit, then start playing cards of their choice
		#if doubles in suit >= total doubles in initial hand, they must play that many doubles; else doubles must equal no. doubles in hand
		#if exists a tractor of at least same size as inital tractor, must play a tractor
		#play the hand
	if turncounter == 3:
		#if structure is matched by one hand that is all trumps, goes there
		#else determine by highest card in hierarchy
		#increment point counts if opponents win
		#change who gets the turn-
    #turn shift
	if len[hands[0]] == 0 and len[hands[1]] == 0 and len[hands[2]] == 0 and len[hands[3]] == 0:
		#if dealer score 14 and dealer's team took last trick and last trick high card was an ace then make it 15 and it's game over
		#change dealer by point count
		#increase score by point count
		#if anything is bigger than 14 reduce to 14
		dealing = False
    turncounter = (turncounter + 1)%4
    await ctx.bot.send_message(ctx.message.channel, 'It is now {0.mention}\'s turn.'.format(players[(turncounter+turn)%4]))


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
        #resetting here
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
            deleteque.append(message)

with open('test.json') as f:
    token = json.load(f)

client.run(token["token"])
