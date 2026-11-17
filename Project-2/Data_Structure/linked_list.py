"""
linked_list.py
--------------
A singly linked list of Cards, built from Node objects.

In our game this represents a TABLEAU PILE:

    head (bottom card)                          tail (top card)
    [K♠] ---> [Q♥] ---> [J♣] ---> [10♦] ---> None

- head = the bottom card of the pile (dealt first)
- tail = the top card of the pile (the one the player sees on top)

Stack-like operations (work on the TOP of the pile):
    append(card)  -> put a card on top
    pop()         -> remove the top card
    peek()        -> look at the top card

Extra linked-list operations (needed for moving a GROUP of cards):
    get(index)          -> card at a position
    splitFrom(index)   -> cut the chain and return the cut-off part
    extend(other_list)  -> attach another chain to the end of this one
"""

from Data_Structure.node import Node


class LinkedList:
    """A chain of Nodes. Each Node holds one Card."""

    def __init__(self):
        self.head = None   # first Node (bottom card), None if empty
        self.tail = None   # last Node (top card), None if empty
        self.count = 0     # how many Nodes are in the chain

    # ---------- Basic information ----------

    def isEmpty(self):
        """Return True if the list has no cards.  O(1)"""
        return self.count == 0

    def size(self):
        """Return the number of cards.  O(1) because we keep a counter."""
        return self.count

    # ---------- Stack-like operations on the top (tail) ----------

    def append(self, card):
        """
        Put a card at the END of the chain (top of the pile).
        O(1) because we already know where the tail is.
        """
        newNode = Node(card)

        if self.isEmpty():
            # The new node is both the first and the last node.
            self.head = newNode
            self.tail = newNode
        else:
            # Link the old last node to the new node, then move the tail.
            self.tail.next = newNode
            self.tail = newNode

        self.count += 1

    def peek(self):
        """Return the top card without removing it.  O(1)"""
        if self.isEmpty():
            return None
        return self.tail.card

    def pop(self):
        """
        Remove and return the top (last) card.

        In a singly linked list a node does not know which node is
        BEFORE it, so we must walk from the head to find the
        second-to-last node.  That makes this O(n).
        (n is at most 19 cards in a tableau pile, so it is fast enough.)
        """
        if self.isEmpty():
            return None

        topCard = self.tail.card

        # Case 1: only one node -> the list becomes empty.
        if self.head is self.tail:
            self.head = None
            self.tail = None
            self.count = 0
            return topCard

        # Case 2: walk until 'current' is the node just before the tail.
        current = self.head
        while current.next is not self.tail:
            current = current.next

        current.next = None    # cut off the old tail
        self.tail = current    # the node before it is the new tail
        self.count -= 1
        return topCard

    # ---------- Extra operations for groups of cards ----------

    def get(self, index):
        """
        Return the card at position 'index' (0 = bottom card).
        We walk the chain step by step, so this is O(n).
        """
        if index < 0 or index >= self.count:
            return None

        current = self.head
        steps = 0
        while steps < index:
            current = current.next
            steps += 1
        return current.card

    def splitFrom(self, index):
        """
        Cut the chain at 'index' and return everything from 'index'
        to the end as a NEW LinkedList.  This list keeps the rest.

        Example (index = 2):
            before:  [K♠] -> [Q♥] -> [J♣] -> [10♦]
            this:    [K♠] -> [Q♥]
            returns: [J♣] -> [10♦]

        Used when the player moves a group of face-up cards. O(n)
        """
        if index < 0 or index >= self.count:
            return LinkedList()   # nothing to cut, return an empty list

        moved = LinkedList()

        if index == 0:
            # Take the whole chain.
            moved.head = self.head
            moved.tail = self.tail
            moved.count = self.count
            self.head = None
            self.tail = None
            self.count = 0
            return moved

        # Walk to the node just BEFORE the cut point.
        before = self.head
        steps = 0
        while steps < index - 1:
            before = before.next
            steps += 1

        # The cut-off part starts right after 'before'.
        moved.head = before.next
        moved.tail = self.tail
        moved.count = self.count - index

        # This list now ends at 'before'.
        before.next = None
        self.tail = before
        self.count = index

        return moved

    def extend(self, other):
        """
        Attach the whole 'other' chain to the end of this chain.
        No cards are copied: we only change one 'next' arrow.  O(1)

        After this, 'other' is emptied so the same nodes are never
        part of two lists at once.
        """
        if other.isEmpty():
            return

        if self.isEmpty():
            self.head = other.head
        else:
            self.tail.next = other.head

        self.tail = other.tail
        self.count += other.count

        # Empty the other list.
        other.head = None
        other.tail = None
        other.count = 0

    # ---------- Helpers for display and testing ----------

    def toList(self):
        """
        Return the cards as a normal Python list, bottom to top.
        The UI uses this to draw a pile from top of screen to bottom.  O(n)
        """
        cards = []
        current = self.head
        while current is not None:
            cards.append(current.card)
            current = current.next
        return cards

    def __str__(self):
        """Example output: [K♠] -> Q♥ -> J♣ -> None"""
        text = ""
        current = self.head
        while current is not None:
            text += str(current.card) + " -> "
            current = current.next
        return text + "None"


# ---------- Quick self-test ----------
if __name__ == "__main__":
    from Models.card import Card

    pile = LinkedList()
    print("Empty pile:", pile, "| size:", pile.size())
    assert pile.isEmpty()
    assert pile.pop() is None
    assert pile.peek() is None

    # Build a pile: K♠ (face-down), then Q♥, J♣, 10♦ face-up
    pile.append(Card("Spades", 13))
    pile.append(Card("Hearts", 12, faceUp=True))
    pile.append(Card("Clubs", 11, faceUp=True))
    pile.append(Card("Diamonds", 10, faceUp=True))
    print("Pile:", pile, "| size:", pile.size())
    assert pile.size() == 4
    assert pile.peek().cardId() == "10♦"
    assert pile.get(1).cardId() == "Q♥"

    # pop removes the top card
    top = pile.pop()
    print("Popped:", top, "| pile now:", pile)
    assert top.cardId() == "10♦"
    assert pile.peek().cardId() == "J♣"
    assert pile.size() == 3

    # splitFrom: move Q♥ and J♣ to another pile
    group = pile.splitFrom(1)
    print("Split group:", group, "| left behind:", pile)
    assert group.size() == 2
    assert pile.size() == 1
    assert pile.peek().cardId() == "K♠"

    # extend: attach the group onto a different pile
    other = LinkedList()
    other.append(Card("Spades", 13, faceUp=True))
    other.extend(group)
    print("Other after extend:", other)
    assert other.size() == 3
    assert other.peek().cardId() == "J♣"
    assert group.isEmpty()

    # splitFrom(0) takes everything
    everything = other.splitFrom(0)
    assert other.isEmpty() and everything.size() == 3

    # pop down to empty
    while not everything.isEmpty():
        everything.pop()
    assert everything.head is None and everything.tail is None

    print("All LinkedList tests passed!")