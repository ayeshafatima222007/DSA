"""
deck.py
-------
The Deck holds the 52 cards BEFORE they are dealt.

It uses a normal Python list (an array), because:
    - we need to build 52 cards in order,
    - random.shuffle() needs a list to mix the cards,
    - list.pop() removes the last card in O(1) time.
"""

import random

from Models.card import Card, SUITS


class Deck:
    """A list of 52 Card objects that can be shuffled and dealt."""

    def __init__(self):
        self.cards = []         # Python list that stores the Card objects
        self.createCards()

    def createCards(self):
        """
        Fill the list with 52 cards: 4 suits x 13 ranks.
        All cards start face-down.
        """
        self.cards = []
        for suit in SUITS:              # "Hearts", "Diamonds", "Clubs", "Spades"
            for rank in range(1, 14):   # 1 (Ace) up to 13 (King)
                self.cards.append(Card(suit, rank))

    def shuffle(self):
        """Put the cards in a random order (in place).  O(n)"""
        random.shuffle(self.cards)

    def dealCard(self):
        """
        Remove and return the LAST card of the list.  O(1)
        Returns None if the deck is empty.
        """
        if self.isEmpty():
            return None
        return self.cards.pop()

    def size(self):
        """Return how many cards are left in the deck."""
        return len(self.cards)

    def isEmpty(self):
        """Return True if there are no cards left."""
        return len(self.cards) == 0


# ---------- Quick self-test ----------
if __name__ == "__main__":
    deck = Deck()
    print("Cards created:", deck.size())
    print("First 5 before shuffle:", deck.cards[:5])
    assert deck.size() == 52

    # Every card must be different: use the ids as dictionary keys
    seen = {}
    for card in deck.cards:
        seen[card.cardId()] = True
    assert len(seen) == 52

    deck.shuffle()
    print("First 5 after shuffle: ", deck.cards[:5])
    assert deck.size() == 52    # shuffling must not lose or add cards

    card = deck.dealCard()
    print("Dealt:", card, "| left:", deck.size())
    assert deck.size() == 51

    while not deck.isEmpty():
        deck.dealCard()
    assert deck.dealCard() is None

    print("All Deck tests passed!")