"""
start_menu.py
-------------
The menu shown BEFORE the game starts (and when the player presses "Menu").
It is one panel with two columns:

    +--------------------------------+----------------------------+
    |  CSC200 · DSA PROJECT          |  Ready to play?            |
    |      (fan of 5 cards)          |  CARDS PER DRAW            |
    |     Klondike Solitaire         |  [ Draw 1 | Draw 3 ]       |
    |  STACK · QUEUE · LINKED ...    |  [ Resume game ] (only when a game is running)
    |  (blue "felt" side)            |  [ Start game  ]           |
    |                                |  [ How to play ]           |
    |                                |  [ Exit        ]           |
    +--------------------------------+----------------------------+

The menu does not start the game itself. It only sends SIGNALS,
and the main window decides what to do:
    startClicked(drawCount)  -> deal a new game with 1 or 3 cards per draw
    resumeClicked()          -> go back to the running game
    exitClicked()            -> close the program
"""

from PyQt6.QtCore import Qt, QRectF, pyqtSignal
from PyQt6.QtGui import QPainter
from PyQt6.QtWidgets import (QWidget, QLabel, QPushButton, QFrame,
                             QVBoxLayout, QHBoxLayout, QButtonGroup)

from Models.card import Card
from UI import card_painter

RULES_TEXT = (
    "<b>Goal:</b> move all 52 cards to the four foundations, "
    "from Ace up to King in each suit.<br><br>"
    "<b>Tableau:</b> build columns DOWN in alternating colours "
    "(a red 6 goes on a black 7). Only a King can go into an empty column.<br><br>"
    "<b>Stock:</b> click it to turn over 1 (or 3) cards onto the waste. "
    "When it is empty, click it again to recycle the waste.<br><br>"
    "<b>Controls:</b> click a card, then click where it should go. "
    "Double-click sends a card to its foundation.<br>"
    "Ctrl+Z undo &nbsp;·&nbsp; Ctrl+Y redo &nbsp;·&nbsp; H hint"
)


class CardFan(QWidget):
    """A small decoration: five cards spread like a hand, drawn with QPainter."""

    def __init__(self):
        super().__init__()
        self.cards = [Card("Hearts", 1, True), Card("Spades", 13, True),
                      Card("Diamonds", 12, True), Card("Clubs", 11, True),
                      Card("Hearts", 10, True)]
        self.setFixedSize(380, 170)

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        painter.setRenderHint(QPainter.RenderHint.TextAntialiasing)

        # Every card turns around the same point, 100 pixels BELOW the widget.
        # The card sits 140 pixels above that point, so the turned cards spread out.
        cardRect = QRectF(-43, -260, 86, 120)
        angles = [-24, -12, 0, 12, 24]              # each card is turned a little more

        for i in range(len(self.cards)):
            painter.save()
            painter.translate(self.width() / 2, self.height() + 100)
            painter.rotate(angles[i])
            card_painter.drawCardFace(painter, cardRect, self.cards[i])
            painter.restore()
        painter.end()


