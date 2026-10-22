import sys

#PyQt imports
from PyQt5.QtCore import Qt, QAbstractTableModel, QModelIndex, QThread, pyqtSignal
from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QGridLayout, QTableView,
    QPushButton, QLabel, QProgressBar, QSpinBox, QLineEdit, QMessageBox,
    QDialog, QFormLayout, QDialogButtonBox, QAbstractItemView, QComboBox,
    QTableWidget, QTableWidgetItem, QListWidget, QStackedWidget, QFrame, QCheckBox,
)

#functions calling from 3 files
from Scrapping import ScraperWorker, load_csv, save_csv, FIELDS
from Search import SearchRows, SearchAlgorithms, OPERATORS, TEXT_OPERATORS, ToNumber
from Sorting import RunSort, Benchmark, Algorithms, AlgoNames, ApplicableAlgorithms

#constants
NUMERIC = {"year", "citations", "references", "author_count"}
SLOW_ALGOS = {"Bubble Sort", "Insertion Sort", "Selection Sort"}
COLUMN_WIDTHS = {"doi": 180, "title": 380, "journal": 220, "publisher": 160}
ORDERS = ["Ascending", "Descending"]
SCOPES = ["Full dataset", "Filtered results"]

#a long string just like css file
STYLE = """           
QWidget { font-size: 13px; }
QWidget#page { background: #f3f4f6; }
QLabel#brand { background: #111827; color: white; font-size: 16px; font-weight: bold; padding: 20px 18px 6px 18px; }
QLabel#brandSub { background: #111827; color: #9ca3af; font-size: 11px; padding: 0 18px 14px 18px; }
QListWidget#nav { background: #111827; color: #d1d5db; border: none; font-size: 14px; outline: 0; }
QListWidget#nav::item { padding: 12px 0px; }
QListWidget#nav::item:hover:!selected { background: #1f2937; }
QListWidget#nav::item:selected { background: #2563eb; color: white; }
QLabel#h1 { font-size: 22px; font-weight: bold; color: #111827; }
QLabel#sub { color: #6b7280; }
QLabel#hint { color: #6b7280; font-size: 12px; }
QFrame#card { background: white; border: 1px solid #e5e7eb; border-radius: 8px; }
QLabel#cardTitle { font-weight: bold; color: #374151; font-size: 14px; }
QLabel#statCap { color: #6b7280; font-size: 11px; }
QLabel#statVal { color: #111827; font-size: 17px; font-weight: bold; }
QLabel#bigCount { color: #111827; font-size: 26px; font-weight: bold; }
QPushButton { background: white; border: 1px solid #d1d5db; border-radius: 6px; padding: 7px 18px; }
QPushButton:hover { background: #f3f4f6; }
QPushButton:disabled { color: #9ca3af; background: #f9fafb; }
QPushButton[primary="true"] { background: #2563eb; color: white; border: none; }
QPushButton[primary="true"]:hover { background: #1d4ed8; }
QPushButton[primary="true"]:disabled { background: #bfdbfe; color: white; }
QPushButton[danger="true"] { color: #b91c1c; }
QPushButton[danger="true"]:disabled { color: #9ca3af; }
QLineEdit, QComboBox { background: white; border: 1px solid #d1d5db; border-radius: 6px; padding: 5px 8px; min-height: 22px; }
QLineEdit:disabled, QComboBox:disabled { background: #f3f4f6; color: #9ca3af; }
QProgressBar { border: 1px solid #d1d5db; border-radius: 6px; background: #e5e7eb; text-align: center; min-height: 20px; }
QProgressBar::chunk { background: #2563eb; border-radius: 5px; }
QTableView, QTableWidget { background: white; alternate-background-color: #f9fafb; border: 1px solid #e5e7eb;
    gridline-color: #f3f4f6; selection-background-color: #dbeafe; selection-color: #111827; }
QHeaderView::section { background: #f3f4f6; padding: 7px; border: none; border-bottom: 1px solid #e5e7eb; font-weight: bold; }
"""


def pretty(field):     #change author_count into Author Count
    return field.replace("_", " ").title()


class FuncWorker(QThread):
    #Runs any function in a background thread so the UI does not freeze
    result = pyqtSignal(object)
    failed = pyqtSignal(str)

    def __init__(self, fn):
        super().__init__()
        self.fn = fn

    def run(self):
        try:
            self.result.emit(self.fn())
        except Exception as ex:
            self.failed.emit(str(ex))


