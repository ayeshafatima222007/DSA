# Klondike Solitaire — CSC200 Data Structures & Algorithms

A Klondike Solitaire game written in Python with a PyQt6 interface.
The main goal of the project is to use five data structures — **Stack, Queue,
Linked List, Python List and Dictionary** — for real game operations.

## How to run

Requirements: Python 3.9 or newer and PyQt6.

```
pip install PyQt6
python main.py
```

Run all tests (no window needed):

```
python -m Test.run_all_tests
```

Every data-structure file also has its own small self-test, for example:

```
python -m Data_Structure.queue
```

## How to play

The program opens on a **start menu**: choose Draw 1 or Draw 3, then press
**Start game**. **How to play** shows the rules, and **Exit** closes the program.

| Action | Result |
|---|---|
| **Menu** (Esc) | Pause the game and open the menu; **Resume game** (or Esc again) continues it |
| Click the stock | Draw 1 (or 3) cards. When the stock is empty, the waste is recycled. |
| Click a card, then click a target pile | Move the card (and every card on top of it) |
| Double-click a top card | Send it to its foundation |
| **Undo** (Ctrl+Z) | Reverse the last move |
| **Redo** (Ctrl+Y) | Do an undone move again |
| **Hint** (H) | Outline the best card in gold and where it should go in dashed mint |
| **Insights** panel | Live view of the data structures: foundation progress per suit, the newest moves from the undo stack, and the size of every structure |
| **Draw 1 / Draw 3** switch | Change the draw mode (starts a new game) |
| **New deal** (Ctrl+N) | Shuffle and deal again |

Rules: tableau cards go down in rank with alternating colours; only a King may
go into an empty column; foundations are built from Ace to King in one suit.
The game is won when all 52 cards are on the foundations.

### Scoring (standard Windows Solitaire values)

| Move | Points |
|---|---|
| Waste → tableau | +5 |
| Waste → foundation | +10 |
| Tableau → foundation | +10 |
| Turning over a tableau card | +5 |
| Foundation → tableau | −15 |
| Recycling the waste into the stock | −100 (draw-1) / −20 (draw-3) |

The score never goes below 0. Undo takes the points back, and redo gives them again.

## Project structure

```
Project2/
├── main.py                    Starts the application
├── Models/
│   └── card.py                Card class (suit, rank, faceUp)
├── Data_Structure/
│   ├── node.py                Node: one card + reference to the next node
│   ├── linked_list.py         Singly linked list (head, tail, count)
│   ├── stack.py               Stack built on the LinkedList (LIFO)
│   └── queue.py               Queue built on Nodes with front/rear (FIFO)
├── Game/
│   ├── deck.py                52 cards in a Python list + shuffle
│   ├── game_state.py          All piles and dictionaries, dealing a new game
│   └── game_logic.py          Rules, moves, flipping, undo/redo, scoring, hint, win check
├── UI/
│   ├── styles.py              Colours, sizes and the Qt style sheet
│   ├── card_painter.py        Draws cards with QPainter (no images)
│   ├── start_menu.py          Start menu: card fan, draw choice, rules, start/resume/exit
│   ├── game_board.py          Draws the felt panels and all piles, turns clicks into moves
│   └── main_window.py         Top bar with stats, control dock, live insights panel
└── Test/
    ├── test_setup.py          Data structures, deck, starting deal, new game
    ├── test_game_logic.py     Rules, moves, flipping, undo/redo, scoring, win, hint, random games
    └── run_all_tests.py       Runs every test
```

The game logic (`Models`, `Data_Structure`, `Game`) never imports PyQt6, so all
rules can be tested from the terminal without the interface.

## Where each data structure is used

