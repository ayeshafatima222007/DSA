"""
card_painter.py
---------------
Functions that DRAW cards with QPainter. No images are used.

    drawCardFace(painter, rect, card)   -> a face-up card
    drawCardBack(painter, rect)         -> red patterned back
    drawEmptySlot(painter, rect, text)  -> outline of an empty pile
    drawSelection(painter, rect)        -> gold outline for a selected card

'rect' is a QRectF that says WHERE on the screen to draw and how big.
"""

from PyQt6.QtCore import Qt, QRectF, QPointF
from PyQt6.QtGui import QColor, QFont, QPen, QPainterPath, QPolygonF

from UI import styles


# Where the suit symbols (pips) go on number cards.
# Dictionary: rank -> list of (x, y) positions, 0.0 = left/top, 1.0 = right/bottom.
LEFT = 0.32
MIDDLE = 0.50
RIGHT = 0.68

PIP_POSITIONS = {
    2:  [(MIDDLE, 0.0), (MIDDLE, 1.0)],
    3:  [(MIDDLE, 0.0), (MIDDLE, 0.5), (MIDDLE, 1.0)],
    4:  [(LEFT, 0.0), (RIGHT, 0.0), (LEFT, 1.0), (RIGHT, 1.0)],
    5:  [(LEFT, 0.0), (RIGHT, 0.0), (MIDDLE, 0.5), (LEFT, 1.0), (RIGHT, 1.0)],
    6:  [(LEFT, 0.0), (RIGHT, 0.0), (LEFT, 0.5), (RIGHT, 0.5), (LEFT, 1.0), (RIGHT, 1.0)],
    7:  [(LEFT, 0.0), (RIGHT, 0.0), (MIDDLE, 0.25), (LEFT, 0.5), (RIGHT, 0.5),
         (LEFT, 1.0), (RIGHT, 1.0)],
    8:  [(LEFT, 0.0), (RIGHT, 0.0), (MIDDLE, 0.25), (LEFT, 0.5), (RIGHT, 0.5),
         (MIDDLE, 0.75), (LEFT, 1.0), (RIGHT, 1.0)],
    9:  [(LEFT, 0.0), (RIGHT, 0.0), (LEFT, 0.333), (RIGHT, 0.333), (MIDDLE, 0.5),
         (LEFT, 0.667), (RIGHT, 0.667), (LEFT, 1.0), (RIGHT, 1.0)],
    10: [(LEFT, 0.0), (RIGHT, 0.0), (MIDDLE, 0.167), (LEFT, 0.333), (RIGHT, 0.333),
         (LEFT, 0.667), (RIGHT, 0.667), (MIDDLE, 0.833), (LEFT, 1.0), (RIGHT, 1.0)],
}


def suitColor(card):
    if card.isRed():
        return QColor(styles.RED_SUIT)
    return QColor(styles.BLACK_SUIT)


def drawCenteredText(painter, centerX, centerY, text, upsideDown=False):
    """Draw text centred on a point. If upsideDown, rotate it 180 degrees."""
    box = QRectF(-60, -60, 120, 120)
    painter.save()
    painter.translate(centerX, centerY)
    if upsideDown:
        painter.rotate(180)
    painter.drawText(box, Qt.AlignmentFlag.AlignCenter, text)
    painter.restore()


def drawRoundedCard(painter, rect, fillColor, borderColor):
    """The white (or red) rounded rectangle that every card starts with."""
    painter.setPen(QPen(QColor(borderColor), 1))
    painter.setBrush(QColor(fillColor))
    painter.drawRoundedRect(rect, styles.CARD_RADIUS, styles.CARD_RADIUS)


# =====================================================================
# FACE-UP CARD
# =====================================================================

def drawCardFace(painter, rect, card):
    """Draw a face-up card: corners + pips (or a big letter for J, Q, K)."""
    drawRoundedCard(painter, rect, styles.CARD_FACE, styles.CARD_BORDER)
    painter.setPen(suitColor(card))

    drawCorner(painter, rect, card, upsideDown=False)
    drawCorner(painter, rect, card, upsideDown=True)

    if card.rank == 1:
        drawAce(painter, rect, card)
    elif card.rank >= 11:
        drawFaceCard(painter, rect, card)
    else:
        drawPips(painter, rect, card)


def drawCorner(painter, rect, card, upsideDown):
    """Rank and small suit in the top-left (or bottom-right, upside down)."""
    rankFont = QFont(styles.CARD_FONT, int(rect.height() * 0.13))
    rankFont.setBold(True)
    suitFont = QFont(styles.SYMBOL_FONT, int(rect.height() * 0.085))

    x = rect.left() + rect.width() * 0.13
    y = rect.top() + rect.height() * 0.11
    if upsideDown:
        x = rect.right() - rect.width() * 0.13
        y = rect.bottom() - rect.height() * 0.11

    painter.setFont(rankFont)
    drawCenteredText(painter, x, y, card.rankName(), upsideDown)

    suitY = y + rect.height() * 0.12
    if upsideDown:
        suitY = y - rect.height() * 0.12
    painter.setFont(suitFont)
    drawCenteredText(painter, x, suitY, card.symbol(), upsideDown)


