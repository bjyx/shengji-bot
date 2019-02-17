package game;

public class GameData {
	private static boolean started = false;
	private static boolean ended = false;
	private static int[] score = {2, 2};
	private static int dominantSuit = -1;
	private static int dealer = -1;
	
	public static void startGame() {
		started = true;
	}
	
	public static boolean hasGameStarted() {
		return started;
	}
	
	public static void endGame() {
		ended = true;
	}
	
	public static boolean hasGameEnded() {
		return ended;
	}
	
	public static void reset() {
		started = false;
		ended = false;
		score[0] = 2;
		score[1] = 2;
		dominantSuit = -1;
	}
	public static void changescore(int team, int delta) {
		score[team] += delta;
	}
	
	public static int getscore(int team) {
		return score[team];
	}
	
	public static void setDealer(int wind) {
		dealer = wind;
	}
	public static int getDealer() {
		return dealer;
	}
	public static void newRound(int newDealer) {
		dominantSuit = -1;
		setDealer(newDealer);
	}
	public static void setDominantSuit(int newSuit) {
		dominantSuit = newSuit;
	}
	public static int getDominantSuit() {
		return dominantSuit;
	}
	public static int getDominantRank() {
		return score[dealer%2];
	}
}
