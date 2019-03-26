package cards;

import java.util.Collections;
import java.util.List;
import java.util.Random;

import cards.Card;
import game.GameData;
import game.PlayerList;
import net.dv8tion.jda.core.EmbedBuilder;
import net.dv8tion.jda.core.entities.MessageEmbed;

public class HandManager {
	public static List< List<Card> > hands;
	private static List<Card> kitty;
	
	public static void deal() throws InterruptedException {
		Random random = new Random();
		CardList.initialize();
		for (int z=0; z<25; z++) {
			for (int i=0; i<4; i++) {
				hands.get((GameData.getDealer()+i)%4).add(CardList.cardList.remove(random.nextInt(CardList.cardList.size())));
				PlayerList.getPlayer(i).openPrivateChannel().complete().sendMessage(sendHands(i)).complete();
				Thread.sleep(1000);
			}
		}
	}
	public static void dealKitty() {
		hands.get(GameData.getDealer()).addAll(CardList.cardList);
	}
	public static void initKitty(List<Card> cards) {
		kitty.addAll(cards);
	}
	public static boolean contains(int wind, int r, int s) {
		return (HandManager.hands.get(wind).contains(CardList.getCard(r,s))||HandManager.hands.get(wind).contains(CardList.getCard2(r,s)));
	}
	public static boolean containspair(int wind, int r, int s) {
		return (HandManager.hands.get(wind).contains(CardList.getCard(r,s))&&HandManager.hands.get(wind).contains(CardList.getCard2(r,s)));
	}
	public static void play(List<Card> cards) {
		
	}
	public static int kittyPoints() {
		int x=0;
		for (Card c : kitty) {
			if (c.getRank()==5) x += 10;
			if (c.getRank()==10||c.getRank()==13) x += 20;
		}
		return x;
	}
	public static MessageEmbed sendHands(int i) {
		Collections.sort(hands.get(i));
		EmbedBuilder builder = new EmbedBuilder().setTitle("Your Hand");
		StringBuilder newString = new StringBuilder();
		for (Card c : hands.get(i)) {
			newString.append(c.toString()).append("\n");
		}
		builder.addField("",newString.toString(),false);
		return builder.build();
	}
	
}