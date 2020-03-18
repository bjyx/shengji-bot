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
		if (PlayerList.getArray().contains(e.getAuthor())) {
			sendMessage(e, ":x: You're already on the list.");
			return;
		}
		if (args.length<2) {
			sendMessage(e, ":x: Which side do you want to be on?");
			return;
		}
		if (Arrays.asList(PlayerList.getArray()).contains(null)) {
			PlayerList.addPlayer(e.getAuthor(), parseArg(args[1]));
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
		return Arrays.asList("SJ.join <alignment> - Join a game.\n"
				+ "- Alignment can be any of the following:\n"
				+ "\\* `north, n, bei, b`\n"
				+ "\\* `south, s, nan`\n"
				+ "\\* `west, w, xi, x`\n"
				+ "\\* `east, e, dong, d`\n");
	}
	private int parseArg(String a) {
		if (a.toLowerCase().charAt(0)=='n'&&a.equals("nan")) return 2;
		if (a.toLowerCase().charAt(0)=='n') return 0;
		if (a.toLowerCase().charAt(0)=='b') return 0;
		if (a.toLowerCase().charAt(0)=='s') return 2;
		if (a.toLowerCase().charAt(0)=='e') return 1;
		if (a.toLowerCase().charAt(0)=='d') return 1;
		if (a.toLowerCase().charAt(0)=='w') return 3;
		if (a.toLowerCase().charAt(0)=='x') return 3;
		return -1;
	}
}
