package commands;

import java.util.Arrays;
import java.util.List;

import cards.CardList;
import cards.HandManager;
import game.GameData;
import game.PlayerList;
import net.dv8tion.jda.core.events.message.MessageReceivedEvent;

public class CallCommand extends Command {
	private static final List<String> acceptable=Arrays.asList("N","C","D","H","S");
	@Override
	public void onCommand(MessageReceivedEvent e, String[] args) {
		if (GameData.hasGameEnded()) {
			sendMessage(e, ":x: Have you tried turning it off and on again?");
			return;
		}
		if (!GameData.hasGameStarted()) {
			sendMessage(e, ":x: `404 GAME NOT FOUND`"); 
			return;
		}
		if (!GameData.isDealing()) {
			sendMessage(e, ":x: There's a time and place for everything, but not now.");  //oak
			return;
		}
		if (!PlayerList.getArray().contains(e.getAuthor())) {
			sendMessage(e, ":x: Who *are* you? I don't blame you..."); //turrets
			return;
		}
		if (args.length>=2) {
			sendMessage(e, ":x: Don't overload my algorithms--a maximum of two arguments are needed here.");
			return;
		}
		if (args.length==0) {
			sendMessage(e, ":x: Your orders, sir/ma'am?");
			return;
		}
		if (!acceptable.contains(args[0].toUpperCase())) {
			sendMessage(e, ":x: Too bad that's not a valid argument. Use one of N(o trump), C(lubs), D(iamonds), H(earts), or S(pades).");
			return;
		}
		int s = acceptable.indexOf(args[0].toUpperCase());
		boolean i = (args.length==2?true:false);
		if (s==0) {
			i=true;
			if (!(HandManager.containspair(PlayerList.getArray().indexOf(e.getAuthor()), 15, 0))||!(HandManager.containspair(PlayerList.getArray().indexOf(e.getAuthor()), 16, 0))) {
				sendMessage(e, ":x: Can you prove you have a pair of jokers?");
				return;
			}
		}
		else {
			if (i) {
				if (!(HandManager.containspair(PlayerList.getArray().indexOf(e.getAuthor()), GameData.getDominantRank(), s))) {
					sendMessage(e, ":x: Can you prove you have that pair of cards?");
					return;
				}
			}
			else {
				if (!(HandManager.contains(PlayerList.getArray().indexOf(e.getAuthor()), GameData.getDominantRank(), s))) {
					sendMessage(e, ":x: Can you prove you have that card?");
					return;
				}
			}
		}
		sendMessage(e, GameData.setDominantSuit(s, i));
	}

	@Override
	public List<String> getAliases() {
		return Arrays.asList("SJ.call");
	}

	@Override
	public String getDescription() {
		return "Call the proper suit, if you have a card of the dominant rank. Or jokers if you want no trump suit.";
	}

	@Override
	public String getName() {
		return "Call a trump (call)";
	}

	@Override
	public List<String> getUsageInstructions() {
		return Arrays.asList("SJ.call **<suit>** **[strong]** - call the appropriate suit as the trump suit.\n - **<suit>** can be one of the following:\n --- N [no trumps]\n --- C [clubs]\\n --- D [diamonds]\\n --- H [hearts]\\n --- S [spades]\n - If the strong field is filled with anything, then the call will be taken as a strong call.");
	}

}