class StartMenu(QWidget):
    """The start screen. Talks to the main window only through signals."""

    startClicked = pyqtSignal(int)      # sends the chosen draw count (1 or 3)
    resumeClicked = pyqtSignal()
    exitClicked = pyqtSignal()

    def __init__(self):
        super().__init__()
        self.setObjectName("menuPage")
        self.setAttribute(Qt.WidgetAttribute.WA_StyledBackground, True)

        # The whole menu is one column in the middle of the screen.
        outer = QVBoxLayout(self)
        outer.addStretch()
        row = QHBoxLayout()
        row.addStretch()
        row.addWidget(self.buildPanel())
        row.addStretch()
        outer.addLayout(row)
        outer.addStretch()

    def makeButton(self, text, styleName):
        button = QPushButton(text)
        button.setObjectName(styleName)
        button.setCursor(Qt.CursorShape.PointingHandCursor)
        return button

    def buildPanel(self):
        """The menu card: a blue side with the title (left), options on the right."""
        panel = QFrame()
        panel.setObjectName("menuPanel")
        panel.setFixedWidth(880)

        row = QHBoxLayout(panel)
        row.setContentsMargins(14, 14, 14, 14)
        row.setSpacing(0)
        row.addWidget(self.buildTitleSide())
        row.addLayout(self.buildOptionsSide(), 1)
        return panel

    def buildTitleSide(self):
        """Left column: tag, card fan, title, tagline and subtitle."""
        side = QFrame()
        side.setObjectName("menuSide")
        side.setFixedWidth(430)

        box = QVBoxLayout(side)
        box.setContentsMargins(24, 26, 24, 30)
        box.setSpacing(10)

        tag = QLabel("CSC200  ·  DSA PROJECT")
        tag.setObjectName("menuTag")
        tag.setAlignment(Qt.AlignmentFlag.AlignCenter)
        box.addWidget(tag)
        box.addStretch()

        fanRow = QHBoxLayout()
        fanRow.addStretch()
        fanRow.addWidget(CardFan())
        fanRow.addStretch()
        box.addLayout(fanRow)

        title = QLabel("Klondike Solitaire")
        title.setObjectName("menuTitle")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        tagline = QLabel("STACK  ·  QUEUE  ·  LINKED LIST  ·  LIST  ·  DICTIONARY")
        tagline.setObjectName("menuTagline")
        tagline.setAlignment(Qt.AlignmentFlag.AlignCenter)
        box.addWidget(title)
        box.addWidget(tagline)
        box.addStretch()
        return side

    def buildOptionsSide(self):
        """Right column: draw choice and the main buttons."""
        box = QVBoxLayout()
        box.setContentsMargins(36, 30, 26, 30)
        box.setSpacing(12)

        heading = QLabel("Ready to play?")
        heading.setObjectName("panelHeading")
        subtitle = QLabel("Choose a mode and deal the cards.")
        subtitle.setObjectName("subtitle")
        box.addWidget(heading)
        box.addWidget(subtitle)
        box.addSpacing(10)

        # Draw 1 / Draw 3 choice (only one can be checked)
        caption = QLabel("CARDS PER DRAW")
        caption.setObjectName("sectionLabel")
        box.addWidget(caption)

        self.drawOneButton = self.makeButton("Draw 1  ·  easier", "segmentLeft")
        self.drawThreeButton = self.makeButton("Draw 3  ·  classic", "segmentRight")
        self.drawOneButton.setCheckable(True)
        self.drawThreeButton.setCheckable(True)
        self.drawOneButton.setChecked(True)
        self.drawGroup = QButtonGroup(self)
        self.drawGroup.addButton(self.drawOneButton)
        self.drawGroup.addButton(self.drawThreeButton)

        switch = QHBoxLayout()
        switch.setSpacing(0)
        switch.addWidget(self.drawOneButton, 1)
        switch.addWidget(self.drawThreeButton, 1)
        box.addLayout(switch)
        box.addSpacing(10)

        # Main buttons
        self.resumeButton = self.makeButton("Resume game", "menuButton")
        self.startButton = self.makeButton("Start game", "menuPrimary")
        self.rulesButton = self.makeButton("How to play", "menuButton")
        self.exitButton = self.makeButton("Exit", "menuButton")
        self.resumeButton.setVisible(False)           # only shown while a game is running
        self.resumeButton.setShortcut("Esc")          # Esc switches between game and menu
        self.rulesButton.setCheckable(True)

        self.rulesText = QLabel(RULES_TEXT)
        self.rulesText.setObjectName("rulesText")
        self.rulesText.setWordWrap(True)
        self.rulesText.setVisible(False)

        box.addWidget(self.resumeButton)
        box.addWidget(self.startButton)
        box.addWidget(self.rulesButton)
        box.addWidget(self.rulesText)
        box.addWidget(self.exitButton)
        box.addStretch()

        self.startButton.clicked.connect(self.onStart)
        self.resumeButton.clicked.connect(self.resumeClicked.emit)
        self.exitButton.clicked.connect(self.exitClicked.emit)
        self.rulesButton.toggled.connect(self.rulesText.setVisible)
        return box

    def onStart(self):
        """Send the chosen draw count to the main window."""
        if self.drawThreeButton.isChecked():
            self.startClicked.emit(3)
        else:
            self.startClicked.emit(1)

    def setGameRunning(self, running, drawCount):
        """
        Called by the main window before the menu is shown.
        If a game is running, show "Resume game" and call the other button "New game".
        """
        self.resumeButton.setVisible(running)
        if running:
            self.startButton.setText("New game")
            self.setButtonStyle(self.resumeButton, "menuPrimary")   # gold = the main action
            self.setButtonStyle(self.startButton, "menuButton")
        else:
            self.startButton.setText("Start game")
            self.setButtonStyle(self.startButton, "menuPrimary")
        self.drawOneButton.setChecked(drawCount == 1)
        self.drawThreeButton.setChecked(drawCount == 3)

    def setButtonStyle(self, button, styleName):
        """Change which style sheet rule a button uses, and redraw it."""
        button.setObjectName(styleName)
        button.style().unpolish(button)     # forget the old style...
        button.style().polish(button)       # ...and apply the new one