"""CS200 Project 1 - Journal Articles manager (PyQt5).

Needs Task2.py (the scraper) in the same folder.
Run:  python main.py
"""
import sys

from PyQt5.QtCore import Qt, QAbstractTableModel, QModelIndex
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QTableView,
    QPushButton, QLabel, QProgressBar, QSpinBox, QLineEdit, QMessageBox,
    QDialog, QFormLayout, QDialogButtonBox, QAbstractItemView, QGroupBox,
)

from Task2 import ScraperWorker, load_csv, save_csv, FIELDS

NUMERIC = {"year", "citations", "references", "author_count"}


class ArticleModel(QAbstractTableModel):
    """Shows `shown` (a list of row dicts). Later: sorting/filtering just
    replace `shown` via set_rows()."""

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
                return FIELDS[section].replace("_", " ").title()
            return str(section + 1)
        return None


class RowDialog(QDialog):
    """Add / edit one article."""

    def __init__(self, parent=None, row=None):
        super().__init__(parent)
        self.setWindowTitle("Edit article" if row else "Add article")
        self.setMinimumWidth(480)
        form = QFormLayout(self)
        self.edits = {}
        for f in FIELDS:
            e = QLineEdit(str(row.get(f, "")) if row else "")
            self.edits[f] = e
            form.addRow(f.replace("_", " ").title() + ":", e)
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


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("CS200 Project 1 - Journal Articles")
        self.resize(1250, 720)
        self.rows = load_csv()          # full dataset (persisted in articles.csv)
        self.worker = None

        self.model = ArticleModel(self.rows)
        self.table = QTableView()
        self.table.setModel(self.model)
        self.table.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.table.setSelectionMode(QAbstractItemView.ExtendedSelection)
        self.table.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.table.setAlternatingRowColors(True)
        self.table.horizontalHeader().setStretchLastSection(True)
        self.table.doubleClicked.connect(self.edit_row)
        self._set_widths()

        central = QWidget()
        lay = QVBoxLayout(central)
        lay.addWidget(self._scraper_box())
        lay.addWidget(self._crud_bar())
        self._scrape_buttons(running=False)
        lay.addWidget(self.table, 1)
        self.count_lbl = QLabel()
        lay.addWidget(self.count_lbl)
        self.setCentralWidget(central)
        self._update_count()

    # ---------- UI builders ----------
    def _set_widths(self):
        widths = {"doi": 180, "title": 380, "journal": 220, "publisher": 160}
        for i, f in enumerate(FIELDS):
            self.table.setColumnWidth(i, widths.get(f, 90))

    def _scraper_box(self):
        box = QGroupBox("Scraper (Crossref)")
        v = QVBoxLayout(box)
        r1 = QHBoxLayout()
        r1.addWidget(QLabel("Target rows:"))
        self.target = QSpinBox()
        self.target.setRange(1, 200000)
        self.target.setValue(15000)
        r1.addWidget(self.target)
        self.btn_start = QPushButton("Start")
        self.btn_pause = QPushButton("Pause")
        self.btn_resume = QPushButton("Resume")
        self.btn_stop = QPushButton("Stop")
        for b in (self.btn_start, self.btn_pause, self.btn_resume, self.btn_stop):
            r1.addWidget(b)
        r1.addStretch()
        v.addLayout(r1)

        r2 = QHBoxLayout()
        r2.addWidget(QLabel("Optional URL:"))
        self.url_in = QLineEdit()
        self.url_in.setPlaceholderText(
            "e.g. https://api.crossref.org/works?query=machine+learning  (bonus: scrape from this URL)")
        r2.addWidget(self.url_in, 1)
        v.addLayout(r2)

        r3 = QHBoxLayout()
        self.bar = QProgressBar()
        self.bar.setRange(0, 15000)
        self.bar.setValue(len(self.rows))
        self.status_lbl = QLabel("Idle")
        r3.addWidget(self.bar, 1)
        r3.addWidget(self.status_lbl)
        v.addLayout(r3)

        self.btn_start.clicked.connect(self.start_scrape)
        self.btn_pause.clicked.connect(self.pause_scrape)
        self.btn_resume.clicked.connect(self.resume_scrape)
        self.btn_stop.clicked.connect(self.stop_scrape)
        return box

    def _crud_bar(self):
        w = QWidget()
        h = QHBoxLayout(w)
        h.setContentsMargins(0, 0, 0, 0)
        self.btn_add = QPushButton("Add")
        self.btn_edit = QPushButton("Edit")
        self.btn_del = QPushButton("Delete")
        for b in (self.btn_add, self.btn_edit, self.btn_del):
            h.addWidget(b)
        h.addStretch()
        self.btn_add.clicked.connect(self.add_row)
        self.btn_edit.clicked.connect(self.edit_row)
        self.btn_del.clicked.connect(self.delete_rows)
        return w

    def _scrape_buttons(self, running, paused=False):
        self.btn_start.setEnabled(not running)
        self.btn_pause.setEnabled(running and not paused)
        self.btn_resume.setEnabled(running and paused)
        self.btn_stop.setEnabled(running)
        self.target.setEnabled(not running)
        self.url_in.setEnabled(not running)
        # CRUD is locked while scraping (scraper owns the CSV file)
        for b in (self.btn_add, self.btn_edit, self.btn_del):
            b.setEnabled(not running)

    def _update_count(self):
        self.count_lbl.setText(
            f"Showing {len(self.model.shown):,} of {len(self.rows):,} articles")

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
        self.count_lbl.setText(f"Scraped {done:,} / {target:,}")

    def on_done(self, total):
        self.rows = load_csv()
        self.model.set_rows(self.rows)
        self._scrape_buttons(running=False)
        self._update_count()

    # ---------- CRUD ----------
    def _selected_rows(self):
        idx = sorted({i.row() for i in self.table.selectionModel().selectedRows()})
        return idx

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

    def closeEvent(self, e):
        if self.worker and self.worker.isRunning():
            self.worker.stop()
            self.worker.wait(5000)
        e.accept()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    w = MainWindow()
    w.show()
    sys.exit(app.exec_())