package commands;

import java.util.Arrays;
import java.util.List;
import java.util.Random;

import cards.Card;
import cards.CardList;
import cards.HandManager;
import game.GameData;
import game.PlayerList;
import net.dv8tion.jda.core.events.message.MessageReceivedEvent;

public class DealCommand extends Command {

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
			sendMessage(e, ":x: What are you doing? Stop it! I...I-I...I-I-I-I-I-I-I--");  //GLaDOS
			return;
		}
		if (!PlayerList.getArray().contains(e.getAuthor())) {
			sendMessage(e, ":x: Who *are* you? I don't blame you..."); //turrets
			return;
		}
		GameData.startDeal();
		sendMessage(e, ":o: Dealing. The dominant rank is :" + Card.numbers[GameData.getDominantRank()] +":.");
		try {
			HandManager.deal();
		} catch (InterruptedException e1) {
			e1.printStackTrace();
		}
		if (GameData.getDominantSuit()==-1) {
			sendMessage(e, "You have `30` seconds to weak call.");
			try {
				Thread.sleep(30000);
			} catch (InterruptedException e1) {
				e1.printStackTrace();
			}
		}
		if (GameData.getDominantSuit()!=-1&&!GameData.getStrong()) {
			sendMessage(e, "You have `30` seconds to strong call.");
			try {
				Thread.sleep(30000);
			} catch (InterruptedException e1) {
				e1.printStackTrace();
			}
		}
		if (GameData.getDominantSuit()!=-1&&GameData.getDominantSuit()!=0) {
			sendMessage(e, "You have `30` seconds to override with jokers.");
			try {
				Thread.sleep(30000);
			} catch (InterruptedException e1) {
				e1.printStackTrace();
			}
		}
		if (GameData.getDominantSuit()==-1) {
			//drastic measures
			Random random = new Random();
			Card c = CardList.cardList.get(random.nextInt(CardList.cardList.size()));
			if (c.getRank()!=GameData.getDominantRank()) {
				sendMessage(e, "Auto-call has pulled up an incompatible card. A redeal will be required.");
				GameData.redeal();
				return;
			}
			GameData.setDominantSuit(c.getSuit(), false);
		}
	}

	@Override
	public List<String> getAliases() {
		// TODO Auto-generated method stub
		return Arrays.asList("SJ.deal");
	}

	@Override
	public String getDescription() {
		// TODO Auto-generated method stub
		return "Starts the process of dealing cards for each round. Can only be used if you *aren't* currently dealing or playing anything in a game that has started.";
	}

	@Override
	public String getName() {
		// TODO Auto-generated method stub
		return "Deal (deal)";
	}

	@Override
	public List<String> getUsageInstructions() {
		// TODO Auto-generated method stub
		return Arrays.asList("SJ.deal - Start dealing for the current round.");
	}

}
