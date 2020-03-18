package commands;

import java.util.Arrays;
import java.util.List;

import game.GameData;
import game.PlayerList;
import net.dv8tion.jda.core.events.message.MessageReceivedEvent;

public class PlayCommand extends Command {

	@Override
	public void onCommand(MessageReceivedEvent e, String[] args) {
		// TODO Auto-generated method stub
		if (GameData.hasGameEnded()) {
			sendMessage(e, ":x: Have you tried turning it off and on again?");
			return;
		}
		if (!GameData.hasGameStarted()) {
			sendMessage(e, ":x: `404 GAME NOT FOUND`"); 
			return;
		}
		if (!GameData.isDealing()) {
			sendMessage(e, ":x: WhaT ArE YOu DOING? sToP iT! I...i-I...I-I-i-I-I-I-i--");  //GLaDOS
			return;
		}
		if (!PlayerList.getArray().contains(e.getAuthor())) {
			sendMessage(e, ":x: Who *are* you? I don't blame you..."); //turrets
			return;
		}
		if (args.length<2) {
			sendMessage(e, ":x: Playing **what**, pray tell?");
			return;
		}
		for (int i=1; i<args.length; i++) {
			
		}
	}

	@Override
	public List<String> getAliases() {
		// TODO Auto-generated method stub
		return Arrays.asList("SJ.play");
	}

	@Override
	public String getDescription() {
		// TODO Auto-generated method stub
		return "Play the set of cards specified in the argument, as long as they're in your hand.";
	}

	@Override
	public String getName() {
		// TODO Auto-generated method stub
		return "Play a card";
	}

	@Override
	public List<String> getUsageInstructions() {
		// TODO Auto-generated method stub
		return Arrays.asList("SJ.play *<cards>* - plays the cards specified, as long as that move is legal");
	}

}
