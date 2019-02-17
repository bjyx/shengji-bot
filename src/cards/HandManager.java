package cards;

import java.util.List;
import java.util.Random;

import game.GameData;

public class HandManager {
	private static List<List<Card> > hands;
	private static List<Card> kitty;
	
	public static void deal() {
		Random random = new Random();
		CardList.initialize();
		for (int z=0; z<25; z++) {
			for (int i=0; i<4; i++) {
				hands.get((GameData.getDealer()+i)%4).add(CardList.getCardList().remove(random.nextInt(CardList.getCardList().size())));
				//TODO find a sleep command
			}
		}
		hands.get(GameData.getDealer()).addAll(CardList.getCardList());
	}
	public static void initKitty(List<Card> cards) {
		kitty.addAll(cards);
	}
	public static void play() {
		
	}
	public static int kittyPoints() {
		int x=0;
		for (Card c : kitty) {
			if (c.getRank()==5) x += 10;
			if (c.getRank()==10||c.getRank()==13) x += 20;
		}
		return x;
	}
}