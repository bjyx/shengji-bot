package commands;

import java.util.Arrays;
import java.util.List;
import game.PlayerList;

import net.dv8tion.jda.core.events.message.MessageReceivedEvent;

public class LeaveCommand extends Command {

	@Override
	public void onCommand(MessageReceivedEvent e, String[] args) {
		//TODO: if game started return;
		//TODO: if game over return;
		if (!Arrays.asList(PlayerList.getArray()).contains(e.getAuthor())) {
			sendMessage(e, ":x: You're not on the list.");
			return;
		}
		PlayerList.removePlayer(e.getAuthor());
		sendMessage(e, ":o: Done");
	}

	@Override
	public List<String> getAliases() {
		return Arrays.asList("SJ.leave");
	}

	@Override
	public String getDescription() {
		return "Leave a game that hasn't started. ";
	}

	@Override
	public String getName() {
		return "Leave (leave)";
	}

	@Override
	public List<String> getUsageInstructions() {
		return Arrays.asList("SJ.leave - Leave a game.");
	}

}
