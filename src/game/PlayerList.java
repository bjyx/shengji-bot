package game;

import java.util.Arrays;
import java.util.List;

import net.dv8tion.jda.core.EmbedBuilder;
import net.dv8tion.jda.core.entities.MessageEmbed;
import net.dv8tion.jda.core.entities.User;

public class PlayerList {
	private static User[] players = {null, null, null, null};
	
	public static void addPlayer(User u, int a) {
		if (players[a]==null) {
			players[a]=u;
			return;
		}
		if (players[(2+a)%4]==null) {
			players[(2+a)%4]=u;
			return;
		}
	}
	public static void removePlayer(User u) {
		if (players[0]==u) {
			players[0]=null;
			return;
		}
		if (players[1]==u) {
			players[1]=null;
			return;
		}
		if (players[2]==u) {
			players[2]=null;
			return;
		}
		if (players[3]==u) {
			players[3]=null;
			return;
		}
	}
	public static MessageEmbed getPlayers() {
		EmbedBuilder builder = new EmbedBuilder().setTitle("Players").setColor(8519882).addField("North-South", players[0]+"\n"+players[2], false).addField("East-West", players[1]+"\n"+players[3], false);
		
		return builder.build();
	}
	public static List<User> getArray() {
		return Arrays.asList(players);
	}
	public static User getPlayerDealer(int wind) {
		return players[(GameData.getDealer()+wind)%4];
	}
	public static User getPlayer(int wind) {
		return players[wind];
	}
}
