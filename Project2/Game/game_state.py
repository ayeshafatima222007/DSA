"""
game_state.py
-------------
GameState holds ALL the piles of one Solitaire game, and sets up
a new game by dealing the cards from the Deck.

Where every data structure is used:

    Deck            -> Python LIST     (52 cards, shuffled)
    stock           -> QUEUE           (face-down draw pile, FIFO)
    waste           -> STACK           (cards drawn from the stock)
    tableau         -> DICTIONARY      {1: LinkedList, ..., 7: LinkedList}
    foundations     -> DICTIONARY      {"Hearts": Stack, ...}
    cardLocations   -> DICTIONARY      {"Q♥": ("tableau", 3), ...}

This file only STORES the game. The rules (which moves are legal)
will go in game_logic.py in Stage 4.
"""

from Models.card import SUITS
from Data_Structure.linked_list import LinkedList
from Data_Structure.stack import Stack
from Data_Structure.queue import Queue
from Game.deck import Deck


class GameState:
    """All piles and dictionaries for one game of Klondike Solitaire."""

    def __init__(self):
        self.deck = Deck()          # Python list of 52 cards
        self.stock = Queue()        # draw pile
        self.waste = Stack()        # drawn cards
        self.tableau = {}           # column number -> LinkedList
        self.foundations = {}       # suit name -> Stack
        self.cardLocations = {}     # card id -> (pile type, pile key)
        self.moveCount = 0
        self.newGame()

    # ---------- Setting up a new game ----------

    def newGame(self):
        """Throw away the old game and deal a brand new one."""
        self.createEmptyPiles()
        self.deck.createCards()     # fresh 52 cards
        self.deck.shuffle()
        self.dealTableau()
        self.fillStock()
        self.moveCount = 0

    def createEmptyPiles(self):
        """Make every pile empty and clear the location dictionary."""
        self.stock = Queue()
        self.waste = Stack()

        self.tableau = {}
        for column in range(1, 8):          # columns 1 to 7
            self.tableau[column] = LinkedList()

        self.foundations = {}
        for suit in SUITS:                  # one foundation per suit
            self.foundations[suit] = Stack()

        self.cardLocations = {}

    def dealTableau(self):
        """
        Column 1 gets 1 card, column 2 gets 2 cards, ... column 7 gets 7.
        Total = 1+2+3+4+5+6+7 = 28 cards.
        Only the top (last) card of every column is turned face-up.
        """
        for column in range(1, 8):
            for i in range(column):
                card = self.deck.dealCard()
                self.tableau[column].append(card)
                self.cardLocations[card.cardId()] = ("tableau", column)

            # Flip the top card of this column face-up.
            topCard = self.tableau[column].peek()
            topCard.flip()

    def fillStock(self):
        """Put every card still in the deck (52 - 28 = 24) into the stock."""
        while not self.deck.isEmpty():
            card = self.deck.dealCard()
            self.stock.enqueue(card)
            self.cardLocations[card.cardId()] = ("stock", None)

    # ---------- Helpers ----------

    def getLocation(self, card):
        """Return where a card is, e.g. ("tableau", 3).  O(1) dictionary lookup."""
        return self.cardLocations.get(card.cardId())

    def countAllCards(self):
        """Count cards in every pile. Must always be 52."""
        total = self.stock.size() + self.waste.size()
        for column in self.tableau:
            total += self.tableau[column].size()
        for suit in self.foundations:
            total += self.foundations[suit].size()
        return total

    def printState(self):
        """Print the whole game as text (for testing without the GUI)."""
        print("Stock:", self.stock.size(), "cards")
        print("Waste:", self.waste.toList())
        for suit in self.foundations:
            print("Foundation", suit + ":", self.foundations[suit].toList())
        for column in self.tableau:
            print("Column", column, ":", self.tableau[column])


# ---------- Quick self-test ----------
if __name__ == "__main__":
    game = GameState()
    game.printState()
    print()

    # Run the checks on 100 different shuffles, not just one.
    for test in range(100):
        game.newGame()

        # 1. All 52 cards are somewhere
        assert game.countAllCards() == 52
        assert len(game.cardLocations) == 52

        # 2. Column N has N cards, only the top one face-up
        for column in range(1, 8):
            cards = game.tableau[column].toList()
            assert len(cards) == column
            for position in range(len(cards)):
                isTop = (position == len(cards) - 1)
                assert cards[position].faceUp == isTop

        # 3. Stock has 24 face-down cards, waste and foundations empty
        assert game.stock.size() == 24
        for card in game.stock.toList():
            assert card.faceUp is False
            assert game.getLocation(card) == ("stock", None)
        assert game.waste.isEmpty()
        for suit in SUITS:
            assert game.foundations[suit].isEmpty()

        # 4. The location dictionary agrees with the tableau
        for column in range(1, 8):
            for card in game.tableau[column].toList():
                assert game.getLocation(card) == ("tableau", column)

    print("Checked 100 new games: 52 cards, 28 in tableau, 24 in stock.")
    print("All GameState tests passed!")