package cards;

import java.util.Comparator;

import game.GameData;
import game.Round;

public class Card {
	private final int rank; //2-13, 14 = A, 15 = J
	private final int suit; //1C 2D 3H 4S
	private static final String[] numbers = {"zero","one","two","three","four","five","six","seven","eight","nine","keycap_ten","regional_indicator_j","regional_indicator_q","regional_indicator_k","regional_indicator_a","small_red_triangle_down","small_red_triangle"};
	private static final String[] suits = {"joker","clubs","diamonds","hearts","spades"};
	
	public Card() {
		rank = 0;
		suit = 0;
	}
	public Card(int r, int s) {
		rank = r;
		suit = s;
	}
	
	static class comparator implements Comparator<Card> {
		@Override
		public int compare(Card o1, Card o2) {
			if (o1.getHierarchy()==o2.getHierarchy()) {
				if (o1.suit==o2.suit) {
					if (o1.rank==o2.rank) return 0;
					else if (o1.rank<o2.rank) return -1;
					else return 1;
				}
				else if (o1.suit < o2.suit) return -1;
				else return 1;
			}
			return (o1.getHierarchy()-o2.getHierarchy())/Math.abs(o1.getHierarchy()-o2.getHierarchy());
		}
		
	}
	
	public int getHierarchy() {
		if (rank >= 15) return rank + 15;
		if (rank == GameData.getDominantRank()) return 29;
		if (suit == GameData.getDominantSuit()) return 14+rank-(rank>GameData.getDominantRank()?1:0); //17-28
		if (suit == Round.getRoundSuit()) return rank-(rank>GameData.getDominantRank()?1:0); //2-13
		return 0;
	}
	public int getRank() {
		return rank;
	}
	public String getSuit() {
		return suits[suit];
	}
	public String getSuitShort() {
		if (getSuit()==null) return "N";
		return getSuit().substring(0,1).toUpperCase();
	}
	public String toString() {
		return ":" + numbers[rank] + "::" + suits[suit] + ":";
	}
	
}
