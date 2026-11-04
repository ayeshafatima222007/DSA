"""
game_logic.py
-------------
The RULES of Klondike Solitaire.

GameState (game_state.py) only stores the piles.
GameLogic (this file) decides which moves are legal and performs them.

Every move follows the same 4 steps:
    1. CHECK   - is the move legal?        (if not, return False, change nothing)
    2. MOVE    - take card(s) from one data structure, put them in another
    3. UPDATE  - update the cardLocations dictionary, flip exposed cards
    4. RECORD  - push a record of the move onto the undo Stack

Moves supported:
    drawFromStock()                    stock (Queue)   -> waste (Stack)
    moveWasteToTableau(column)         waste (Stack)   -> tableau (LinkedList)
    moveWasteToFoundation()            waste (Stack)   -> foundation (Stack)
    moveTableauToFoundation(column)    tableau         -> foundation
    moveTableauToTableau(from, i, to)  tableau         -> tableau (group of cards)
    moveFoundationToTableau(suit, col) foundation      -> tableau
    undo()                             reverse the last move
"""

from Data_Structure.stack import Stack
from Data_Structure.queue import Queue
from Game.game_state import GameState


class GameLogic:
    """Checks and performs moves on a GameState. Keeps the undo history."""

    def __init__(self, drawCount=1):
        self.state = GameState()    # all the piles
        self.history = Stack()      # undo history: each item is a dictionary describing one move
        self.drawCount = drawCount  # 1 = draw one card, 3 = draw three cards

    def newGame(self):
        """Deal a new game and forget the old undo history."""
        self.state.newGame()
        self.history = Stack()

    # =====================================================================
    # RULES (these only CHECK, they never change anything)
    # =====================================================================

    def canPlaceOnTableau(self, card, column):
        """
        Tableau rule:
            - an empty column only accepts a King
            - otherwise the top card must be face-up,
              the opposite colour, and exactly one rank higher
        """
        pile = self.state.tableau[column]

        if pile.isEmpty():
            return card.rank == 13

        top = pile.peek()
        if not top.faceUp:
            return False
        if top.color() == card.color():
            return False
        return top.rank == card.rank + 1

    def canPlaceOnFoundation(self, card):
        """
        Foundation rule (same suit, going up):
            - an empty foundation only accepts an Ace
            - otherwise the card must be one rank higher than the top card
        The dictionary gives us the right foundation instantly: foundations[card.suit]
        """
        foundation = self.state.foundations[card.suit]

        if foundation.isEmpty():
            return card.rank == 1
        return foundation.peek().rank + 1 == card.rank

    def canPickUp(self, column, index):
        """
        Can the player select the card at this position in a column?
        Only face-up cards can be picked up. Every card below a face-up card
        is also face-up and already in valid order (the rules guarantee it),
        so the whole group from 'index' to the top can be moved together.
        """
        card = self.state.tableau[column].get(index)
        if card is None:
            return False
        return card.faceUp

    def isWon(self):
        """The game is won when all 52 cards are on the foundations."""
        total = 0
        for suit in self.state.foundations:
            total += self.state.foundations[suit].size()
        return total == 52

    # =====================================================================
    # SMALL HELPERS
    # =====================================================================

    def setLocation(self, card, pileType, key):
        """Update the dictionary that remembers where each card is."""
        self.state.cardLocations[card.cardId()] = (pileType, key)

    def flipTopCard(self, column):
        """
        After cards leave a column, turn its new top card face-up.
        Returns True if a card was flipped (undo needs to know this).
        """
        top = self.state.tableau[column].peek()
        if top is not None and not top.faceUp:
            top.flip()
            return True
        return False

    def recordMove(self, move):
        """Save a move on the undo stack and count it."""
        self.history.push(move)
        self.state.moveCount += 1

    # =====================================================================
    # STOCK AND WASTE
    # =====================================================================

    def drawFromStock(self):
        """
        Take 1 (or 3) cards from the FRONT of the stock queue,
        turn them face-up and push them onto the waste stack.
        If the stock is empty, recycle the waste back into the stock.
        """
        if self.state.stock.isEmpty():
            return self.recycleWaste()

        drawn = 0
        while drawn < self.drawCount and not self.state.stock.isEmpty():
            card = self.state.stock.dequeue()     # Queue: first in, first out
            card.flip()                           # face-up
            self.state.waste.push(card)           # Stack: newest on top
            self.setLocation(card, "waste", None)
            drawn += 1

        self.recordMove({"type": "draw", "count": drawn})
        return True

    def recycleWaste(self):
        """
        Stock is empty: put all waste cards back into the stock,
        in the SAME order they were first drawn.

        Popping the waste gives the cards backwards, so we pop them
        into a temporary stack first (this reverses them again).
        """
        if self.state.waste.isEmpty():
            return False

        temp = Stack()
        while not self.state.waste.isEmpty():
            temp.push(self.state.waste.pop())

        count = 0
        while not temp.isEmpty():
            card = temp.pop()
            card.flip()                           # face-down again
            self.state.stock.enqueue(card)
            self.setLocation(card, "stock", None)
            count += 1

        self.recordMove({"type": "recycle", "count": count})
        return True

    def moveWasteToTableau(self, column):
        """Move the top waste card onto a tableau column."""
        card = self.state.waste.peek()
        if card is None or not self.canPlaceOnTableau(card, column):
            return False

        self.state.waste.pop()
        self.state.tableau[column].append(card)
        self.setLocation(card, "tableau", column)

        self.recordMove({"type": "wasteToTableau", "to": column})
        return True

    def moveWasteToFoundation(self):
        """Move the top waste card onto its foundation."""
        card = self.state.waste.peek()
        if card is None or not self.canPlaceOnFoundation(card):
            return False

        self.state.waste.pop()
        self.state.foundations[card.suit].push(card)
        self.setLocation(card, "foundation", card.suit)

        self.recordMove({"type": "wasteToFoundation", "suit": card.suit})
        return True

    # =====================================================================
    # TABLEAU AND FOUNDATION
    # =====================================================================

    def moveTableauToFoundation(self, column):
        """Move the top card of a tableau column onto its foundation."""
        pile = self.state.tableau[column]
        card = pile.peek()
        if card is None or not card.faceUp or not self.canPlaceOnFoundation(card):
            return False

        pile.pop()
        self.state.foundations[card.suit].push(card)
        self.setLocation(card, "foundation", card.suit)
        flipped = self.flipTopCard(column)

        self.recordMove({"type": "tableauToFoundation", "from": column,
                         "suit": card.suit, "flipped": flipped})
        return True

    def moveTableauToTableau(self, fromColumn, index, toColumn):
        """
        Move the card at 'index' in fromColumn, AND every card on top of it,
        onto toColumn.

        Uses the linked list:
            splitFrom(index) cuts the group off the first column,
            extend(group)    attaches the whole group to the second column.
        """
        if fromColumn == toColumn:
            return False
        if not self.canPickUp(fromColumn, index):
            return False

        card = self.state.tableau[fromColumn].get(index)   # bottom card of the group
        if not self.canPlaceOnTableau(card, toColumn):
            return False

        group = self.state.tableau[fromColumn].splitFrom(index)
        count = group.size()
        for movedCard in group.toList():
            self.setLocation(movedCard, "tableau", toColumn)
        self.state.tableau[toColumn].extend(group)

        flipped = self.flipTopCard(fromColumn)

        self.recordMove({"type": "tableauToTableau", "from": fromColumn,
                         "to": toColumn, "count": count, "flipped": flipped})
        return True

    def moveFoundationToTableau(self, suit, column):
        """Move the top card of a foundation back down to a tableau column."""
        card = self.state.foundations[suit].peek()
        if card is None or not self.canPlaceOnTableau(card, column):
            return False

        self.state.foundations[suit].pop()
        self.state.tableau[column].append(card)
        self.setLocation(card, "tableau", column)

        self.recordMove({"type": "foundationToTableau", "suit": suit, "to": column})
        return True

    # =====================================================================
    # UNDO (pop the last move from the history stack and reverse it)
    # =====================================================================

    def undo(self):
        """Reverse the most recent move. Returns False if there is nothing to undo."""
        if self.history.isEmpty():
            return False

        move = self.history.pop()       # LIFO: the newest move comes out first
        moveType = move["type"]

        if moveType == "draw":
            self.undoDraw(move)
        elif moveType == "recycle":
            self.undoRecycle(move)
        elif moveType == "wasteToTableau":
            self.undoWasteToTableau(move)
        elif moveType == "wasteToFoundation":
            self.undoWasteToFoundation(move)
        elif moveType == "tableauToFoundation":
            self.undoTableauToFoundation(move)
        elif moveType == "tableauToTableau":
            self.undoTableauToTableau(move)
        elif moveType == "foundationToTableau":
            self.undoFoundationToTableau(move)

        self.state.moveCount -= 1
        return True

    def undoDraw(self, move):
        """
        Put drawn cards back at the FRONT of the stock.
        A queue can only add at the rear, so we build a new queue:
        first the returned cards (in their original order), then the old stock.
        """
        temp = Stack()
        for i in range(move["count"]):
            card = self.state.waste.pop()
            card.flip()                       # face-down again
            temp.push(card)                   # reverses: first-drawn card ends on top

        newStock = Queue()
        while not temp.isEmpty():
            card = temp.pop()
            newStock.enqueue(card)
            self.setLocation(card, "stock", None)
        while not self.state.stock.isEmpty():
            newStock.enqueue(self.state.stock.dequeue())

        self.state.stock = newStock

    def undoRecycle(self, move):
        """Move the recycled cards from the stock back onto the waste."""
        for i in range(move["count"]):
            card = self.state.stock.dequeue()
            card.flip()                       # face-up again
            self.state.waste.push(card)
            self.setLocation(card, "waste", None)

    def undoWasteToTableau(self, move):
        card = self.state.tableau[move["to"]].pop()
        self.state.waste.push(card)
        self.setLocation(card, "waste", None)

    def undoWasteToFoundation(self, move):
        card = self.state.foundations[move["suit"]].pop()
        self.state.waste.push(card)
        self.setLocation(card, "waste", None)

    def undoTableauToFoundation(self, move):
        column = move["from"]
        if move["flipped"]:
            self.state.tableau[column].peek().flip()   # turn it face-down again
        card = self.state.foundations[move["suit"]].pop()
        self.state.tableau[column].append(card)
        self.setLocation(card, "tableau", column)

    def undoTableauToTableau(self, move):
        fromPile = self.state.tableau[move["from"]]
        toPile = self.state.tableau[move["to"]]

        if move["flipped"]:
            fromPile.peek().flip()                     # turn it face-down again

        # The moved group is the last 'count' cards of the target column.
        group = toPile.splitFrom(toPile.size() - move["count"])
        for movedCard in group.toList():
            self.setLocation(movedCard, "tableau", move["from"])
        fromPile.extend(group)

    def undoFoundationToTableau(self, move):
        card = self.state.tableau[move["to"]].pop()
        self.state.foundations[move["suit"]].push(card)
        self.setLocation(card, "foundation", move["suit"])


# ---------- Quick demo ----------
# The full tests are in Tests/test_game_logic.py
if __name__ == "__main__":
    logic = GameLogic()
    logic.state.printState()

    print("\nDrawing one card from the stock...")
    logic.drawFromStock()
    print("Waste top:", logic.state.waste.peek(), "| stock left:", logic.state.stock.size())

    print("Undoing the draw...")
    logic.undo()
    print("Waste empty:", logic.state.waste.isEmpty(), "| stock:", logic.state.stock.size())