def drawPips(painter, rect, card):
    """Draw the suit symbols for cards 2 to 10 using PIP_POSITIONS."""
    painter.setFont(QFont(styles.SYMBOL_FONT, int(rect.height() * 0.115)))
    top = rect.top() + rect.height() * 0.19
    usableHeight = rect.height() * 0.62

    for position in PIP_POSITIONS[card.rank]:
        x = rect.left() + rect.width() * position[0]
        y = top + usableHeight * position[1]
        upsideDown = position[1] > 0.5        # bottom half pips point down
        drawCenteredText(painter, x, y, card.symbol(), upsideDown)


def drawAce(painter, rect, card):
    """One large suit symbol in the middle."""
    painter.setFont(QFont(styles.SYMBOL_FONT, int(rect.height() * 0.30)))
    drawCenteredText(painter, rect.center().x(), rect.center().y(), card.symbol())


def drawFaceCard(painter, rect, card):
    """J, Q, K: a coloured frame with a big letter and suit (no artwork)."""
    inner = rect.adjusted(rect.width() * 0.22, rect.height() * 0.17,
                          -rect.width() * 0.22, -rect.height() * 0.17)
    fill = styles.FACE_CARD_FILL_BLACK
    if card.isRed():
        fill = styles.FACE_CARD_FILL_RED

    painter.setPen(QPen(suitColor(card), 1.5))
    painter.setBrush(QColor(fill))
    painter.drawRect(inner)

    letterFont = QFont(styles.CARD_FONT, int(rect.height() * 0.24))
    letterFont.setBold(True)
    painter.setFont(letterFont)
    drawCenteredText(painter, inner.center().x(), inner.center().y() - inner.height() * 0.12,
                     card.rankName())

    painter.setFont(QFont(styles.SYMBOL_FONT, int(rect.height() * 0.14)))
    drawCenteredText(painter, inner.center().x(), inner.center().y() + inner.height() * 0.25,
                     card.symbol())


# =====================================================================
# CARD BACK
# =====================================================================

def drawCardBack(painter, rect):
    """White border, red inside with a diamond lattice, and a white diamond in the centre."""
    drawRoundedCard(painter, rect, styles.CARD_FACE, styles.CARD_BORDER)

    inner = rect.adjusted(5, 5, -5, -5)
    painter.setPen(Qt.PenStyle.NoPen)
    painter.setBrush(QColor(styles.CARD_BACK_RED))
    painter.drawRoundedRect(inner, 4, 4)

    # Lattice: two sets of diagonal lines, clipped to the red area.
    painter.save()
    clip = QPainterPath()
    clip.addRoundedRect(inner, 4, 4)
    painter.setClipPath(clip)
    painter.setPen(QPen(QColor(styles.CARD_BACK_PATTERN), 1))
    spacing = 9
    size = int(inner.width() + inner.height())
    for step in range(-size, size, spacing):
        x = inner.left() + step
        painter.drawLine(QPointF(x, inner.top()), QPointF(x + inner.height(), inner.bottom()))
        painter.drawLine(QPointF(x, inner.bottom()), QPointF(x + inner.height(), inner.top()))
    painter.restore()

    # Centre emblem: a white diamond with a red diamond inside.
    centerX = inner.center().x()
    centerY = inner.center().y()
    drawDiamond(painter, centerX, centerY, inner.width() * 0.36, inner.height() * 0.20,
                styles.CARD_FACE)
    drawDiamond(painter, centerX, centerY, inner.width() * 0.20, inner.height() * 0.11,
                styles.CARD_BACK_RED)


def drawDiamond(painter, centerX, centerY, halfWidth, halfHeight, color):
    shape = QPolygonF([
        QPointF(centerX, centerY - halfHeight),
        QPointF(centerX + halfWidth, centerY),
        QPointF(centerX, centerY + halfHeight),
        QPointF(centerX - halfWidth, centerY),
    ])
    painter.setPen(Qt.PenStyle.NoPen)
    painter.setBrush(QColor(color))
    painter.drawPolygon(shape)


# =====================================================================
# EMPTY PILES AND SELECTION
# =====================================================================

def drawEmptySlot(painter, rect, text=""):
    """A faint outline where a pile is empty, with an optional symbol inside."""
    fill = QColor(0, 0, 0, 45)
    painter.setPen(QPen(QColor(styles.SLOT_BORDER), 2))
    painter.setBrush(fill)
    painter.drawRoundedRect(rect, styles.CARD_RADIUS, styles.CARD_RADIUS)

    if text != "":
        painter.setPen(QColor(styles.SLOT_SYMBOL))
        painter.setFont(QFont(styles.SYMBOL_FONT, int(rect.height() * 0.28)))
        drawCenteredText(painter, rect.center().x(), rect.center().y(), text)


def drawSelection(painter, rect):
    """Gold outline around a selected card."""
    painter.setPen(QPen(QColor(styles.SELECTED_BORDER), 3))
    painter.setBrush(Qt.BrushStyle.NoBrush)
    painter.drawRoundedRect(rect.adjusted(-1, -1, 1, 1), styles.CARD_RADIUS, styles.CARD_RADIUS)