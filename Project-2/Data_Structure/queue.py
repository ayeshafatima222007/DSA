"""
queue.py
--------
A Queue follows FIFO: First In, First Out.
The first card that goes in is the first card that comes out,
just like people standing in a line.

    enqueue(A)  enqueue(B)  enqueue(C)        dequeue() -> A

    front                      rear
     [A] ---> [B] ---> [C] ---> None
      ^ cards leave here         ^ cards join here

In our game the Queue is used for the STOCKPILE (the face-down
draw pile). Cards are drawn from the front, in the same order they
were placed in the stockpile.

The Queue is built directly from Node objects with TWO pointers:
    frontNode -> where cards are removed
    rearNode  -> where cards are added
Because we know both ends, adding AND removing are both O(1).
"""

from Data_Structure.node import Node


class Queue:
    """A FIFO queue built from linked Nodes."""

    def __init__(self):
        self.frontNode = None   # first Node in line (next to be removed)
        self.rearNode = None    # last Node in line (most recently added)
        self.count = 0          # how many items are in the queue

    def enqueue(self, item):
        """
        Add an item at the REAR (back of the line).  O(1)
        """
        newNode = Node(item)

        if self.isEmpty():
            # The only node is both the front and the rear.
            self.frontNode = newNode
            self.rearNode = newNode
        else:
            # Link the old rear to the new node, then move the rear.
            self.rearNode.next = newNode
            self.rearNode = newNode

        self.count += 1

    def dequeue(self):
        """
        Remove and return the item at the FRONT.  O(1)
        Returns None if the queue is empty.
        """
        if self.isEmpty():
            return None

        frontItem = self.frontNode.card
        self.frontNode = self.frontNode.next   # the second node becomes the front
        self.count -= 1

        # If the queue is now empty, the rear must be cleared too.
        if self.frontNode is None:
            self.rearNode = None

        return frontItem

    def front(self):
        """Return the front item WITHOUT removing it.  O(1)"""
        if self.isEmpty():
            return None
        return self.frontNode.card

    def isEmpty(self):
        """Return True if the queue has no items.  O(1)"""
        return self.count == 0

    def size(self):
        """Return the number of items.  O(1)"""
        return self.count

    def toList(self):
        """
        Return all items as a Python list, front to rear.
        Only used for testing and debugging.  O(n)
        """
        items = []
        current = self.frontNode
        while current is not None:
            items.append(current.card)
            current = current.next
        return items

    def __str__(self):
        return "Queue(front -> rear): " + str(self.toList())


# ---------- Quick self-test ----------
if __name__ == "__main__":
    from Models.card import Card
    from Data_Structure.stack import Stack

    stock = Queue()
    print("New queue:", stock, "| empty:", stock.isEmpty())
    assert stock.isEmpty()
    assert stock.dequeue() is None
    assert stock.front() is None

    # Put three cards into the stockpile
    stock.enqueue(Card("Clubs", 5))
    stock.enqueue(Card("Clubs", 6))
    stock.enqueue(Card("Clubs", 7))
    print("After 3 enqueues:", stock)
    assert stock.size() == 3
    assert stock.front().cardId() == "5♣"

    # FIFO: the first card in (5♣) is the first card out
    first = stock.dequeue()
    print("Dequeued:", first, "| queue now:", stock)
    assert first.cardId() == "5♣"
    assert stock.front().cardId() == "6♣"

    # Empty it completely: front AND rear must become None
    stock.dequeue()
    stock.dequeue()
    assert stock.isEmpty()
    assert stock.frontNode is None and stock.rearNode is None

    # Enqueue after emptying must still work
    stock.enqueue(Card("Hearts", 1))
    assert stock.front().cardId() == "A♥" and stock.size() == 1
    stock.dequeue()

    # ----- Full stockpile cycle: draw -> waste -> recycle -----
    for rank in [5, 6, 7]:
        stock.enqueue(Card("Clubs", rank))

    waste = Stack()
    while not stock.isEmpty():          # draw every card
        card = stock.dequeue()
        card.flip()                     # drawn cards are face-up
        waste.push(card)
    print("Waste after drawing all:", waste)

    temp = Stack()                      # reverse the waste...
    while not waste.isEmpty():
        temp.push(waste.pop())
    while not temp.isEmpty():           # ...then refill the stock
        card = temp.pop()
        card.flip()                     # back to face-down
        stock.enqueue(card)
    print("Stock after recycling:", stock)
    order = []
    for card in stock.toList():
        order.append(card.cardId())
    assert order == ["5♣", "6♣", "7♣"]

    print("All Queue tests passed!")