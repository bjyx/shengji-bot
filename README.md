# shengji-bot
### Made for the purpose of playing bā shí fēn shēng jí (80-point upgrade/tractor) by `[REDACTED]`. *Bot is buggy and may not reflect the actual game of shēngjí.*

## Command list
### Anytime
`$intro` - Probably how you got here. Sends a link directing you to this file.

### Before game starts
`$join` - Join a game as the first available wind. Winds in order are North, West, South, East. The order determines teams (North with South and East with West.)

`$leave` - Has the opposite effect of join - leave the game. Any people occupying winds behind you are moved up by one, an implementation that will probably be fixed soon.

`$list` - Lists all players in the current game (and associated wind). 

`$start` - Starts the game! 

### During game
`$deal` - Starts the dealing process. A card will be dealt to a person every two seconds.

`$call <suit> [strong]` - Can be used at any time during the dealing process. `suit` must be a suit shorthand (see Appendix A). `strong`, if included and anything besides 0, will perform a strong call (see Appendix B). Otherwise, it's a weak call. *Each call type can only be done once per deal cycle, and weak calls cannot be done after a strong call.*

`$kitty <*cards>` - Sets the kitty (see Appendix B). `cards` must contain eight arguments, each one an acceptable card in your hand (see Appendix A).

`$play <*cards>` - Plays the cards specified. `cards` can contain any number of elements.

`$score` - Shows the scoreboard (see Appendix B).

`$surrender` - A way to say you're a bad player.

`$reset` - Casts a vote to reset the game. *Resetting requires the approval of three people currently in the game.*

## Appendix A: Formatting

Cards are expressed as two alphanumeric characters (with the exception of tens), in order the rank and the suit (with the exception of Jokers).

Examples:
`2C` = Two of Clubs
`4D` = Four of Diamonds
`8H` = Eight of Hearts
`10C` = Ten of Clubs
`QS` = Queen of Spades
`AD` = <abbr title="Star of India">Ace of Diamonds</abbr>
`J-` = Black Joker
`J+` = Red Joker
 
 Suits are simply the last letter of each (again, excepting Jokers). 

## Appendix B: How to play tractor/shēng jí

**Shēng jí** (lit. upgrade, also known as **tuō lā jī**/**tractor**) is a trick-taking game (much like bridge). Any number of decks can be used in this game, but this bot handles the two-deck variant.

The game requires four players, sitting in a circle. Two people sitting opposite each other are on a *team*.

At game start, each team is at a *score* of 2. Teams can increase this score by winning rounds.

### Round structure

The dominant rank for each round is the score of the team of the current dealer. This dealer is determined by the results of previous rounds as follows:

* In the first round, whoever declares a trump first immediately becomes the dealer, with his team becoming declarers.
* In subsequent rounds, if the declarers won the previous round, the previous dealer's partner becomes dealer; otherwise, the other team becomes the declarers, and the person to the previous dealer's right becomes the new dealer. 

Cards are not dealt in this game, rather drawn - the bot attempts to simulate this by dealing one card every half-second. At any time during the drawing process, a player can declare a suit to be trump by revealing a card with the dominant rank; that card's suit is now the *trump suit*. (This is the *weak declaration* mentioned above.) 

Revealing two of the same card (both of the dominant rank) will cancel any prior weak declaration.

*In the regular game, revealing a pair of jokers will declare no-trump rounds. This is not currently supported by this bot, but it may be implemented in the future.*

After everyone has drawn 25 cards, the dealer integrates the remaining eight cards into his hand, and will choose eight cards from his hand to discard. These cards are known as the *kitty*, and will not be used in the upcoming round until the end. 

Play then starts with the dealer, who may lead a trick of any number of cards, which the other players must match:

* Doubles require other doubles in the same suit to be played (if no doubles, then singles in the same suit).
* Tractors (consecutive doubles; see Appendix C) require first tractors, then doubles, then singles in the same suit.
* Other plays are considered *shuǎi* (throws), and can *only* be played when the cards cannot be proven to not be the largest in their suit.
* * If someone does have cards that can beat a single or double in this play (and note they have to be in the same suit), the player that led the trick *must* take back every other card and play the lowest in that category. (see Appendix D)
* If a player is out of cards in a certain suit, the player can play a card from a different suit; unless the card is a trump, the card has the lowest possible priority.

The person with the highest play takes the trick and (if they are not on the declarers' team) any *points* associated with it. Points are calculated for a trick by the number of `5`s, `10`s, and `K`s among the cards in the trick (`5` worth 5 points each, `10` and `K` 10 points each.)

Only the opponents (aka not declarers) actually count their points. If the opponents win the last trick, the cards in the kitty are revealed, and the points underneath doubled and added to the total.

### Result of each round

If the opponents have:			Then the declarers are:		And their score increases by:

* 0 points						Declarers					+3
* 5-35 points					Declarers					+2
* 40-75 points					Declarers					+1
* 80-115 points				Opponents				0
* 120-155 points				Opponents				+1
* 160-195 points				Opponents				+2
* at least 200 points			Opponents				+3

## Appendix C: What is a tractor?

Assume, for the sake of argument, that the trumps are `9C`.

Tractors:
`5H 5H 4H 4H`
`6D 6D 5D 5D 4D 4D 3D 3D`
`8C 8C 7C 7C 6C 6C`
`10S 10S 8S 8S`
`9C 9C 9D 9D AC AC`
`J+ J+ J- J- 9C 9C`

Not tractors:
`5D 5D 4S 4S` (not the same suit)
`6D 6D 4D 4D` (not consecutive)
`9H 9H 8H 8H` (trumps + non-trumps)
`9H 9H 9D 9D` (equal rank trumps)
`9C 9C 8C 8C` (not consecutive)

## Appendix D: Rules regarding shuǎi

Again, assume, for the sake of argument, that the trumps are `9C`.

Leader: `KD QD`

`KD XX`: Leader must play only `QD`.
`AD XX`: Leader must play only `QD`.
`10C 3C`: Leader need not take back cards, but person playing this hand uses trumps to take the trick.

Leader: `KD QD QD 10D 10D`

`AD XX XX XX XX`: Leader must play only `KD`.
`JD JD XX XX XX`: Leader must play only `10D 10D`.
`8C 8C 5C 5C JC`: Leader need not take back cards, but person playing this hand uses trumps to take the trick. A person with higher trump doubles may take the trick. If equally ranked, the first person to play takes the trick.
