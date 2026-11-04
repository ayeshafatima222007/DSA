"""
card.py
-------
The Card class represents ONE playing card.

Every other part of the game (stack, queue, linked list, deck, piles)
stores and moves Card objects, so this is the foundation of the project.
"""

# ---------- Constants (shared information about all cards) ----------

# The four suits, in the order we will use them everywhere in the game.
SUITS = ["Hearts", "Diamonds", "Clubs", "Spades"]

# Suits that are red. Every other suit is black.
RED_SUITS = ["Hearts", "Diamonds"]

# Dictionary: suit name -> symbol shown on the card.
SUIT_SYMBOLS = {
    "Hearts": "♥",
    "Diamonds": "♦",
    "Clubs": "♣",
    "Spades": "♠",
}

# Dictionary: special rank numbers -> letter shown on the card.
# Ranks 2 to 10 are just shown as their number.
RANK_NAMES = {
    1: "A",
    11: "J",
    12: "Q",
    13: "K",
}


class Card:
    """One playing card with a suit, a rank and a face-up/face-down state."""

    def __init__(self, suit, rank, faceUp=False):
        # Check the input so a wrong card can never be created by mistake.
        if suit not in SUITS:
            raise ValueError("Invalid suit: " + str(suit))
        if rank < 1 or rank > 13:
            raise ValueError("Invalid rank: " + str(rank))

        self.suit = suit          # "Hearts", "Diamonds", "Clubs" or "Spades"
        self.rank = rank          # number from 1 (Ace) to 13 (King)
        self.faceUp = faceUp    # True = player can see it, False = hidden

    # ---------- Colour ----------

    def isRed(self):
        """Return True if the card is a Heart or a Diamond."""
        return self.suit in RED_SUITS

    def color(self):
        """Return the colour of the card as text: "red" or "black"."""
        if self.isRed():
            return "red"
        return "black"

    # ---------- Face up / face down ----------

    def flip(self):
        """Turn the card over (face-up becomes face-down and the other way)."""
        self.faceUp = not self.faceUp

    # ---------- Text helpers (used for printing and for the UI) ----------

    def rankName(self):
        """Return the rank as text: "A", "2" ... "10", "J", "Q", "K"."""
        if self.rank in RANK_NAMES:
            return RANK_NAMES[self.rank]
        return str(self.rank)

    def symbol(self):
        """Return the suit symbol, for example "♥"."""
        return SUIT_SYMBOLS[self.suit]

    def cardId(self):
        """
        Return a short unique name such as "Q♥" or "10♠".
        No two cards in a deck share an id, so we can use it
        as a dictionary key later (to track where each card is).
        """
        return self.rankName() + self.symbol()

    def __str__(self):
        """
        Called by print(card).
        Face-up cards print normally: Q♥
        Face-down cards print inside brackets: [Q♥]
        (We still show the name so debugging is easy.)
        """
        if self.faceUp:
            return self.cardId()
        return "[" + self.cardId() + "]"

    def __repr__(self):
        """Called when a card is printed inside a list, e.g. print([c1, c2])."""
        return self.__str__()


# ---------- Quick self-test ----------
# This block runs ONLY when you run this file directly,
# not when another file imports Card.
if __name__ == "__main__":
    ace = Card("Spades", 1)
    queen = Card("Hearts", 12, faceUp=True)

    print("Ace of spades (face-down):", ace)
    print("Queen of hearts (face-up):", queen)

    ace.flip()
    print("Ace after flip:", ace)

    print("Queen colour:", queen.color())
    print("Ace colour:", ace.color())
    print("Queen id:", queen.cardId())

    # Simple checks: if any of these is wrong, Python stops with an error.
    assert queen.isRed() is True
    assert ace.isRed() is False
    assert ace.faceUp is True
    assert queen.rankName() == "Q"
    assert Card("Clubs", 10).rankName() == "10"

    # A wrong card must be rejected.
    try:
        Card("Stars", 5)
        print("ERROR: invalid suit was accepted!")
    except ValueError:
        print("Invalid suit correctly rejected.")

    print("All Card tests passed!")