class ArticleModel(QAbstractTableModel):
    #gives data to table=data,searching,sorting

    def __init__(self, rows=None):
        super().__init__()
        self.shown = rows or []

    def set_rows(self, rows):
        self.beginResetModel()
        self.shown = rows
        self.endResetModel()

    def rowCount(self, parent=QModelIndex()):
        return 0 if parent.isValid() else len(self.shown)

    def columnCount(self, parent=QModelIndex()):
        return 0 if parent.isValid() else len(FIELDS)

    def data(self, index, role=Qt.DisplayRole):
        if not index.isValid():
            return None
        key = FIELDS[index.column()]
        if role == Qt.DisplayRole:
            return str(self.shown[index.row()].get(key, ""))
        if role == Qt.TextAlignmentRole and key in NUMERIC:
            return int(Qt.AlignRight | Qt.AlignVCenter)
        return None

    def headerData(self, section, orientation, role=Qt.DisplayRole):
        if role == Qt.DisplayRole:
            if orientation == Qt.Horizontal:
                return pretty(FIELDS[section])
            return str(section + 1)
        return None


class RowDialog(QDialog):
    #a small form of Add / edit one article

    def __init__(self, parent=None, row=None):
        super().__init__(parent)
        self.setWindowTitle("Edit article" if row else "Add article")
        self.setMinimumWidth(480)
        form = QFormLayout(self)
        self.edits = {}
        for f in FIELDS:
            e = QLineEdit(str(row.get(f, "")) if row else "")
            self.edits[f] = e
            form.addRow(pretty(f) + ":", e)
        bb = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        bb.accepted.connect(self._accept)
        bb.rejected.connect(self.reject)
        form.addRow(bb)
        self.result_row = None

    def _accept(self):
        out = {}
        for f, e in self.edits.items():
            v = e.text().strip()
            if f in NUMERIC:
                try:
                    v = int(v) if v else 0
                except ValueError:
                    QMessageBox.warning(self, "Invalid", f"'{f}' must be a whole number.")
                    return
            out[f] = v
        if not out["doi"] or not out["title"]:
            QMessageBox.warning(self, "Missing", "DOI and Title are required.")
            return
        self.result_row = out
        self.accept()


