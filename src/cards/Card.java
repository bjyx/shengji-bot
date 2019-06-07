package cards;


import game.GameData;
import game.Round;

public class Card implements Comparable<Card> {
	private final int rank; //2-13, 14 = A, 15 = J-, 16 = J+
	private final int suit; //1C 2D 3H 4S
	public static final String[] numbers = {"zero","one","two","three","four","five","six","seven","eight","nine","keycap_ten","regional_indicator_j","regional_indicator_q","regional_indicator_k","regional_indicator_a","small_red_triangle_down","small_red_triangle"};
	public static final String[] nums = {"0","1","2","3","4","5","6","7","8","9","10","J","Q","K","A","-","+"};
	public static final String[] suits = {"joker","clubs","diamonds","hearts","spades"};
	
	public Card() {
		rank = 0;
		suit = 0;
	}
	public Card(int r, int s) {
		rank = r;
		suit = s;
	}
	
	public int getHierarchy() {
		if (rank >= 15) return rank + 15;
		if (rank == GameData.getDominantRank()&&suit==GameData.getDominantSuit()) return 29;
		if (rank == GameData.getDominantRank()) return 28;
		if (suit == GameData.getDominantSuit()) return 14+rank-(rank>GameData.getDominantRank()?1:0); //16-27
		if (suit == Round.getRoundSuit()) return rank-(rank>GameData.getDominantRank()?1:0); //2-13
		return 0;
	}
	
	public int getRank() {
		return rank;
	}
	public int getSuit() {
		return suit;
	}
	
	public String getRankString() {
		return numbers[rank];
	}
	public String getSuitString() {
		return suits[suit];
	}
	public String getSuitShort() {
		if (getSuitString()==null) return "N";
		return getSuitString().substring(0,1).toUpperCase();
	}
	public String toString() {
		return "`" + nums[rank] + (suits[suit].substring(0,1).toUpperCase()) + "`";
	}
	public String toEmoji() {
		return ":" + numbers[rank] + "::" + suits[suit] + ":";
	}
	@Override
	public int compareTo(Card o) {
		if (getHierarchy()>o.getHierarchy()) return 1;
		else if (getHierarchy()<o.getHierarchy()) return -1;
		return 0;
	}
	public boolean equals(Card o) {
		return (rank==o.getRank() && suit==o.getSuit());
	}
}
