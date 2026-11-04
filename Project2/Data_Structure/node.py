"""
node.py
-------
A Node is one "box" in a chain.

    +--------+------+
    |  card  | next | ---> (another Node, or None at the end)
    +--------+------+

The LinkedList, Stack and Queue are all built by linking Nodes together.
"""


class Node:
    """One link in a chain: holds a Card and a reference to the next Node."""

    def __init__(self, card):
        self.card = card    # the Card object stored in this box
        self.next = None    # the next Node in the chain (None = no next box)

    def __str__(self):
        return "Node(" + str(self.card) + ")"


# ---------- Quick self-test ----------
if __name__ == "__main__":
    from Models.card import Card

    # Build a tiny chain by hand: 7♠ -> 6♥ -> None
    first = Node(Card("Spades", 7, faceUp=True))
    second = Node(Card("Hearts", 6, faceUp=True))
    first.next = second

    print("First node:", first)
    print("Next of first:", first.next)
    print("Next of second:", second.next)

    assert first.next is second
    assert second.next is None
    print("All Node tests passed!")