from PyQt6.QtCore import Qt, QRectF, QPointF, pyqtSignal
from PyQt6.QtGui import QPainter, QColor, QFont, QPen, QLinearGradient
from PyQt6.QtWidgets import QWidget

from Models.card import SUITS, SUIT_SYMBOLS
from UI import styles
from UI import card_painter


class GameBoard(QWidget):
    """Draws the piles of a GameLogic and turns mouse clicks into moves."""

    # Signals: messages the board sends to the main window.
    changed = pyqtSignal()              # "a move was made, refresh everything"
    message = pyqtSignal(str, str)      # (text, kind) kind = "info", "error", ...

    def __init__(self, logic):
        super().__init__()
        self.logic = logic          # GameLogic object (holds the GameState)
        self.selected = None        # the selected place (dictionary) or None
        self.hintTarget = None      # where the hinted card should go (dictionary) or None

        # Sizes, recalculated by computeLayout() whenever the widget changes size.
        self.cardWidth = styles.MAX_CARD_WIDTH
        self.cardHeight = self.cardWidth * styles.CARD_RATIO
        self.columnGap = 20
        self.boardLeft = 0

        self.setMinimumSize(600, 400)

    # =====================================================================
    # LAYOUT (sizes and positions)
    # =====================================================================

    def computeLayout(self):
        """Choose a card size that fits the widget's width AND height."""
        pad = styles.PANEL_PADDING

        # 7 cards + 6 gaps must fit inside the panel width.
        byWidth = (self.width() - 2 * pad) / (7 + 6 * styles.COLUMN_GAP_RATIO)

        # Roughly 3.3 card heights must fit vertically (top row + a tableau column).
        fixedSpace = 4 * pad + styles.LABEL_HEIGHT + styles.NOTE_HEIGHT + styles.PANEL_GAP
        byHeight = (self.height() - fixedSpace) / 3.3 / styles.CARD_RATIO

        width = min(styles.MAX_CARD_WIDTH, byWidth, byHeight)
        width = max(styles.MIN_CARD_WIDTH, width)

        self.cardWidth = width
        self.cardHeight = width * styles.CARD_RATIO
        self.columnGap = width * styles.COLUMN_GAP_RATIO

        boardWidth = 7 * self.cardWidth + 6 * self.columnGap
        self.boardLeft = (self.width() - boardWidth) / 2      # centre the columns

    def resizeEvent(self, event):
        """Qt calls this when the widget changes size."""
        self.computeLayout()
        super().resizeEvent(event)

    def columnX(self, column):
        """Left edge of column 1..7."""
        return self.boardLeft + (column - 1) * (self.cardWidth + self.columnGap)

    def cardRect(self, x, y):
        return QRectF(x, y, self.cardWidth, self.cardHeight)

    def topRowY(self):
        return styles.PANEL_PADDING + styles.LABEL_HEIGHT

    def topPanelRect(self):
        height = self.topRowY() + self.cardHeight + styles.NOTE_HEIGHT + styles.PANEL_PADDING / 2
        return QRectF(0, 0, self.width(), height)

    def tableauPanelRect(self):
        top = self.topPanelRect().bottom() + styles.PANEL_GAP
        return QRectF(0, top, self.width(), self.height() - top)

    def stockRect(self):
        return self.cardRect(self.columnX(1), self.topRowY())

    def wasteRect(self):
        return self.cardRect(self.columnX(2), self.topRowY())

    def wasteVisibleCount(self):
        """How many waste cards are shown: 1 in draw-1 mode, up to 3 in draw-3 mode."""
        if self.logic.drawCount == 3:
            return min(3, self.logic.state.waste.size())
        return min(1, self.logic.state.waste.size())

    def wasteFanOffset(self):
        return self.cardWidth * styles.WASTE_FAN_RATIO

    def wasteTopRect(self):
        """Where the TOP waste card is drawn (the only one you can click)."""
        shift = max(self.wasteVisibleCount() - 1, 0) * self.wasteFanOffset()
        return self.wasteRect().translated(shift, 0)

    def foundationRect(self, suit):
        """Foundations sit above columns 4, 5, 6, 7 in the order of SUITS."""
        index = SUITS.index(suit)
        return self.cardRect(self.columnX(4 + index), self.topRowY())

    def tableauTop(self):
        return self.tableauPanelRect().top() + styles.PANEL_PADDING

    def emptyColumnRect(self, column):
        return self.cardRect(self.columnX(column), self.tableauTop())

    def tableauCardRects(self, column):
        """
        Return a list with one QRectF per card in the column (bottom card first).
        Face-down cards overlap more than face-up cards.
        If a column is too tall for the panel, the face-up gap shrinks.
        """
        cards = self.logic.state.tableau[column].toList()
        if len(cards) == 0:
            return []

        faceDownCount = 0
        faceUpCount = 0
        for card in cards:
            if card.faceUp:
                faceUpCount += 1
            else:
                faceDownCount += 1

        faceDownGap = self.cardHeight * styles.FACE_DOWN_RATIO
        faceUpGap = self.cardHeight * styles.FACE_UP_RATIO

        bottom = self.tableauPanelRect().bottom() - styles.PANEL_PADDING
        spaceLeft = bottom - self.tableauTop() - self.cardHeight - faceDownCount * faceDownGap
        if faceUpCount > 1 and (faceUpCount - 1) * faceUpGap > spaceLeft:
            faceUpGap = max(self.cardHeight * 0.09, spaceLeft / (faceUpCount - 1))

        rects = []
        y = self.tableauTop()
        for card in cards:
            rects.append(self.cardRect(self.columnX(column), y))
            if card.faceUp:
                y += faceUpGap
            else:
                y += faceDownGap
        return rects

    def placeRect(self, place):
        """The rectangle of a place (used to draw the hint target outline)."""
        if place["pile"] == "foundation":
            return self.foundationRect(place["key"])
        if place["pile"] == "stock":
            return self.stockRect()
        rects = self.tableauCardRects(place["key"])
        if len(rects) == 0:
            return self.emptyColumnRect(place["key"])
        return rects[-1]

    # =====================================================================
    # FINDING WHAT WAS CLICKED
    # =====================================================================

    def findClicked(self, x, y):
        """Return the place (dictionary) under the mouse, or None."""
        point = QPointF(x, y)
        state = self.logic.state

        if self.stockRect().contains(point):
            return {"pile": "stock", "key": None, "index": None}

        if not state.waste.isEmpty() and self.wasteTopRect().contains(point):
            return {"pile": "waste", "key": None, "index": None}

        for suit in SUITS:
            if self.foundationRect(suit).contains(point):
                return {"pile": "foundation", "key": suit, "index": None}

        for column in range(1, 8):
            rects = self.tableauCardRects(column)
            if len(rects) == 0:
                if self.emptyColumnRect(column).contains(point):
                    return {"pile": "tableau", "key": column, "index": None}

            # Check from the TOP card down: the top card covers the cards under it.
            for i in range(len(rects) - 1, -1, -1):
                if rects[i].contains(point):
                    return {"pile": "tableau", "key": column, "index": i}
        return None

    def selectedCard(self):
        """Return the Card object that is currently selected."""
        place = self.selected
        if place["pile"] == "waste":
            return self.logic.state.waste.peek()
        if place["pile"] == "foundation":
            return self.logic.state.foundations[place["key"]].peek()
        return self.logic.state.tableau[place["key"]].get(place["index"])

    # =====================================================================
    # MOUSE
    # =====================================================================

    def mousePressEvent(self, event):
        if event.button() != Qt.MouseButton.LeftButton:
            return
        self.hintTarget = None
        clicked = self.findClicked(event.position().x(), event.position().y())

        if clicked is None:                       # clicked on the green felt
            self.clearSelection()
            return

        if clicked["pile"] == "stock":
            self.selected = None
            if self.logic.drawFromStock():
                self.afterMove()
            else:
                self.message.emit("The stock and the waste are both empty.", "info")
                self.update()
            return

        if self.selected is None:                 # first click: select
            if not self.trySelect(clicked):
                self.message.emit("Only face-up cards can be picked up.", "error")
            return

        if clicked == self.selected:              # same card again: unselect
            self.clearSelection()
            return

        if self.moveSelectedTo(clicked):          # second click: move
            self.afterMove()
            return

        # The move was illegal. Select the clicked card instead, if possible.
        self.selected = None
        self.trySelect(clicked)
        self.message.emit("That move isn't allowed.", "error")
        self.update()

    def mouseDoubleClickEvent(self, event):
        """Double-click: send the waste or tableau top card to its foundation."""
        clicked = self.findClicked(event.position().x(), event.position().y())
        if clicked is None:
            return

        moved = False
        if clicked["pile"] == "waste":
            moved = self.logic.moveWasteToFoundation()
        elif clicked["pile"] == "tableau" and clicked["index"] is not None:
            topIndex = self.logic.state.tableau[clicked["key"]].size() - 1
            if clicked["index"] == topIndex:
                moved = self.logic.moveTableauToFoundation(clicked["key"])

        if moved:
            self.afterMove()

    # =====================================================================
    # SELECTING AND MOVING
    # =====================================================================

    def trySelect(self, place):
        """Select a place if it holds a card the player may pick up."""
        state = self.logic.state
        allowed = False

        if place["pile"] == "waste":
            allowed = not state.waste.isEmpty()
        elif place["pile"] == "foundation":
            allowed = not state.foundations[place["key"]].isEmpty()
        elif place["pile"] == "tableau" and place["index"] is not None:
            allowed = self.logic.canPickUp(place["key"], place["index"])

        if allowed:
            self.selected = place
            self.update()
        return allowed

    def moveSelectedTo(self, target):
        """Ask GameLogic to move the selected card(s) to the target. True if moved."""
        source = self.selected
        logic = self.logic

        if target["pile"] == "tableau":
            column = target["key"]
            if source["pile"] == "waste":
                return logic.moveWasteToTableau(column)
            if source["pile"] == "tableau":
                return logic.moveTableauToTableau(source["key"], source["index"], column)
            if source["pile"] == "foundation":
                return logic.moveFoundationToTableau(source["key"], column)

        if target["pile"] == "foundation":
            card = self.selectedCard()
            if card.suit != target["key"]:        # each foundation belongs to one suit
                return False
            if source["pile"] == "waste":
                return logic.moveWasteToFoundation()
            if source["pile"] == "tableau":
                topIndex = logic.state.tableau[source["key"]].size() - 1
                if source["index"] != topIndex:   # only the top card can go up
                    return False
                return logic.moveTableauToFoundation(source["key"])

        return False

    def clearSelection(self):
        self.selected = None
        self.hintTarget = None
        self.update()

    def afterMove(self):
        """Called after every successful move."""
        self.selected = None
        self.hintTarget = None
        self.update()               # redraw the board
        self.changed.emit()         # tell the main window to refresh

    def showHint(self, hint):
        """Highlight a hint: gold outline on the card, dashed outline on the target."""
        self.selected = None
        self.hintTarget = None
        if hint["pile"] == "waste" or hint["pile"] == "tableau":
            self.selected = {"pile": hint["pile"], "key": hint["key"], "index": hint["index"]}
            self.hintTarget = hint["target"]
        elif hint["pile"] == "stock":
            self.hintTarget = {"pile": "stock", "key": None}
        self.update()

    # =====================================================================
    # DRAWING
    # =====================================================================

    def paintEvent(self, event):
        """Qt calls this automatically whenever the board must be redrawn."""
        self.computeLayout()
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        painter.setRenderHint(QPainter.RenderHint.TextAntialiasing)

        self.drawPanel(painter, self.topPanelRect())
        self.drawPanel(painter, self.tableauPanelRect())
        self.drawTopLabels(painter)

        self.drawStock(painter)
        self.drawWaste(painter)
        self.drawFoundations(painter)
        self.drawTableau(painter)
        self.drawHintTarget(painter)

        painter.end()

    def drawPanel(self, painter, rect):
        """A rounded green felt panel with a soft vertical gradient."""
        gradient = QLinearGradient(rect.topLeft(), rect.bottomLeft())
        gradient.setColorAt(0, QColor(styles.FELT_LIGHT))
        gradient.setColorAt(1, QColor(styles.FELT_DARK))
        painter.setPen(QPen(QColor(styles.FELT_BORDER), 1))
        painter.setBrush(gradient)
        painter.drawRoundedRect(rect.adjusted(0.5, 0.5, -0.5, -0.5), 14, 14)

    def drawText(self, painter, x, y, text, color, bold=False, centerWidth=None):
        """Write a small label. If centerWidth is given, centre it in that width."""
        font = QFont(styles.UI_FONT, 9)
        font.setBold(bold)
        if bold:
            font.setLetterSpacing(QFont.SpacingType.AbsoluteSpacing, 1)
        painter.setFont(font)
        painter.setPen(QColor(color))
        if centerWidth is None:
            painter.drawText(QPointF(x, y), text)
        else:
            box = QRectF(x, y - 14, centerWidth, 20)
            painter.drawText(box, Qt.AlignmentFlag.AlignCenter, text)

    def drawTopLabels(self, painter):
        """Headings above the top row and small notes under it."""
        state = self.logic.state
        labelY = styles.PANEL_PADDING + 12
        noteY = self.topRowY() + self.cardHeight + 18

        self.drawText(painter, self.columnX(1), labelY, "STOCK", styles.PANEL_LABEL, True)
        self.drawText(painter, self.columnX(2), labelY, "WASTE", styles.PANEL_LABEL, True)
        self.drawText(painter, self.columnX(4), labelY, "FOUNDATIONS", styles.PANEL_LABEL, True)

        self.drawText(painter, self.columnX(1), noteY,
                      str(state.stock.size()) + " cards", styles.PANEL_NOTE)
        self.drawText(painter, self.columnX(2), noteY,
                      str(state.waste.size()) + " in waste", styles.PANEL_NOTE)

        for suit in SUITS:
            rect = self.foundationRect(suit)
            count = state.foundations[suit].size()            # dictionary -> Stack
            self.drawText(painter, rect.left(), noteY, str(count) + " / 13",
                          styles.PANEL_NOTE, centerWidth=rect.width())

    def isSelected(self, pile, key):
        return (self.selected is not None and self.selected["pile"] == pile
                and self.selected["key"] == key)

    def drawCard(self, painter, rect, card):
        if card.faceUp:
            card_painter.drawCardFace(painter, rect, card)
        else:
            card_painter.drawCardBack(painter, rect)

    def drawStock(self, painter):
        rect = self.stockRect()
        stock = self.logic.state.stock

        if stock.isEmpty():
            card_painter.drawEmptySlot(painter, rect, "↻")   # click to recycle
            return

        if stock.size() > 1:                                 # small "pile" edge
            card_painter.drawCardBack(painter, rect.translated(3, 3))
        card_painter.drawCardBack(painter, rect)

    def drawWaste(self, painter):
        rect = self.wasteRect()
        cards = self.logic.state.waste.toList()

        if len(cards) == 0:
            card_painter.drawEmptySlot(painter, rect)
            return

        # Draw-1 shows only the top card. Draw-3 fans out the top three.
        visible = cards[-self.wasteVisibleCount():]
        for i in range(len(visible)):
            cardRect = rect.translated(i * self.wasteFanOffset(), 0)
            self.drawCard(painter, cardRect, visible[i])

        if self.isSelected("waste", None):
            card_painter.drawSelection(painter, self.wasteTopRect())

    def drawFoundations(self, painter):
        for suit in SUITS:
            rect = self.foundationRect(suit)
            foundation = self.logic.state.foundations[suit]   # dictionary lookup
            if foundation.isEmpty():
                card_painter.drawEmptySlot(painter, rect, SUIT_SYMBOLS[suit])
            else:
                self.drawCard(painter, rect, foundation.peek())
                if self.isSelected("foundation", suit):
                    card_painter.drawSelection(painter, rect)

    def drawTableau(self, painter):
        for column in range(1, 8):
            cards = self.logic.state.tableau[column].toList()
            rects = self.tableauCardRects(column)

            if len(cards) == 0:
                card_painter.drawEmptySlot(painter, self.emptyColumnRect(column), "K")
                continue

            for i in range(len(cards)):
                self.drawCard(painter, rects[i], cards[i])

            # One gold outline around the whole selected group.
            if self.isSelected("tableau", column):
                first = rects[self.selected["index"]]
                last = rects[-1]
                groupRect = QRectF(first.left(), first.top(), first.width(),
                                   last.bottom() - first.top())
                card_painter.drawSelection(painter, groupRect)

    def drawHintTarget(self, painter):
        """Dashed blue outline where the hinted card should go."""
        if self.hintTarget is None:
            return
        rect = self.placeRect(self.hintTarget).adjusted(-4, -4, 4, 4)
        pen = QPen(QColor(styles.HINT_TARGET), 2.5, Qt.PenStyle.DashLine)
        painter.setPen(pen)
        painter.setBrush(Qt.BrushStyle.NoBrush)
        painter.drawRoundedRect(rect, styles.CARD_RADIUS + 3, styles.CARD_RADIUS + 3)