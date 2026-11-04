"""
stack.py
--------
A Stack follows LIFO: Last In, First Out.
The last card you put on is the first card you take off,
just like a real pile of cards on a table.

    push(A♥)  push(2♥)  push(3♥)        pop() -> 3♥

                          [3♥]  <- top
                [2♥]      [2♥]
      [A♥]      [A♥]      [A♥]

In our game a Stack is used for:
    - the 4 foundation piles (Ace up to King of one suit)
    - the waste pile (cards drawn from the stockpile)
    - the undo history (list of moves, newest on top)

This Stack does NOT store cards itself. It uses our own LinkedList
inside it. The Stack only allows the "top" operations, so the
LIFO rule can never be broken from outside.
"""

from Data_Structure.linked_list import LinkedList


class Stack:
    """A LIFO stack built on top of our custom LinkedList."""

    def __init__(self):
        # The linked list that really stores the items.
        # Its tail is the TOP of the stack.
        self.items = LinkedList()

    def push(self, item):
        """Put an item on top of the stack.  O(1)"""
        self.items.append(item)

    def pop(self):
        """
        Remove and return the top item.
        Returns None if the stack is empty.
        O(n) because LinkedList.pop() walks to the second-last node.
        """
        return self.items.pop()

    def peek(self):
        """Return the top item WITHOUT removing it.  O(1)"""
        return self.items.peek()

    def isEmpty(self):
        """Return True if the stack has no items.  O(1)"""
        return self.items.isEmpty()

    def size(self):
        """Return the number of items in the stack.  O(1)"""
        return self.items.size()

    def toList(self):
        """
        Return all items as a Python list, bottom to top.
        Only used for DRAWING the pile on screen and for testing.
        The game logic itself only uses push / pop / peek.
        """
        return self.items.toList()

    def __str__(self):
        return "Stack(bottom -> top): " + str(self.items.toList())


# ---------- Quick self-test ----------
if __name__ == "__main__":
    from Models.card import Card

    hearts = Stack()
    print("New stack:", hearts, "| empty:", hearts.isEmpty())
    assert hearts.isEmpty()
    assert hearts.pop() is None
    assert hearts.peek() is None

    # Build a foundation: A♥, 2♥, 3♥
    hearts.push(Card("Hearts", 1, faceUp=True))
    hearts.push(Card("Hearts", 2, faceUp=True))
    hearts.push(Card("Hearts", 3, faceUp=True))
    print("After 3 pushes:", hearts)
    assert hearts.size() == 3
    assert hearts.peek().cardId() == "3♥"

    # LIFO: the last card pushed (3♥) comes out first
    top = hearts.pop()
    print("Popped:", top, "| stack now:", hearts)
    assert top.cardId() == "3♥"
    assert hearts.peek().cardId() == "2♥"
    assert hearts.size() == 2

    # Reversing order with a stack (used later to recycle the waste pile)
    waste = Stack()
    for rank in [5, 6, 7]:
        waste.push(Card("Clubs", rank, faceUp=True))
    temp = Stack()
    while not waste.isEmpty():
        temp.push(waste.pop())
    print("Waste reversed into temp:", temp)
    assert temp.peek().cardId() == "5♣"   # the first card pushed is now on top

    print("All Stack tests passed!")