package commands;

import java.util.Arrays;
import java.util.List;

import game.GameData;
import game.PlayerList;

import net.dv8tion.jda.core.events.message.MessageReceivedEvent;

public class StartCommand extends Command {
	@Override
	public void onCommand(MessageReceivedEvent e, String[] args) {
		if (GameData.hasGameEnded()) {
			sendMessage(e, ":x: Have you tried turning it off and on again?");
			return;
		}
		if (GameData.hasGameStarted()) {
			sendMessage(e, ":flower_playing_cards: There's a time and place for everything, but not now."); //oak
			return;
		}
		if (!PlayerList.getArray().contains(e.getAuthor())) {
			sendMessage(e, ":x: Who *are* you? I don't blame you..."); //turrets
			return;
		}
		if (PlayerList.getArray().contains(null)) {
			sendMessage(e, ":x: You're going to need a game with less people. Might I recommend Twilight Struggle?"); //shameless self-plug lmao
			return;
		}
		sendMessage(e, ":flower_playing_cards: Kāi shǐ!");
		GameData.startGame();
		//initialize other stuff here?...
	}

	@Override
	public List<String> getAliases() {
		return Arrays.asList("SJ.start");
	}

	@Override
	public String getDescription() {
		return "Let it begin.";
	}

	@Override
	public String getName() {
		return "Start (start)";
	}

	@Override
	public List<String> getUsageInstructions() {
		return Arrays.asList("SJ.start - How it all begins");
	}

}
