"""
test_game_logic.py
------------------
Tests for every rule and every move in game_logic.py.

Run from the project folder:
    python -m Tests.test_game_logic

Each test builds a SMALL, hand-made game so we know exactly
what the right answer should be.
"""

import random

from Models.card import Card, SUITS
from Data_Structure.stack import Stack
from Game.game_logic import GameLogic


# ---------- Helpers ----------

def emptyGame():
    """A GameLogic whose piles are all empty, ready for a hand-made setup."""
    logic = GameLogic()
    logic.state.createEmptyPiles()
    logic.history = Stack()
    logic.state.moveCount = 0
    return logic


def putInColumn(logic, column, card):
    logic.state.tableau[column].append(card)
    logic.setLocation(card, "tableau", column)


def putInStock(logic, card):
    logic.state.stock.enqueue(card)
    logic.setLocation(card, "stock", None)


def ids(cards):
    """Turn a list of cards into a list of strings, e.g. ['K♠', '[Q♥]']."""
    result = []
    for card in cards:
        result.append(str(card))
    return result


def snapshot(logic):
    """Text picture of the whole game, used to compare before/after."""
    state = logic.state
    picture = {}
    picture["stock"] = ids(state.stock.toList())
    picture["waste"] = ids(state.waste.toList())
    for column in state.tableau:
        picture["tableau" + str(column)] = ids(state.tableau[column].toList())
    for suit in state.foundations:
        picture[suit] = ids(state.foundations[suit].toList())
    return picture


# ---------- Tests ----------

def testTableauRules():
    logic = emptyGame()
    putInColumn(logic, 1, Card("Spades", 7, faceUp=True))      # 7♠
    putInColumn(logic, 2, Card("Hearts", 9))                   # face-down 9♥

    assert logic.canPlaceOnTableau(Card("Hearts", 6), 1)         # 6♥ on 7♠: OK
    assert not logic.canPlaceOnTableau(Card("Clubs", 6), 1)      # same colour
    assert not logic.canPlaceOnTableau(Card("Hearts", 5), 1)     # wrong rank
    assert not logic.canPlaceOnTableau(Card("Hearts", 8), 1)     # higher rank
    assert not logic.canPlaceOnTableau(Card("Spades", 8), 2)     # top is face-down
    assert logic.canPlaceOnTableau(Card("Diamonds", 13), 3)      # King on empty
    assert not logic.canPlaceOnTableau(Card("Diamonds", 12), 3)  # Queen on empty
    print("  tableau rules ............ OK")


def testFoundationRules():
    logic = emptyGame()
    assert logic.canPlaceOnFoundation(Card("Hearts", 1))         # Ace on empty
    assert not logic.canPlaceOnFoundation(Card("Hearts", 2))     # 2 on empty

    logic.state.foundations["Hearts"].push(Card("Hearts", 1, faceUp=True))
    assert logic.canPlaceOnFoundation(Card("Hearts", 2))         # 2♥ on A♥
    assert not logic.canPlaceOnFoundation(Card("Hearts", 3))     # skips a rank
    assert logic.canPlaceOnFoundation(Card("Diamonds", 1))       # other suit: own pile
    print("  foundation rules ......... OK")


def testMoveGroupAndFlip():
    logic = emptyGame()
    putInColumn(logic, 1, Card("Spades", 13))                  # face-down K♠
    putInColumn(logic, 1, Card("Clubs", 7, faceUp=True))       # 7♣
    putInColumn(logic, 1, Card("Hearts", 6, faceUp=True))      # 6♥
    putInColumn(logic, 2, Card("Diamonds", 8, faceUp=True))    # 8♦
    before = snapshot(logic)

    # Move 7♣ (index 1) and 6♥ on top of it onto 8♦
    assert logic.moveTableauToTableau(1, 1, 2)
    assert ids(logic.state.tableau[2].toList()) == ["8♦", "7♣", "6♥"]
    assert ids(logic.state.tableau[1].toList()) == ["K♠"]       # flipped face-up!
    assert logic.state.cardLocations["6♥"] == ("tableau", 2)
    assert logic.state.moveCount == 1

    assert logic.undo()
    assert snapshot(logic) == before                             # K♠ face-down again
    assert logic.state.cardLocations["6♥"] == ("tableau", 1)
    assert logic.state.moveCount == 0
    print("  group move + flip + undo . OK")


def testInvalidMoveChangesNothing():
    logic = emptyGame()
    putInColumn(logic, 1, Card("Spades", 7, faceUp=True))
    putInColumn(logic, 2, Card("Clubs", 6, faceUp=True))
    before = snapshot(logic)

    assert not logic.moveTableauToTableau(2, 0, 1)   # 6♣ on 7♠: same colour
    assert not logic.moveTableauToTableau(1, 0, 1)   # same column
    assert not logic.moveTableauToFoundation(1)      # 7 cannot start a foundation
    assert not logic.moveWasteToTableau(1)           # waste is empty
    assert snapshot(logic) == before
    assert logic.history.isEmpty()
    assert logic.state.moveCount == 0
    print("  invalid moves ignored .... OK")


