package commands;

import java.util.Arrays;
import java.util.List;

import game.GameData;
import game.PlayerList;

import net.dv8tion.jda.core.events.message.MessageReceivedEvent;

public class JoinCommand extends Command {
	@Override
	public void onCommand(MessageReceivedEvent e, String[] args) {
		if (GameData.hasGameStarted()) {
			sendMessage(e, ":x: Cannot join a game that has already started.");
			return;
		}
		if (Arrays.asList(PlayerList.getArray()).contains(e.getAuthor())) {
			sendMessage(e, ":x: You're already on the list.");
			return;
		}
		if (Arrays.asList(PlayerList.getArray()).contains(null)) {
			PlayerList.addPlayer(e.getAuthor());
			sendMessage(e, ":o: Done");
			return;
		}
		sendMessage(e, ":x: Four people at a time.");
	}

	@Override
	public List<String> getAliases() {
		return Arrays.asList("SJ.join");
	}

	@Override
	public String getDescription() {
		return "Join a game that hasn't started. ";
	}

	@Override
	public String getName() {
		return "Join (join)";
	}

	@Override
	public List<String> getUsageInstructions() {
		return Arrays.asList("SJ.join - Join a game.");
	}

}