| Data structure | Used for | Why it fits |
|---|---|---|
| **Python list** | `Deck.cards`: creating and shuffling 52 cards | `random.shuffle` needs direct access to any position |
| **Queue** (custom) | Stockpile | Cards are drawn in the order they were placed (FIFO) |
| **Stack** (custom) | 4 foundations, waste pile, undo history, redo history | Only the top item is ever used (LIFO) |
| **Linked List** (custom) | 7 tableau columns | A group of cards moves by cutting and re-linking the chain |
| **Dictionary** | `tableau` {1..7 → LinkedList}, `foundations` {suit → Stack}, `cardLocations` {"Q♥" → ("tableau", 3)}, `SCORE_TABLE` {move type → points}, each move record | O(1) lookup by key instead of searching |

The Stack uses the LinkedList inside it (composition): `push` calls `append`
and `pop` calls `pop`. The Queue uses Nodes directly with `frontNode` and
`rearNode` so that both `enqueue` and `dequeue` are O(1).

### How one card moves through the data structures

```
created in deck.cards (list) → shuffled → dealCard() pops it
→ enqueued in the stock (Queue)
→ drawn: dequeued, flipped, pushed on the waste (Stack)
→ moved: popped from the waste, appended to tableau[4] (LinkedList)
→ moved: popped from the column, pushed on foundations["Hearts"] (Stack)
every step: cardLocations[...] updated (Dictionary), move pushed on undo history (Stack)
```

## Time complexity

| Operation | Complexity | Reason |
|---|---|---|
| Stack `push`, `peek`, `size`, `isEmpty` | O(1) | Tail and counter are stored |
| Stack `pop` / LinkedList `pop` | O(n) | Singly linked: must walk to the second-last node (n ≤ 19) |
| Queue `enqueue`, `dequeue`, `front` | O(1) | Front and rear pointers are stored |
| LinkedList `extend` | O(1) | Only one `next` reference changes |
| LinkedList `get`, `splitFrom` | O(n) | Must walk the chain |
| Dictionary lookup | O(1) on average | Hashing |
| Shuffle | O(n) | `random.shuffle` |

A doubly linked list would make `pop` O(1); the singly linked version was kept
because it is simpler and the piles are small.

## Every move follows the same four steps

1. **Check** — is the move legal? If not, nothing changes.
2. **Move** — take the card(s) from one data structure, put them in another.
3. **Update** — update `cardLocations` and flip the newly exposed card.
4. **Record** — push a dictionary describing the move onto the undo Stack,
   and add its points (from `SCORE_TABLE`) to the score.

### Undo and redo use two stacks

```
make a move  → push on history,     clear redoHistory
undo()       → pop from history,    reverse it,      push on redoHistory
redo()       → pop from redoHistory, do it again,    push on history
```

Undo puts the game back exactly as it was before the move, so redo simply
calls the same move function again with the values saved in the move record.
A new move clears the redo history, because the undone moves no longer fit
the new position.

## Testing

`python -m Test.run_all_tests` checks:

- Stack is LIFO, Queue is FIFO, LinkedList split/extend work
- the deck has 52 different cards
- 100 random deals: 52 cards, 7 columns with 1–7 cards, only top cards face-up, 24 in the stock
- tableau and foundation rules (valid and invalid moves)
- moving a group of cards and flipping the exposed card
- invalid moves change nothing
- drawing, recycling the stock, draw-3 mode
- undo and redo of every kind of move
- scoring, including undo/redo of points and the 0 minimum
- win detection and hints
- every hint the game suggests is a legal move (checked in 50 random games)
- 200 random games (about 80,000 move attempts): after each attempt all 52
  cards are present, every location in the dictionary is correct and the score
  is not negative; then every move is undone back to the starting deal (score 0),
  and every move is redone back to the final position and score

## Features

Mandatory (from the project PDF): card class, shuffled deck, 7-column deal,
FIFO stockpile with draw 1 or 3, tableau and foundation rules, moves between
piles, card flipping, undo, win detection, tests.

Bonus (all items from the PDF): undo/redo, hints, timer and scoring — plus a
move counter, keyboard shortcuts, a live insights panel that shows the data structures,
and a navy-and-gold PyQt6 interface with QPainter-drawn cards that resize with the window.

Not implemented (not required): drag-and-drop, animations.