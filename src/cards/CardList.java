package cards;

import java.util.List;

public class CardList {
	public static List<Card> cardListMaster;
	public static List<Card> cardList;
	
	static {
		for (int s=1; s<=4; s++) {
			for (int r=2; r<=14; r++) {
				cardListMaster.add(new Card(r,s));
				cardListMaster.add(new Card(r,s)); // 2c2c3c3c4c4c...
			}
		}
		cardListMaster.add(new Card(15,0)); //j-
		cardListMaster.add(new Card(15,0));
		cardListMaster.add(new Card(16,0)); //j+
		cardListMaster.add(new Card(16,0));
	} 
	public static Card getCard(int r, int s) {
		return cardListMaster.get(getIndexOf(r,s));
	}
	
	public static Card getCard2(int r, int s) {
		return cardListMaster.get(getIndexOf(r,s)+1);
	}
	
	public static int getIndexOf(int r, int s) {
		if (s==0) {
			if (r==16) return 106;
			return 104;
		}
		return ((r-2)+(s-1)*13)*2;
	}
	public static void initialize() {
		cardList.addAll(cardListMaster);
	}
}
