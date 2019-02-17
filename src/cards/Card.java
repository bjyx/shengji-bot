package cards;

import game.GameData;
import game.Round;

public class Card {
	private final int rank; //2-13, 14 = A, 15 = J
	private final int suit; //1C 2D 3H 4S
	
	public Card() {
		rank = 0;
		suit = 0;
	}
	public Card(int r, int s) {
		rank = r;
		suit = s;
	}
	public int getHierarchy(Round round) {
		if (rank == 16) return 31;
		if (rank == 15) return 30;
		if (rank == GameData.getDominantRank()) return 29;
		if (suit == GameData.getDominantSuit()) return 14+rank-(rank>GameData.getDominantRank()?1:0); //17-28
		if (suit == round.getRoundSuit()) return rank-(rank>GameData.getDominantRank()?1:0); //2-13
		return 0;
	}
	public int getRank() {
		return rank;
	}
	public String getSuit() {
		String[] suits = {null,"clubs","diamonds","hearts","spades"};
		return suits[suit];
	}
	public String getSuitShort() {
		if (getSuit()==null) return "N";
		return getSuit().substring(0,1).toUpperCase();
	}
	
}
