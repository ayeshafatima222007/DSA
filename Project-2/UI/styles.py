"""
styles.py
---------
All sizes and colours of the interface in ONE place.
To change how the game looks, change the values here.

Colour theme: "Midnight & Gold"
    deep navy background, blue felt table, gold buttons and highlights.
"""

# ---------- Card sizes ----------
# Cards grow and shrink with the window, so these are LIMITS and RATIOS.
MAX_CARD_WIDTH = 112         # cards never get wider than this (pixels)
MIN_CARD_WIDTH = 52          # ...or narrower than this
CARD_RATIO = 1.4             # height = width x 1.4 (a real card's shape)
CARD_RADIUS = 8              # rounded corners

COLUMN_GAP_RATIO = 0.18      # space between columns = 18% of a card's width
FACE_DOWN_RATIO = 0.10       # visible part of a face-down card = 10% of card height
FACE_UP_RATIO = 0.22         # visible part of a face-up card = 22% of card height
WASTE_FAN_RATIO = 0.26       # sideways spread of the waste in draw-3 mode

PANEL_PADDING = 18           # space inside the felt panels
PANEL_GAP = 14               # space between the two felt panels
LABEL_HEIGHT = 24            # room for "STOCK", "WASTE", "FOUNDATIONS"
NOTE_HEIGHT = 24             # room for "20 cards", "3 / 13" under the top row

# ---------- Card colours ----------
CARD_FACE = "#ffffff"
CARD_BORDER = "#b9b9b9"
RED_SUIT = "#d4142a"
BLACK_SUIT = "#111111"
FACE_CARD_FILL_RED = "#fdecee"
FACE_CARD_FILL_BLACK = "#eef0f4"

CARD_BACK_RED = "#c8102e"
CARD_BACK_PATTERN = "#ec5a70"

SELECTED_BORDER = "#ffc83d"  # gold outline around selected cards
HINT_TARGET = "#7ef0c6"      # dashed mint outline where a hinted card should go

# ---------- Table colours (blue felt) ----------
FELT_LIGHT = "#1f5b97"
FELT_DARK = "#153f6c"
FELT_BORDER = "#2f6fb0"
SLOT_BORDER = "#4380bf"
SLOT_SYMBOL = "#5f95cf"
PANEL_LABEL = "#dce9f8"      # "STOCK", "WASTE", ...
PANEL_NOTE = "#a8c4e4"       # "20 cards", "3 / 13", ...

# ---------- Status dot colours (one per message kind) ----------
DOT_COLORS = {
    "info": "#4fb3ff",
    "hint": "#f5b83d",
    "error": "#ff6b6b",
    "win": "#f5b83d",
}

# ---------- Fonts ----------
CARD_FONT = "Georgia"
SYMBOL_FONT = "Segoe UI Symbol"
UI_FONT = "Segoe UI"

