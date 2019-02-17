package game;

import java.util.List;

import cards.Card;

public class Round {
	private static int RoundSuit;
	private List<List<Card> > plays;
	
	public void uploadPlay(List<Card> cards) {
		plays.add(cards);
	}
	
	public static int getRoundSuit() {
		// TODO Auto-generated method stub
		return RoundSuit;
	}
	
}