class MainWindow(QMainWindow):        #complete window
    def __init__(self):        #side bar of 5 pages
        super().__init__()
        self.setWindowTitle("CS200 Project 1 - Journal Articles")
        self.resize(1300, 780)
        self.rows = load_csv()          # full dataset (persisted in articles.csv)
        self.filtered_rows = None       # filled by the Searching page later
        self.worker = None              # scraper thread
        self.bg = None                  # sorting / benchmark thread

        # sidebar
        side = QWidget()
        side.setFixedWidth(200)
        side.setStyleSheet("background: #111827;")
        sv = QVBoxLayout(side)
        sv.setContentsMargins(0, 0, 0, 0)
        sv.setSpacing(0)
        brand = QLabel("Journal Articles")
        brand.setObjectName("brand")
        sub = QLabel("CS200 - Project 1")
        sub.setObjectName("brandSub")
        self.nav = QListWidget()
        self.nav.setObjectName("nav")
        sv.addWidget(brand)
        sv.addWidget(sub)
        sv.addWidget(self.nav, 1)

        # pages
        self.stack = QStackedWidget()
        for title, page in (("Data", self._data_page()), ("Scraper", self._scraper_page()),
                            ("Searching", self._search_page()), ("Sorting", self._sort_page()), ("Benchmark", self._bench_page())):
            self.nav.addItem("     " + title)
            self.stack.addWidget(page)
        self.nav.currentRowChanged.connect(self.stack.setCurrentIndex)
        self.nav.setCurrentRow(0)

        root = QWidget()
        h = QHBoxLayout(root)
        h.setContentsMargins(0, 0, 0, 0)
        h.setSpacing(0)
        h.addWidget(side)
        h.addWidget(self.stack, 1)
        self.setCentralWidget(root)
        self.setStyleSheet(STYLE)

        # widgets that must be locked while the scraper owns the CSV file
        self.lock_widgets = [self.btn_add, self.btn_edit, self.btn_del] + self.sort_ctrls + self.bench_ctrls
        self._scrape_buttons(running=False)
        self._update_count()

    # ---------- small UI helpers ----------
    def _new_page(self, title, subtitle):       #Create an empty page with a heading and a subtitle
        page = QWidget()
        page.setObjectName("page")
        lay = QVBoxLayout(page)
        lay.setContentsMargins(26, 22, 26, 16)
        lay.setSpacing(12)
        h = QLabel(title)
        h.setObjectName("h1")
        s = QLabel(subtitle)
        s.setObjectName("sub")
        lay.addWidget(h)
        lay.addWidget(s)
        return page, lay

    def _card(self, title=None):      # White card box with optional title
        f = QFrame()
        f.setObjectName("card")
        v = QVBoxLayout(f)
        v.setContentsMargins(16, 14, 16, 14)
        v.setSpacing(10)
        if title:
            t = QLabel(title)
            t.setObjectName("cardTitle")
            v.addWidget(t)
        return f, v

    def _btn(self, text, primary=False, danger=False):      # Button (blue if primary, red text if danger)
        b = QPushButton(text)
        if primary:
            b.setProperty("primary", True)
        if danger:
            b.setProperty("danger", True)
        return b

    def _stat(self, caption):       # Caption + value label for one statistic
        w = QWidget()
        v = QVBoxLayout(w)
        v.setContentsMargins(0, 0, 0, 0)
        v.setSpacing(0)
        cap = QLabel(caption)
        cap.setObjectName("statCap")
        val = QLabel("-")
        val.setObjectName("statVal")
        v.addWidget(cap)
        v.addWidget(val)
        return w, val

    def _make_table(self, model):      # Read-only table bound to a model
        t = QTableView()
        t.setModel(model)
        t.setSelectionBehavior(QAbstractItemView.SelectRows)
        t.setEditTriggers(QAbstractItemView.NoEditTriggers)
        t.setAlternatingRowColors(True)
        t.horizontalHeader().setStretchLastSection(True)
        t.verticalHeader().setDefaultSectionSize(28)
        for i, f in enumerate(FIELDS):
            t.setColumnWidth(i, COLUMN_WIDTHS.get(f, 100))
        return t

    def _column_combo(self):       # Dropdown of all column names
        c = QComboBox()
        for f in FIELDS:
            c.addItem(pretty(f), f)
        return c

    # ---------- page: Data ----------
    def _data_page(self):       #Table, Add/Edit/Delete buttons
        page, lay = self._new_page("Data", "All scraped articles. Double-click a row to edit it.")
        bar = QHBoxLayout()
        self.btn_add = self._btn("Add article", primary=True)
        self.btn_edit = self._btn("Edit")
        self.btn_del = self._btn("Delete", danger=True)
        for b in (self.btn_add, self.btn_edit, self.btn_del):
            bar.addWidget(b)
        bar.addStretch()
        self.count_lbl = QLabel()
        self.count_lbl.setObjectName("sub")
        bar.addWidget(self.count_lbl)
        lay.addLayout(bar)

        self.model = ArticleModel(self.rows)
        self.table = self._make_table(self.model)
        self.table.setSelectionMode(QAbstractItemView.ExtendedSelection)
        self.table.doubleClicked.connect(self.edit_row)
        lay.addWidget(self.table, 1)

        self.btn_add.clicked.connect(self.add_row)
        self.btn_edit.clicked.connect(self.edit_row)
        self.btn_del.clicked.connect(self.delete_rows)
        return page

    # ---------- page: Scraper ----------
    def _scraper_page(self):          #Target, URL, Start/Pause/Resume/Stop, progress bar
        page, lay = self._new_page("Scraper", "Collect articles from the Crossref API into articles.csv.")

        card, v = self._card("Settings")
        g = QGridLayout()
        g.setHorizontalSpacing(12)
        g.setVerticalSpacing(10)
        g.addWidget(QLabel("Target rows"), 0, 0)
        self.target = QSpinBox()
        self.target.setRange(1, 200000)
        self.target.setValue(15000)
        self.target.setFixedWidth(140)
        g.addWidget(self.target, 0, 1)
        g.addWidget(QLabel("Scrape from URL"), 1, 0)
        self.url_in = QLineEdit()
        self.url_in.setPlaceholderText("Optional (bonus), e.g. https://api.crossref.org/works?query=machine+learning")
        g.addWidget(self.url_in, 1, 1, 1, 2)
        g.setColumnStretch(2, 1)
        v.addLayout(g)
        btns = QHBoxLayout()
        self.btn_start = self._btn("Start", primary=True)
        self.btn_pause = self._btn("Pause")
        self.btn_resume = self._btn("Resume")
        self.btn_stop = self._btn("Stop", danger=True)
        for b in (self.btn_start, self.btn_pause, self.btn_resume, self.btn_stop):
            btns.addWidget(b)
        btns.addStretch()
        v.addLayout(btns)
        lay.addWidget(card)

        card2, v2 = self._card("Progress")
        self.scrape_count = QLabel()
        self.scrape_count.setObjectName("bigCount")
        v2.addWidget(self.scrape_count)
        self.bar = QProgressBar()
        self.bar.setRange(0, self.target.value())
        self.bar.setValue(min(len(self.rows), self.target.value()))
        v2.addWidget(self.bar)
        self.status_lbl = QLabel("Idle")
        self.status_lbl.setObjectName("sub")
        v2.addWidget(self.status_lbl)
        self._show_scrape_count(len(self.rows), self.target.value())
        lay.addWidget(card2)
        lay.addStretch()

        self.btn_start.clicked.connect(self.start_scrape)
        self.btn_pause.clicked.connect(self.pause_scrape)
        self.btn_resume.clicked.connect(self.resume_scrape)
        self.btn_stop.clicked.connect(self.stop_scrape)
        return page

    # ---------- page: Searching ----------
    def _search_page(self):      #4 conditions, Linear/Binary
        page, lay = self._new_page("Searching",
                                   "Find articles with one or more conditions (Linear or Binary search).")
        card, v = self._card("Conditions")
        arow = QHBoxLayout()
        arow.setSpacing(10)
        arow.addWidget(QLabel("Algorithm"))
        self.search_algo = QComboBox()
        self.search_algo.addItems(list(SearchAlgorithms))
        arow.addWidget(self.search_algo)
        self.search_algo_info = QLabel()
        self.search_algo_info.setObjectName("hint")
        arow.addWidget(self.search_algo_info)
        arow.addStretch()
        v.addLayout(arow)
        g = QGridLayout()
        g.setHorizontalSpacing(10)
        g.setVerticalSpacing(8)
        self.cond_rows = []
        for i in range(4):
            if i == 0:
                join = QLabel("Where")
            else:
                join = QComboBox()
                join.addItems(["AND", "OR"])
            neg = QCheckBox("NOT")
            col = self._column_combo()
            if i == 0:
                col.setCurrentIndex(col.findData("title"))
            op = QComboBox()
            op.addItems(OPERATORS)
            val = QLineEdit()
            val.setPlaceholderText("value (leave empty to skip this row)")
            val.returnPressed.connect(self.do_search)
            for j, w in enumerate((join, neg, col, op, val)):
                g.addWidget(w, i, j)
            self.cond_rows.append((join, neg, col, op, val))
        g.setColumnStretch(4, 1)
        v.addLayout(g)
        hint = QLabel("Conditions are combined from left to right. NOT reverses a single condition. "
                      "> >= < <= work on numbers. Binary Search needs sorted data (the column is sorted "
                      "first) and only supports 'equals'.")
        hint.setObjectName("hint")
        v.addWidget(hint)
        btns = QHBoxLayout()
        self.btn_search = self._btn("Search", primary=True)
        self.btn_clear = self._btn("Clear")
        btns.addWidget(self.btn_search)
        btns.addWidget(self.btn_clear)
        btns.addStretch()
        v.addLayout(btns)
        lay.addWidget(card)

        card2, v2 = self._card("Result")
        row = QHBoxLayout()
        self.search_stats = {}
        for cap in ("Algorithm", "Matches", "Rows searched", "Time (ms)", "Sorted first (ms)", "Complexity"):
            w, val = self._stat(cap)
            self.search_stats[cap] = val
            row.addWidget(w, 1)
        v2.addLayout(row)
        lay.addWidget(card2)

        self.search_model = ArticleModel(self.rows)
        self.search_table = self._make_table(self.search_model)
        lay.addWidget(self.search_table, 1)
        self.search_count_lbl = QLabel()
        self.search_count_lbl.setObjectName("hint")
        lay.addWidget(self.search_count_lbl)
        self._reset_search()

        self.search_algo.currentIndexChanged.connect(self.update_search_ops)
        self.update_search_ops()
        self.btn_search.clicked.connect(self.do_search)
        self.btn_clear.clicked.connect(lambda: self._reset_search(clear_inputs=True))
        return page

    def update_search_ops(self):
        #Binary Search only supports equals
        algo = self.search_algo.currentText()
        binary = algo == "Binary Search"
        self.search_algo_info.setText(SearchAlgorithms[algo])
        for join, neg, col, op, val in self.cond_rows:
            m = op.model()
            for i in range(op.count()):
                m.item(i).setEnabled(not binary or op.itemText(i) == "equals")
            if binary and op.currentText() != "equals":
                op.setCurrentText("equals")

    def do_search(self):
        conds = []
        for i, (join, neg, col, op, val) in enumerate(self.cond_rows):
            text = val.text().strip()
            if not text:
                continue
            if op.currentText() not in TEXT_OPERATORS and ToNumber(text) is None:
                QMessageBox.warning(self, "Search", f"'{op.currentText()}' needs a number (row {i + 1}).")
                return
            conds.append({"field": col.currentData(), "op": op.currentText(), "value": text,
                          "negate": neg.isChecked(), "join": "AND" if i == 0 else join.currentText()})
        if not conds:
            QMessageBox.information(self, "Search", "Type a value in at least one row.")
            return
        try:
            res = SearchRows(self.rows, conds, self.search_algo.currentText())
        except ValueError as ex:
            QMessageBox.warning(self, "Search", str(ex))
            return
        self.filtered_rows = res["rows"]            # used by Sorting -> "Filtered results"
        self.search_model.set_rows(res["rows"])
        s = self.search_stats
        s["Algorithm"].setText(res["algo"])
        s["Matches"].setText(f"{len(res['rows']):,}")
        s["Rows searched"].setText(f"{res['n']:,}")
        s["Time (ms)"].setText(f"{res['time_ms']:.2f}")
        s["Sorted first (ms)"].setText(f"{res['prep_ms']:.2f}" if res["algo"] == "Binary Search" else "-")
        s["Complexity"].setText(res["complexity"])
        self.search_count_lbl.setText(f"{len(res['rows']):,} of {res['n']:,} articles match")

    def _reset_search(self, clear_inputs=False):
        self.filtered_rows = None
        self.search_model.set_rows(self.rows)
        for cap, val in self.search_stats.items():
            val.setText("-")
        self.search_count_lbl.setText(f"No search yet - showing all {len(self.rows):,} articles")
        if clear_inputs:
            for join, neg, col, op, val in self.cond_rows:
                val.clear()
                neg.setChecked(False)

    # ---------- page: Sorting ----------
    def _sort_page(self):        #Column, algorithm, multi-level, scope
        page, lay = self._new_page("Sorting", "Sort by one or more columns. The original data is never reordered.")

        card, v = self._card("Options")
        g = QGridLayout()
        g.setHorizontalSpacing(10)
        g.setVerticalSpacing(10)
        self.sort_col = self._column_combo()
        self.sort_order = QComboBox()
        self.sort_order.addItems(ORDERS)
        self.sort_algo = QComboBox()
        self.sort_algo.addItems(AlgoNames)
        self.algo_info = QLabel()
        self.algo_info.setObjectName("hint")
        self.sort_scope = QComboBox()
        self.sort_scope.addItems(SCOPES)
        g.addWidget(QLabel("Sort by"), 0, 0)
        g.addWidget(self.sort_col, 0, 1)
        g.addWidget(self.sort_order, 0, 2)
        g.addWidget(QLabel("Algorithm"), 1, 0)
        g.addWidget(self.sort_algo, 1, 1)
        g.addWidget(self.algo_info, 1, 2)
        g.addWidget(QLabel("Scope"), 2, 0)
        g.addWidget(self.sort_scope, 2, 1)

        self.extra_cols = []
        for n, row in ((2, 0), (3, 1)):
            c = QComboBox()
            c.addItem("(none)", None)
            for f in FIELDS:
                c.addItem(pretty(f), f)
            o = QComboBox()
            o.addItems(ORDERS)
            g.addWidget(QLabel(f"Then by (level {n})"), row, 4)
            g.addWidget(c, row, 5)
            g.addWidget(o, row, 6)
            self.extra_cols.append((c, o))
        hint = QLabel("Levels 2 and 3 break ties of the first column (multi-level sort).")
        hint.setObjectName("hint")
        g.addWidget(hint, 2, 4, 1, 3)
        g.setColumnMinimumWidth(3, 30)
        g.setColumnStretch(7, 1)
        v.addLayout(g)

        btns = QHBoxLayout()
        self.btn_sort = self._btn("Sort", primary=True)
        self.btn_reset = self._btn("Reset order")
        btns.addWidget(self.btn_sort)
        btns.addWidget(self.btn_reset)
        self.sort_status = QLabel("")
        self.sort_status.setObjectName("hint")
        btns.addWidget(self.sort_status)
        btns.addStretch()
        v.addLayout(btns)
        lay.addWidget(card)

        card2, v2 = self._card("Last sort")
        row = QHBoxLayout()
        self.stat_vals = {}
        for cap in ("Algorithm", "Rows", "Time (ms)", "Comparisons", "Swaps", "Complexity", "Stable"):
            w, val = self._stat(cap)
            self.stat_vals[cap] = val
            row.addWidget(w, 1)
        v2.addLayout(row)
        self.sort_note = QLabel("")
        self.sort_note.setObjectName("hint")
        v2.addWidget(self.sort_note)
        lay.addWidget(card2)

        self.sort_model = ArticleModel(self.rows)
        self.sort_table = self._make_table(self.sort_model)
        lay.addWidget(self.sort_table, 1)
        self.sort_count_lbl = QLabel()
        self.sort_count_lbl.setObjectName("hint")
        lay.addWidget(self.sort_count_lbl)
        self._update_sort_count()

        self.sort_ctrls = [self.sort_col, self.sort_order, self.sort_algo, self.sort_scope,
                           self.btn_sort, self.btn_reset]
        for c, o in self.extra_cols:
            self.sort_ctrls += [c, o]

        self.sort_col.currentIndexChanged.connect(self.update_algo_choices)
        self.sort_algo.currentIndexChanged.connect(self.update_algo_info)
        self.btn_sort.clicked.connect(self.do_sort)
        self.btn_reset.clicked.connect(self.show_all)
        return page

    # ---------- page: Benchmark ----------
    BENCH_HEADERS = ["Algorithm", "Complexity", "Stable", "Rows", "Time (ms)", "Comparisons", "Swaps", "Note"]

    def _bench_page(self):
        page, lay = self._new_page("Benchmark","Run every sorting algorithm on one column and compare them.")
        card, v = self._card("Options")
        row = QHBoxLayout()
        row.setSpacing(10)
        self.bench_col = self._column_combo()
        self.bench_scope = QComboBox()
        self.bench_scope.addItems(SCOPES)
        self.bench_n = QSpinBox()
        self.bench_n.setRange(100, 200000)
        self.bench_n.setValue(3000)
        self.bench_n.setSingleStep(500)
        self.btn_bench = self._btn("Run benchmark", primary=True)
        for lbl, w in (("Column", self.bench_col), ("Scope", self.bench_scope), ("Rows to test", self.bench_n)):
            row.addWidget(QLabel(lbl))
            row.addWidget(w)
        row.addWidget(self.btn_bench)
        row.addStretch()
        v.addLayout(row)
        hint = QLabel("Bubble, Insertion and Selection sort are O(n^2): keep the row count low (about 3000) or they take minutes.")
        hint.setObjectName("hint")
        v.addWidget(hint)
        self.bench_status = QLabel("")
        self.bench_status.setObjectName("hint")
        v.addWidget(self.bench_status)
        lay.addWidget(card)

        self.bench_table = QTableWidget(0, len(self.BENCH_HEADERS))
        self.bench_table.setHorizontalHeaderLabels(self.BENCH_HEADERS)
        self.bench_table.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.bench_table.setAlternatingRowColors(True)
        self.bench_table.verticalHeader().setVisible(False)
        self.bench_table.horizontalHeader().setStretchLastSection(True)
        lay.addWidget(self.bench_table, 1)
        note = QLabel("Bold row = fastest. Swaps = element moves for Merge, Hybrid, Insertion, Shell, Counting, Radix and Bucket sort.")
        note.setObjectName("hint")
        lay.addWidget(note)

        self.bench_ctrls = [self.bench_col, self.bench_scope, self.bench_n, self.btn_bench]
        self.btn_bench.clicked.connect(self.do_benchmark)
        return page

    # ---------- state helpers ----------     	Buttons lock/unlock, counts
    def _scrape_buttons(self, running, paused=False):
        self.btn_start.setEnabled(not running)
        self.btn_pause.setEnabled(running and not paused)
        self.btn_resume.setEnabled(running and paused)
        self.btn_stop.setEnabled(running)
        self.target.setEnabled(not running)
        self.url_in.setEnabled(not running)
        # CRUD, sorting and benchmark are locked while scraping (scraper owns the CSV file)
        for w in self.lock_widgets:
            w.setEnabled(not running)
        if not running:
            self.update_algo_choices()

    def _update_count(self):
        self.count_lbl.setText(f"{len(self.rows):,} articles")

    def _update_sort_count(self):
        self.sort_count_lbl.setText(f"Showing {len(self.sort_model.shown):,} rows")

    def _show_scrape_count(self, done, target):
        self.scrape_count.setText(f"{done:,} / {target:,} articles")

    def _refresh_sort_view(self):
        self.sort_model.set_rows(self.rows)
        self._update_sort_count()
        self.update_algo_choices()
        self._reset_search()                # data changed: old search result is out of date

    # ---------- scraper control ----------
    def start_scrape(self):
        url = self.url_in.text().strip() or None
        self.bar.setRange(0, self.target.value())
        self.worker = ScraperWorker(target=self.target.value(), url=url)
        self.worker.progress.connect(self.on_progress)
        self.worker.status.connect(self.status_lbl.setText)
        self.worker.done.connect(self.on_done)
        self._scrape_buttons(running=True)
        self.worker.start()

    def pause_scrape(self):
        if self.worker:
            self.worker.pause()
            self._scrape_buttons(running=True, paused=True)

    def resume_scrape(self):
        if self.worker:
            self.worker.resume()
            self._scrape_buttons(running=True, paused=False)

    def stop_scrape(self):
        if self.worker:
            self.worker.stop()

    def on_progress(self, done, target):
        self.bar.setRange(0, target)
        self.bar.setValue(min(done, target))
        self._show_scrape_count(done, target)

    def on_done(self, total):
        self.rows = load_csv()
        self.model.set_rows(self.rows)
        self._scrape_buttons(running=False)
        self._update_count()
        self._refresh_sort_view()
        self._show_scrape_count(len(self.rows), self.target.value())

    # ---------- sorting ----------
    def update_algo_choices(self):
        #Grey out algorithms that cannot sort the chosen column (e.g. Radix on text)."""
        field = self.sort_col.currentData()
        ok = set(ApplicableAlgorithms(self.rows, field)) if self.rows else set(AlgoNames)
        item_model = self.sort_algo.model()
        for i, name in enumerate(AlgoNames):
            item_model.item(i).setEnabled(name in ok)
        if self.sort_algo.currentText() not in ok:
            self.sort_algo.setCurrentIndex(next(i for i, n in enumerate(AlgoNames) if n in ok))
        self.update_algo_info()

    def update_algo_info(self):
        info = Algorithms[self.sort_algo.currentText()]
        self.algo_info.setText(f"{info['complexity']}  |  {'Stable' if info['stable'] else 'Not stable'}")

    def _base_rows(self, scope_combo):
        if scope_combo.currentIndex() == 1 and self.filtered_rows is not None:
            return self.filtered_rows
        return self.rows

    def _set_busy(self, busy):
        for w in (self.btn_sort, self.btn_reset, self.btn_bench, self.btn_start,
                  self.btn_add, self.btn_edit, self.btn_del):
            w.setEnabled(not busy)

    def _run_bg(self, fn, on_ok, status_label, msg):
        self._set_busy(True)
        status_label.setText(msg)
        self.bg = FuncWorker(fn)
        self.bg.result.connect(on_ok)
        self.bg.failed.connect(lambda m: self.on_bg_failed(m, status_label))
        self.bg.start()

    def on_bg_failed(self, msg, status_label):
        self._set_busy(False)
        status_label.setText("Failed")
        QMessageBox.warning(self, "Error", msg)

    def do_sort(self):
        base = self._base_rows(self.sort_scope)
        if not base:
            QMessageBox.information(self, "Sort", "Nothing to sort.")
            return
        first = self.sort_col.currentData()
        columns = [(first, self.sort_order.currentIndex() == 1)]
        used = {first: "Sort by"}                      # kaunsa column kis level par use hua

        for n, (c, o) in enumerate(self.extra_cols, start=2):
            f = c.currentData()
            if f is None:                              # "(none)" select hai to skip
                continue
            if f in used:                              # same column dobara select hua
                QMessageBox.warning(self, "Sort",
                f"'{c.currentText()}' is already selected in '{used[f]}'.\n"
                f"Each column can be used only once in a multi-level sort.")
                return                                 # sort nahi chalega
            used[f] = f"Then by (level {n})"
            columns.append((f, o.currentIndex() == 1))
        algo = self.sort_algo.currentText()
        if algo in SLOW_ALGOS and len(base) > 5000:
            if QMessageBox.question(self, "Slow sort",
                    f"{algo} is O(n^2) and {len(base):,} rows may take several minutes. Continue?"
                    ) != QMessageBox.Yes:
                return
        self._run_bg(lambda: RunSort(base, columns, algo), self.on_sorted,
                     self.sort_status, f"Sorting with {algo}...")

    def on_sorted(self, res):
        self._set_busy(False)
        self.sort_model.set_rows(res["rows"])
        self._update_sort_count()
        self.sort_status.setText("")
        v = self.stat_vals
        v["Algorithm"].setText(res["algo"])
        v["Rows"].setText(f"{res['n']:,}")
        v["Time (ms)"].setText(f"{res['time_ms']:.2f}")
        v["Comparisons"].setText(f"{res['comparisons']:,}")
        v["Swaps"].setText(f"{res['swaps']:,}")
        v["Complexity"].setText(res["complexity"])
        v["Stable"].setText("Yes" if res["stable"] else "No")
        self.sort_note.setText(res["note"])

    def show_all(self):
        self._refresh_sort_view()
        self.sort_status.setText("Original order restored")

    # ---------- benchmark ----------
    def do_benchmark(self):
        base = self._base_rows(self.bench_scope)
        if not base:
            QMessageBox.information(self, "Benchmark", "Nothing to benchmark.")
            return
        field, limit = self.bench_col.currentData(), self.bench_n.value()
        self.bench_title = self.bench_col.currentText()
        self._run_bg(lambda: Benchmark(base, field, limit), self.on_benchmark,
                     self.bench_status, "Running all algorithms...")

    def on_benchmark(self, results):
        self._set_busy(False)
        t = self.bench_table
        t.setRowCount(len(results))
        times = [r["time_ms"] for r in results if r["time_ms"] is not None]
        best = min(times) if times else None
        for i, r in enumerate(results):
            ran = r["time_ms"] is not None
            vals = [r["algo"], r["complexity"], "Yes" if r["stable"] else "No", f"{r['n']:,}",
                    f"{r['time_ms']:.2f}" if ran else "-",
                    f"{r['comparisons']:,}" if ran else "-",
                    f"{r['swaps']:,}" if ran else "-", r["note"]]
            for j, val in enumerate(vals):
                it = QTableWidgetItem(val)
                if 3 <= j <= 6:
                    it.setTextAlignment(int(Qt.AlignRight | Qt.AlignVCenter))
                if ran and r["time_ms"] == best:
                    f = QFont()
                    f.setBold(True)
                    it.setFont(f)
                if not ran:
                    it.setForeground(Qt.gray)
                t.setItem(i, j, it)
        t.resizeColumnsToContents()
        t.setColumnWidth(1, t.columnWidth(1) + 30)
        t.horizontalHeader().setStretchLastSection(True)
        self.bench_status.setText(f"Done: column '{self.bench_title}', {results[0]['n']:,} rows tested.")

    # ---------- CRUD ----------
    def _selected_rows(self):
        return sorted({i.row() for i in self.table.selectionModel().selectedRows()})

    def _save(self):
        save_csv(self.rows)

    def add_row(self):
        dlg = RowDialog(self)
        if dlg.exec_() == QDialog.Accepted:
            if any(r["doi"] == dlg.result_row["doi"] for r in self.rows):
                QMessageBox.warning(self, "Duplicate", "An article with this DOI already exists.")
                return
            self.rows.append(dlg.result_row)
            self.model.set_rows(self.rows)
            self._save()
            self._update_count()
            self._refresh_sort_view()
            self.table.scrollToBottom()

    def edit_row(self, *_):
        sel = self._selected_rows()
        if len(sel) != 1:
            QMessageBox.information(self, "Edit", "Select exactly one row to edit.")
            return
        row = self.model.shown[sel[0]]
        dlg = RowDialog(self, row)
        if dlg.exec_() == QDialog.Accepted:
            row.update(dlg.result_row)       # same dict object as in self.rows
            self.model.set_rows(self.model.shown)
            self.sort_model.set_rows(self.sort_model.shown)
            self.search_model.set_rows(self.search_model.shown)
            self._save()

    def delete_rows(self):
        sel = self._selected_rows()
        if not sel:
            QMessageBox.information(self, "Delete", "Select one or more rows first.")
            return
        if QMessageBox.question(self, "Delete", f"Delete {len(sel)} selected row(s)?") != QMessageBox.Yes:
            return
        doomed = {id(self.model.shown[i]) for i in sel}
        self.rows = [r for r in self.rows if id(r) not in doomed]
        self.model.set_rows(self.rows)
        self._save()
        self._update_count()
        self._refresh_sort_view()

    def closeEvent(self, e):
        if self.worker and self.worker.isRunning():
            self.worker.stop()
            self.worker.wait(5000)
        if self.bg and self.bg.isRunning():
            if not self.bg.wait(3000):
                self.bg.terminate()
                self.bg.wait()
        e.accept()


if __name__ == "__main__":        #it start the program
    app = QApplication(sys.argv)
    w = MainWindow()
    w.show()
    sys.exit(app.exec_())