# ---------- Qt Style Sheet for the window (looks like CSS) ----------
WINDOW_STYLE = """
QWidget#central { background: #0b1220; }

QWidget { font-family: "Segoe UI"; color: #e7edf7; }

/* ---------- top bar ---------- */
QFrame#topBar { background: #121b2d; border: 1px solid #22304a; border-radius: 14px; }
QLabel#title  { font-size: 20px; font-weight: bold; color: #ffffff; }
QLabel#subtitle { font-size: 13px; color: #8a9bb8; }

QFrame#statPill { background: #1a2539; border: 1px solid #26354f; border-radius: 10px; }
QLabel#pillCaption { font-size: 10px; font-weight: bold; color: #8a9bb8; }
QLabel#pillValue   { font-size: 17px; font-weight: bold; color: #ffffff; }

/* ---------- buttons ---------- */
QPushButton {
    font-size: 14px;
    font-weight: 600;
    color: #e7edf7;
    background: #1a2539;
    border: 1px solid #2a3a57;
    border-radius: 9px;
    padding: 8px 16px;
}
QPushButton:hover    { background: #22304a; border-color: #36496b; }
QPushButton:pressed  { background: #141d2e; }
QPushButton:disabled { color: #4f5f7b; background: #131b2b; border-color: #1c2740; }

QPushButton#goldButton {
    color: #1b1404;
    background: #f5b83d;
    border: 1px solid #f5b83d;
}
QPushButton#goldButton:hover   { background: #ffc95c; }
QPushButton#goldButton:pressed { background: #d99a1e; }

QPushButton#segmentLeft, QPushButton#segmentRight {
    background: #121b2d;
    color: #8a9bb8;
    padding: 8px 14px;
}
QPushButton#segmentLeft  { border-top-right-radius: 0; border-bottom-right-radius: 0; }
QPushButton#segmentRight { border-top-left-radius: 0;  border-bottom-left-radius: 0; border-left: none; }
QPushButton#segmentLeft:checked, QPushButton#segmentRight:checked {
    background: #f5b83d; color: #1b1404; border-color: #f5b83d;
}

QPushButton#panelToggle:checked { background: #22304a; border-color: #4f6a96; color: #ffffff; }

/* ---------- control dock (under the board) ---------- */
QFrame#dock { background: #121b2d; border: 1px solid #22304a; border-radius: 14px; }
QLabel#statusText { font-size: 14px; color: #e7edf7; }

/* ---------- insights panel ---------- */
QFrame#insightsPanel { background: #121b2d; border: 1px solid #22304a; border-radius: 14px; }
QFrame#divider    { background: #22304a; max-height: 1px; min-height: 1px; border: none; }
QLabel#sectionLabel { font-size: 11px; font-weight: bold; color: #8a9bb8; }
QLabel#panelHeading { font-size: 18px; font-weight: bold; color: #ffffff; }
QLabel#smallMuted   { font-size: 12px; color: #8a9bb8; }
QLabel#suitRed      { font-size: 17px; color: #ff7a85; }
QLabel#suitBlack    { font-size: 17px; color: #e7edf7; }
QLabel#rowValue     { font-size: 13px; font-weight: 600; color: #e7edf7; }
QLabel#dsName       { font-size: 13px; color: #e7edf7; }
QLabel#dsType       { font-size: 11px; color: #8a9bb8; }
QLabel#dsValue      { font-size: 13px; font-weight: bold; color: #f5b83d; }

QFrame#historyRow    { background: #1a2539; border: 1px solid #22304a; border-radius: 8px; }
QFrame#historyTopRow { background: #2a2414; border: 1px solid #6b5420; border-radius: 8px; }
QLabel#historyText   { font-size: 12px; color: #e7edf7; }
QLabel#historyPoints { font-size: 12px; font-weight: bold; color: #f5b83d; }
QLabel#emptyText     { font-size: 13px; color: #6f809c; }

QProgressBar {
    background: #1f2b42;
    border: none;
    border-radius: 4px;
    max-height: 8px;
    min-height: 8px;
}
QProgressBar::chunk { background: #f5b83d; border-radius: 4px; }

/* ---------- start menu ---------- */
QWidget#menuPage {
    background: qradialgradient(cx:0.5, cy:0.45, radius:0.85, fx:0.5, fy:0.45,
                                stop:0 #1c3a66, stop:0.55 #0f1a2e, stop:1 #0b1220);
}
QFrame#menuPanel { background: #121b2d; border: 1px solid #26354f; border-radius: 20px; }
QFrame#menuSide  { background: #0f2340; border: none; border-radius: 16px; }
QLabel#menuTitle { font-size: 34px; font-weight: bold; color: #ffffff; }
QLabel#menuTag   { font-size: 12px; font-weight: bold; color: #f5b83d; }
QLabel#rulesText {
    font-size: 13px; color: #d4deec;
    background: #1a2539; border: 1px solid #26354f; border-radius: 10px; padding: 12px;
}
QPushButton#menuPrimary, QPushButton#menuButton { font-size: 16px; padding: 11px; border-radius: 10px; }
QPushButton#menuPrimary { color: #1b1404; background: #f5b83d; border: 1px solid #f5b83d; }
QPushButton#menuPrimary:hover   { background: #ffc95c; }
QPushButton#menuPrimary:pressed { background: #d99a1e; }
QPushButton#menuButton:checked  { background: #22304a; border-color: #36496b; }

/* ---------- pop-up windows ---------- */
QMessageBox { background: #121b2d; }
QMessageBox QLabel { color: #e7edf7; font-size: 14px; }
QToolTip { background: #1a2539; color: #e7edf7; border: 1px solid #2a3a57; padding: 4px; }
"""