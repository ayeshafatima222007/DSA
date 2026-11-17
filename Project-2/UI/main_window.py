from PyQt6.QtCore import Qt, QTimer
from PyQt6.QtWidgets import (QMainWindow, QWidget, QLabel, QPushButton, QFrame,
                             QHBoxLayout, QVBoxLayout, QGridLayout, QButtonGroup,
                             QProgressBar, QMessageBox, QStackedWidget)

from Models.card import SUITS, SUIT_SYMBOLS, RED_SUITS
from Game.game_logic import GameLogic
from UI.game_board import GameBoard
from UI.start_menu import StartMenu
from UI import styles

DEFAULT_TIP = "Click a card, then click where it should go. Double-click sends it home."
HISTORY_ROWS = 6        # how many recent moves the insights panel shows


class MainWindow(QMainWindow):

    def __init__(self):
        super().__init__()
        self.logic = GameLogic(drawCount=1)    # the whole game (data structures + rules)
        self.secondsPlayed = 0                 # for the timer
        self.gameOver = False                  # True after the player wins
        self.statLabels = {}                   # dictionary: caption -> value QLabel (top bar)
        self.suitBars = {}                     # dictionary: suit -> QProgressBar
        self.suitCounts = {}                   # dictionary: suit -> QLabel "3/13"
        self.dsValues = {}                     # dictionary: data structure name -> QLabel

        self.setWindowTitle("Klondike Solitaire - CSC200 Data Structures")
        self.resize(1340, 880)
        self.setMinimumSize(1060, 700)
        self.setStyleSheet(styles.WINDOW_STYLE)

        self.buildLayout()

        # QTimer calls tick() once every 1000 ms (1 second).
        # It is started when the player leaves the menu.
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.tick)

        self.showMessage(DEFAULT_TIP, "info")
        self.refresh()
        self.pages.setCurrentWidget(self.menu)     # the program starts on the menu

    # =====================================================================
    # BUILDING THE WINDOW
    # =====================================================================

    def buildLayout(self):
        """Create the two pages and put them in a QStackedWidget."""
        self.menu = StartMenu()
        self.menu.startClicked.connect(self.startFromMenu)
        self.menu.resumeClicked.connect(self.resumeGame)
        self.menu.exitClicked.connect(self.close)

        self.gamePage = self.buildGamePage()

        self.pages = QStackedWidget()
        self.pages.addWidget(self.menu)
        self.pages.addWidget(self.gamePage)
        self.setCentralWidget(self.pages)

    def buildGamePage(self):
        page = QWidget()
        page.setObjectName("central")          # matches "QWidget#central" in the style sheet
        page.setAttribute(Qt.WidgetAttribute.WA_StyledBackground, True)

        layout = QVBoxLayout(page)
        layout.setContentsMargins(20, 16, 20, 16)
        layout.setSpacing(14)

        self.board = GameBoard(self.logic)
        self.board.changed.connect(self.onBoardChanged)    # after every successful move
        self.board.message.connect(self.showMessage)       # errors and other messages

        # Left side: board + control dock.  Right side: insights panel.
        leftSide = QVBoxLayout()
        leftSide.setSpacing(12)
        leftSide.addWidget(self.board, 1)      # 1 = the board takes all spare space
        leftSide.addWidget(self.buildDock())

        body = QHBoxLayout()
        body.setSpacing(16)
        body.addLayout(leftSide, 1)
        body.addWidget(self.buildInsightsPanel())

        layout.addWidget(self.buildTopBar())
        layout.addLayout(body, 1)
        return page

    def makeButton(self, text, styleName=""):
        button = QPushButton(text)
        if styleName != "":
            button.setObjectName(styleName)    # picks the colour from the style sheet
        button.setCursor(Qt.CursorShape.PointingHandCursor)
        return button

    def makeLabel(self, text, styleName, wrap=False):
        label = QLabel(text)
        label.setObjectName(styleName)
        label.setWordWrap(wrap)
        return label

    def makeDivider(self):
        line = QFrame()
        line.setObjectName("divider")
        return line

    # ---------- top bar: menu, title, stats, draw mode ----------

    def makeStatPill(self, caption):
        """A small box with a caption and a value, e.g.  MOVES / 18."""
        pill = QFrame()
        pill.setObjectName("statPill")
        box = QVBoxLayout(pill)
        box.setContentsMargins(14, 5, 14, 6)
        box.setSpacing(0)
        box.addWidget(self.makeLabel(caption.upper(), "pillCaption"))
        value = self.makeLabel("-", "pillValue")
        box.addWidget(value)
        self.statLabels[caption] = value       # remember it so we can update it later
        return pill

    def buildTopBar(self):
        bar = QFrame()
        bar.setObjectName("topBar")
        row = QHBoxLayout(bar)
        row.setContentsMargins(14, 10, 14, 10)
        row.setSpacing(10)

        self.menuButton = self.makeButton("☰  Menu")
        self.menuButton.setShortcut("Esc")
        self.menuButton.setToolTip("Pause and open the menu (Esc)")
        self.menuButton.clicked.connect(self.openMenu)
        row.addWidget(self.menuButton)
        row.addSpacing(6)

        titleBox = QVBoxLayout()
        titleBox.setSpacing(0)
        titleBox.addWidget(self.makeLabel("Klondike Solitaire", "title"))
        self.subtitle = self.makeLabel("", "subtitle")
        titleBox.addWidget(self.subtitle)
        row.addLayout(titleBox)
        row.addStretch()

        for caption in ["Time", "Moves", "Score", "Hidden"]:
            row.addWidget(self.makeStatPill(caption))
        row.addStretch()

        # Draw 1 / Draw 3 switch: two buttons where only one can be checked.
        self.drawOneButton = self.makeButton("Draw 1", "segmentLeft")
        self.drawThreeButton = self.makeButton("Draw 3", "segmentRight")
        self.drawOneButton.setCheckable(True)
        self.drawThreeButton.setCheckable(True)
        self.drawOneButton.setChecked(True)
        self.drawGroup = QButtonGroup(self)
        self.drawGroup.setExclusive(True)
        self.drawGroup.addButton(self.drawOneButton)
        self.drawGroup.addButton(self.drawThreeButton)
        self.drawOneButton.clicked.connect(self.chooseDrawOne)
        self.drawThreeButton.clicked.connect(self.chooseDrawThree)

        switch = QHBoxLayout()
        switch.setSpacing(0)
        switch.addWidget(self.drawOneButton)
        switch.addWidget(self.drawThreeButton)
        row.addLayout(switch)
        return bar

    # ---------- control dock: status message + game buttons ----------

    def buildDock(self):
        dock = QFrame()
        dock.setObjectName("dock")
        row = QHBoxLayout(dock)
        row.setContentsMargins(16, 10, 12, 10)
        row.setSpacing(8)

        self.statusDot = QLabel()
        self.statusDot.setFixedSize(10, 10)
        self.statusText = self.makeLabel("", "statusText", wrap=True)
        row.addWidget(self.statusDot)
        row.addSpacing(4)
        row.addWidget(self.statusText, 1)

        self.undoButton = self.makeButton("↶  Undo")
        self.redoButton = self.makeButton("↷  Redo")
        self.hintButton = self.makeButton("★  Hint", "goldButton")
        self.newGameButton = self.makeButton("New deal")
        self.panelButton = self.makeButton("Insights", "panelToggle")
        self.panelButton.setCheckable(True)
        self.panelButton.setChecked(True)

        # Keyboard shortcuts and tooltips
        self.undoButton.setShortcut("Ctrl+Z")
        self.redoButton.setShortcut("Ctrl+Y")
        self.hintButton.setShortcut("H")
        self.newGameButton.setShortcut("Ctrl+N")
        self.undoButton.setToolTip("Undo the last move (Ctrl+Z)")
        self.redoButton.setToolTip("Redo an undone move (Ctrl+Y)")
        self.hintButton.setToolTip("Show the best move on the board (H)")
        self.newGameButton.setToolTip("Shuffle and deal a new game (Ctrl+N)")
        self.panelButton.setToolTip("Show or hide the insights panel")

        for button in [self.undoButton, self.redoButton, self.hintButton,
                       self.newGameButton, self.panelButton]:
            row.addWidget(button)

        self.undoButton.clicked.connect(self.undoMove)
        self.redoButton.clicked.connect(self.redoMove)
        self.hintButton.clicked.connect(self.showHint)
        self.newGameButton.clicked.connect(self.startNewGame)
        self.panelButton.toggled.connect(self.togglePanel)
        return dock

    # ---------- insights panel: foundations, move history, data structures ----------

    def buildInsightsPanel(self):
        self.insightsPanel = QFrame()
        self.insightsPanel.setObjectName("insightsPanel")
        self.insightsPanel.setFixedWidth(310)

        box = QVBoxLayout(self.insightsPanel)
        box.setContentsMargins(20, 18, 20, 18)
        box.setSpacing(10)

        box.addWidget(self.makeLabel("GAME INSIGHTS", "sectionLabel"))
        box.addWidget(self.makeLabel("Live data structures", "panelHeading"))

        box.addSpacing(4)
        box.addLayout(self.buildFoundationSection())
        box.addSpacing(4)
        box.addWidget(self.makeDivider())
        box.addSpacing(4)
        box.addLayout(self.buildHistorySection())
        box.addSpacing(4)
        box.addWidget(self.makeDivider())
        box.addSpacing(4)
        box.addLayout(self.buildStructureSection())
        box.addStretch()
        return self.insightsPanel

    def buildFoundationSection(self):
        """One progress bar per suit (foundations dictionary -> Stack sizes)."""
        section = QVBoxLayout()
        section.setSpacing(6)

        header = QHBoxLayout()
        header.addWidget(self.makeLabel("FOUNDATIONS", "sectionLabel"))
        header.addStretch()
        self.homeLabel = self.makeLabel("0 / 52", "rowValue")
        header.addWidget(self.homeLabel)
        section.addLayout(header)

        for suit in SUITS:
            row = QHBoxLayout()
            row.setSpacing(10)
            if suit in RED_SUITS:
                symbol = self.makeLabel(SUIT_SYMBOLS[suit], "suitRed")
            else:
                symbol = self.makeLabel(SUIT_SYMBOLS[suit], "suitBlack")
            symbol.setFixedWidth(18)

            bar = QProgressBar()
            bar.setRange(0, 13)
            bar.setTextVisible(False)
            count = self.makeLabel("0/13", "smallMuted")
            count.setFixedWidth(38)
            count.setAlignment(Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter)

            row.addWidget(symbol)
            row.addWidget(bar, 1)
            row.addWidget(count)
            section.addLayout(row)

            self.suitBars[suit] = bar
            self.suitCounts[suit] = count
        return section

    def buildHistorySection(self):
        """The newest moves, read from the undo Stack (top of the stack first)."""
        section = QVBoxLayout()
        section.setSpacing(6)

        header = QHBoxLayout()
        header.addWidget(self.makeLabel("MOVE HISTORY", "sectionLabel"))
        header.addStretch()
        self.historyCount = self.makeLabel("", "smallMuted")
        header.addWidget(self.historyCount)
        section.addLayout(header)

        self.historyBox = QVBoxLayout()
        self.historyBox.setSpacing(5)
        section.addLayout(self.historyBox)
        return section

    def buildStructureSection(self):
        """A small table: each data structure, what it is used for, and its size now."""
        section = QVBoxLayout()
        section.setSpacing(8)
        section.addWidget(self.makeLabel("DATA STRUCTURES", "sectionLabel"))

        grid = QGridLayout()
        grid.setHorizontalSpacing(10)
        grid.setVerticalSpacing(7)

        rows = [
            ("Stock", "Queue (FIFO)"),
            ("Waste", "Stack (LIFO)"),
            ("Tableau", "7 Linked lists"),
            ("Foundations", "4 Stacks"),
            ("Card locations", "Dictionary"),
            ("Undo / Redo", "2 Stacks"),
        ]
        for i in range(len(rows)):
            nameBox = QVBoxLayout()
            nameBox.setSpacing(0)
            nameBox.addWidget(self.makeLabel(rows[i][0], "dsName"))
            nameBox.addWidget(self.makeLabel(rows[i][1], "dsType"))

            value = self.makeLabel("-", "dsValue")
            value.setAlignment(Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter)

            grid.addLayout(nameBox, i, 0)
            grid.addWidget(value, i, 1)
            self.dsValues[rows[i][0]] = value
        grid.setColumnStretch(0, 1)
        section.addLayout(grid)
        return section

    # =====================================================================
    # UPDATING THE SCREEN
    # =====================================================================

    def formatTime(self):
        minutes = self.secondsPlayed // 60
        seconds = self.secondsPlayed % 60
        return f"{minutes:02d}:{seconds:02d}"

    def tick(self):
        """Called every second by the QTimer."""
        self.secondsPlayed += 1
        self.statLabels["Time"].setText(self.formatTime())

    def refresh(self):
        """Redraw the board and every number after anything changes."""
        self.board.update()        # tells Qt to call board.paintEvent() again
        self.updateTopBar()
        self.updateInsights()
        self.undoButton.setEnabled(not self.logic.history.isEmpty())
        self.redoButton.setEnabled(not self.logic.redoHistory.isEmpty())

    def updateTopBar(self):
        state = self.logic.state
        self.statLabels["Time"].setText(self.formatTime())
        self.statLabels["Moves"].setText(str(state.moveCount))
        self.statLabels["Score"].setText(str(state.score))
        self.statLabels["Hidden"].setText(str(state.countTableauCards(False)))
        self.subtitle.setText(str(state.countTableauCards(True)) + " cards visible  ·  " +
                              str(state.countOnFoundations()) + " cards home")

    def updateInsights(self):
        state = self.logic.state

        # Foundations: one Stack per suit, found through the dictionary.
        for suit in SUITS:
            size = state.foundations[suit].size()
            self.suitBars[suit].setValue(size)
            self.suitCounts[suit].setText(str(size) + "/13")
        self.homeLabel.setText(str(state.countOnFoundations()) + " / 52")

        self.updateHistory()

        # Data structure sizes
        waste = state.waste.peek()
        if waste is None:
            wasteText = "empty"
        else:
            wasteText = "top " + str(waste)

        nodes = 0
        for column in state.tableau:
            nodes += state.tableau[column].size()

        self.dsValues["Stock"].setText(str(state.stock.size()) + " cards")
        self.dsValues["Waste"].setText(wasteText)
        self.dsValues["Tableau"].setText(str(nodes) + " nodes")
        self.dsValues["Foundations"].setText(str(state.countOnFoundations()) + " cards")
        self.dsValues["Card locations"].setText(str(len(state.cardLocations)) + " keys")
        self.dsValues["Undo / Redo"].setText(str(self.logic.history.size()) + " / " +
                                             str(self.logic.redoHistory.size()))

    def updateHistory(self):
        """Show the newest moves from the undo Stack. The top of the stack is highlighted."""
        while self.historyBox.count() > 0:          # remove the old rows
            item = self.historyBox.takeAt(0)
            item.widget().deleteLater()

        moves = self.logic.history.toList()          # bottom ... top
        self.historyCount.setText("undo stack: " + str(len(moves)))

        if len(moves) == 0:
            self.historyBox.addWidget(self.makeLabel("No moves yet.", "emptyText"))
            return

        shown = 0
        index = len(moves) - 1                       # start at the TOP of the stack
        while index >= 0 and shown < HISTORY_ROWS:
            self.historyBox.addWidget(self.makeHistoryRow(moves[index], shown == 0))
            index -= 1
            shown += 1

    def makeHistoryRow(self, move, isTop):
        row = QFrame()
        if isTop:
            row.setObjectName("historyTopRow")       # gold: this is what Undo will reverse
        else:
            row.setObjectName("historyRow")
        line = QHBoxLayout(row)
        line.setContentsMargins(10, 5, 10, 5)

        line.addWidget(self.makeLabel(self.describeMove(move), "historyText"), 1)
        points = move["points"]
        if points > 0:
            line.addWidget(self.makeLabel("+" + str(points), "historyPoints"))
        elif points < 0:
            line.addWidget(self.makeLabel(str(points), "historyPoints"))
        return row

    def describeMove(self, move):
        """Turn a move dictionary into a short sentence."""
        moveType = move["type"]
        if moveType == "draw":
            if move["count"] == 1:
                return "Drew 1 card"
            return "Drew " + str(move["count"]) + " cards"
        if moveType == "recycle":
            return "Recycled the waste"
        if moveType == "wasteToTableau":
            return move["card"] + "   waste → column " + str(move["to"])
        if moveType == "wasteToFoundation":
            return move["card"] + "   waste → foundation"
        if moveType == "tableauToFoundation":
            return move["card"] + "   column " + str(move["from"]) + " → foundation"
        if moveType == "tableauToTableau":
            text = move["card"]
            if move["count"] > 1:
                text += " +" + str(move["count"] - 1)
            return text + "   column " + str(move["from"]) + " → " + str(move["to"])
        if moveType == "foundationToTableau":
            return move["card"] + "   foundation → column " + str(move["to"])
        return moveType

    def showMessage(self, text, kind="info"):
        """Show a message in the dock. kind picks the dot colour (see styles.DOT_COLORS)."""
        color = styles.DOT_COLORS[kind]
        self.statusDot.setStyleSheet("background: " + color + "; border-radius: 5px;")
        self.statusText.setText(text)

    # =====================================================================
    # REACTING TO THE BOARD AND THE BUTTONS
    # =====================================================================

    def onBoardChanged(self):
        """Called by the board's 'changed' signal after every successful move."""
        self.showMessage(DEFAULT_TIP, "info")
        self.refresh()
        self.checkForWin()

    def checkForWin(self):
        if self.gameOver or not self.logic.isWon():
            return
        self.gameOver = True
        self.timer.stop()
        self.showMessage("You won! All 52 cards are on the foundations.", "win")
        self.refresh()
        QMessageBox.information(
            self, "You won!",
            "Congratulations! All 52 cards are on the foundations.\n\n"
            "Score: " + str(self.logic.state.score) + "\n"
            "Moves: " + str(self.logic.state.moveCount) + "\n"
            "Time: " + self.formatTime())

    def startNewGame(self):
        self.logic.newGame()
        self.board.selected = None
        self.board.hintTarget = None
        self.gameOver = False
        self.secondsPlayed = 0
        self.timer.start(1000)
        self.showMessage("New game dealt. " + DEFAULT_TIP, "info")
        self.refresh()

    def undoMove(self):
        """Undo button: pop the last move from the history stack."""
        self.board.selected = None
        self.board.hintTarget = None
        if self.logic.undo():
            if self.gameOver:                  # undoing the winning move
                self.gameOver = False
                self.timer.start(1000)
            self.showMessage("Move undone.", "info")
        else:
            self.showMessage("Nothing to undo.", "error")
        self.refresh()

    def redoMove(self):
        """Redo button: pop the last undone move from the redo stack and do it again."""
        self.board.selected = None
        self.board.hintTarget = None
        if self.logic.redo():
            self.showMessage("Move redone.", "info")
            self.refresh()
            self.checkForWin()                 # redoing the winning move wins again
        else:
            self.showMessage("Nothing to redo.", "error")
            self.refresh()

    def showHint(self):
        """Hint button: highlight the best move on the board."""
        if self.gameOver:
            return
        hint = self.logic.findHint()
        self.board.showHint(hint)
        self.showMessage(hint["text"], "hint")

    def togglePanel(self, visible):
        self.insightsPanel.setVisible(visible)

    # =====================================================================
    # MENU
    # =====================================================================

    def openMenu(self):
        """Pause the game and show the menu (with a "Resume game" button)."""
        self.timer.stop()
        self.menu.setGameRunning(True, self.logic.drawCount)
        self.pages.setCurrentWidget(self.menu)

    def resumeGame(self):
        """Go back to the game exactly as it was."""
        self.pages.setCurrentWidget(self.gamePage)
        if not self.gameOver:
            self.timer.start(1000)

    def startFromMenu(self, drawCount):
        """"Start game" / "New game" in the menu: deal with the chosen draw count."""
        self.logic.drawCount = drawCount
        self.drawOneButton.setChecked(drawCount == 1)       # keep the top bar switch in sync
        self.drawThreeButton.setChecked(drawCount == 3)
        self.startNewGame()
        self.pages.setCurrentWidget(self.gamePage)

    # =====================================================================
    # DRAW MODE
    # =====================================================================

    def chooseDrawOne(self):
        self.changeDrawMode(1)

    def chooseDrawThree(self):
        self.changeDrawMode(3)

    def changeDrawMode(self, newCount):
        """Switching between draw 1 and draw 3 deals a new game (to keep it fair)."""
        if newCount == self.logic.drawCount:
            return

        if self.logic.state.moveCount > 0 and not self.gameOver:
            answer = QMessageBox.question(
                self, "Change mode",
                "Switch to Draw " + str(newCount) + "? This starts a new game.")
            if answer != QMessageBox.StandardButton.Yes:
                # Put the switch back the way it was.
                self.drawOneButton.setChecked(self.logic.drawCount == 1)
                self.drawThreeButton.setChecked(self.logic.drawCount == 3)
                return

        self.logic.drawCount = newCount
        self.startNewGame()