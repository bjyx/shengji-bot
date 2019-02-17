package cards;

import java.util.List;

public class CardList {
	public static List<Card> cardList;
	
	public static void initialize() {
		for (int r=2; r<=14; r++) {
			for (int s=1; s<=4; s++) {
				cardList.add(new Card(r,s));
				cardList.add(new Card(r,s));
			}
		}
		cardList.add(new Card(15,0)); //j-
		cardList.add(new Card(15,0));
		cardList.add(new Card(16,0)); //j+
		cardList.add(new Card(16,0));
	} 
	public static List<Card> getCardList() {
		return cardList;
	}
}
