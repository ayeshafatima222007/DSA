"""
test_setup.py
-------------
Tests for the data structures, the deck and the starting deal.

Run from the project folder:
    python -m Tests.test_setup
"""

from Models.card import Card, SUITS
from Data_Structure.linked_list import LinkedList
from Data_Structure.stack import Stack
from Data_Structure.queue import Queue
from Game.deck import Deck
from Game.game_state import GameState
from Game.game_logic import GameLogic


# ---------- Data structures ----------

def testStackIsLifo():
    stack = Stack()
    for rank in [1, 2, 3]:
        stack.push(Card("Hearts", rank))
    assert stack.size() == 3
    assert stack.peek().rank == 3
    assert stack.pop().rank == 3        # last in, first out
    assert stack.pop().rank == 2
    assert stack.pop().rank == 1
    assert stack.isEmpty()
    assert stack.pop() is None
    print("  stack is LIFO ............ OK")


def testQueueIsFifo():
    queue = Queue()
    for rank in [1, 2, 3]:
        queue.enqueue(Card("Clubs", rank))
    assert queue.size() == 3
    assert queue.front().rank == 1
    assert queue.dequeue().rank == 1    # first in, first out
    assert queue.dequeue().rank == 2
    assert queue.dequeue().rank == 3
    assert queue.isEmpty()
    assert queue.dequeue() is None
    queue.enqueue(Card("Clubs", 9))     # must still work after being emptied
    assert queue.front().rank == 9
    print("  queue is FIFO ............ OK")


def testLinkedListSplitAndExtend():
    pile = LinkedList()
    for rank in [13, 12, 11, 10]:
        pile.append(Card("Spades", rank))
    group = pile.splitFrom(2)           # take J and 10
    assert pile.size() == 2 and group.size() == 2
    assert pile.peek().rank == 12 and group.peek().rank == 10

    other = LinkedList()
    other.extend(group)
    assert other.size() == 2 and group.isEmpty()
    assert other.get(0).rank == 11
    print("  linked list split/extend . OK")


# ---------- Deck (Python list) ----------

def testDeckHas52DifferentCards():
    deck = Deck()
    assert deck.size() == 52
    names = {}                           # dictionary used as a "seen" set
    for card in deck.cards:
        names[card.cardId()] = True
        assert card.faceUp is False
    assert len(names) == 52              # no duplicates
    deck.shuffle()
    assert deck.size() == 52
    print("  deck: 52 different cards . OK")


# ---------- Starting deal ----------

def checkStartingDeal(state):
    # 52 cards in total, all tracked in the dictionary
    assert state.countAllCards() == 52
    assert len(state.cardLocations) == 52

    # Seven columns with 1..7 cards, only the top card face-up
    assert len(state.tableau) == 7
    for column in range(1, 8):
        cards = state.tableau[column].toList()
        assert len(cards) == column
        for i in range(len(cards)):
            assert cards[i].faceUp == (i == len(cards) - 1)

    # 24 face-down cards in the stock, empty waste and foundations
    assert state.stock.size() == 24
    for card in state.stock.toList():
        assert card.faceUp is False
    assert state.waste.isEmpty()
    assert len(state.foundations) == 4
    for suit in SUITS:
        assert state.foundations[suit].isEmpty()


def testStartingDeal():
    state = GameState()
    for i in range(100):                 # 100 different shuffles
        state.newGame()
        checkStartingDeal(state)
    print("  52 cards dealt correctly . OK")


def testNewGameResetsEverything():
    logic = GameLogic()
    logic.drawFromStock()
    logic.drawFromStock()
    assert logic.state.moveCount == 2

    logic.newGame()
    checkStartingDeal(logic.state)
    assert logic.state.moveCount == 0
    assert logic.history.isEmpty()       # old moves cannot be undone
    print("  new game resets .......... OK")


if __name__ == "__main__":
    print("Running setup tests:")
    testStackIsLifo()
    testQueueIsFifo()
    testLinkedListSplitAndExtend()
    testDeckHas52DifferentCards()
    testStartingDeal()
    testNewGameResetsEverything()
    print("All setup tests passed!")