def testDrawRecycleAndUndo():
    logic = emptyGame()
    for rank in [5, 6, 7]:
        putInStock(logic, Card("Clubs", rank))
    before = snapshot(logic)

    logic.drawFromStock()
    logic.drawFromStock()
    logic.drawFromStock()
    assert logic.state.stock.isEmpty()
    assert ids(logic.state.waste.toList()) == ["5♣", "6♣", "7♣"]   # 7♣ on top

    logic.drawFromStock()                          # stock empty -> recycle
    assert logic.state.waste.isEmpty()
    assert ids(logic.state.stock.toList()) == ["[5♣]", "[6♣]", "[7♣]"]

    for i in range(4):                             # undo recycle + 3 draws
        assert logic.undo()
    assert snapshot(logic) == before
    assert not logic.undo()                        # nothing left to undo
    print("  draw / recycle / undo .... OK")


def testDrawThree():
    logic = emptyGame()
    logic.drawCount = 3
    for rank in [1, 2, 3, 4]:
        putInStock(logic, Card("Spades", rank))
    before = snapshot(logic)

    logic.drawFromStock()
    assert ids(logic.state.waste.toList()) == ["A♠", "2♠", "3♠"]
    logic.drawFromStock()                          # only 1 card left
    assert ids(logic.state.waste.toList()) == ["A♠", "2♠", "3♠", "4♠"]

    logic.undo()
    logic.undo()
    assert snapshot(logic) == before
    print("  draw three ............... OK")


def testWin():
    logic = emptyGame()
    for suit in SUITS:                             # stock: A..K of each suit in order
        for rank in range(1, 14):
            putInStock(logic, Card(suit, rank))

    assert not logic.isWon()
    for i in range(52):
        logic.drawFromStock()
        assert logic.moveWasteToFoundation()
    assert logic.isWon()
    print("  win detection ............ OK")


# ---------- Random play test ----------

def checkGameIsConsistent(logic):
    """Rules that must ALWAYS be true, no matter what moves were made."""
    state = logic.state
    assert state.countAllCards() == 52
    assert len(state.cardLocations) == 52

    for card in state.stock.toList():
        assert not card.faceUp
        assert state.getLocation(card) == ("stock", None)
    for card in state.waste.toList():
        assert card.faceUp
        assert state.getLocation(card) == ("waste", None)

    for suit in state.foundations:
        cards = state.foundations[suit].toList()
        for position in range(len(cards)):
            assert cards[position].suit == suit
            assert cards[position].rank == position + 1     # A, 2, 3, ... in order
            assert state.getLocation(cards[position]) == ("foundation", suit)

    for column in state.tableau:
        cards = state.tableau[column].toList()
        seenFaceUp = False
        for card in cards:
            assert state.getLocation(card) == ("tableau", column)
            if card.faceUp:
                seenFaceUp = True
            else:
                assert not seenFaceUp       # no face-down card above a face-up one
        if len(cards) > 0:
            assert cards[-1].faceUp         # the top card is always visible


def tryRandomMove(logic):
    """Try one random move (it may be illegal - that is part of the test)."""
    choice = random.randint(1, 6)
    column = random.randint(1, 7)
    if choice == 1:
        return logic.drawFromStock()
    if choice == 2:
        return logic.moveWasteToTableau(column)
    if choice == 3:
        return logic.moveWasteToFoundation()
    if choice == 4:
        return logic.moveTableauToFoundation(column)
    if choice == 5:
        size = logic.state.tableau[column].size()
        index = random.randint(0, max(size - 1, 0))
        return logic.moveTableauToTableau(column, index, random.randint(1, 7))
    suit = random.choice(SUITS)
    return logic.moveFoundationToTableau(suit, column)


def testRandomGames():
    """Play 200 random games, checking the rules after every attempt,
    then undo every move and check we are back at the start."""
    for game in range(200):
        logic = GameLogic(drawCount=random.choice([1, 3]))
        start = snapshot(logic)

        for attempt in range(400):
            before = snapshot(logic)
            historyBefore = logic.history.size()
            moved = tryRandomMove(logic)
            if not moved:
                assert snapshot(logic) == before          # illegal move: nothing changed
                assert logic.history.size() == historyBefore
            checkGameIsConsistent(logic)

        while logic.undo():
            checkGameIsConsistent(logic)
        assert snapshot(logic) == start
        assert logic.state.moveCount == 0
    print("  200 random games ......... OK")


if __name__ == "__main__":
    print("Running game logic tests:")
    testTableauRules()
    testFoundationRules()
    testMoveGroupAndFlip()
    testInvalidMoveChangesNothing()
    testDrawRecycleAndUndo()
    testDrawThree()
    testWin()
    testRandomGames()
    print("All game logic tests passed!")