package game;

import cards.Card;

public class GameData {
	private static boolean started = false;
	private static boolean dealing = false;
	private static boolean strong = false;
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
	
	public static void startDeal() {
		dealing = true;
	}
	
	public static boolean isDealing() {
		return dealing;
	}
	
	public static void endGame() {
		ended = true;
	}
	
	public static boolean hasGameEnded() {
		return ended;
	}
	
	public static boolean getStrong() {
		return strong;
	}
	
	public static void reset() {
		started = false;
		ended = false;
		score[0] = 2;
		score[1] = 2;
		dominantSuit = -1;
		dealer = -1;
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
		dealing = false;
		strong = false;
		dominantSuit = -1;
		setDealer(newDealer);
	}
	public static String setDominantSuit(int newSuit, boolean str) {
		if (strong && newSuit != 0) return ":x: Lol no.";
		if (!strong && dominantSuit != -1 && !str) return ":x: Lol no.";
		dominantSuit = newSuit; 
		strong = str;
		return ":o " + (strong?"Strong ":"Weak ") + "declaration for :" + Card.suits[dominantSuit] + ":!";
	}
	public static int getDominantSuit() {
		return dominantSuit;
	}
	public static int getDominantRank() {
		return score[dealer%2];
	}

	public static void redeal() {
		dealing = false;
		strong = false;
		dominantSuit = -1;
	}
}
