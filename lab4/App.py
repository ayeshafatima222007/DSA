import sys, os, csv, threading, requests
from PyQt5.QtCore import QThread, pyqtSignal
from PyQt5.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QTableWidget, QTableWidgetItem, QPushButton, QProgressBar, QLabel, QDialog,
    QFormLayout, QLineEdit, QDialogButtonBox, QMessageBox, QAbstractItemView)

CSV_FILE = "books.csv"
TARGET = 15000
COLUMNS = ["title", "author", "first_publish_year", "edition_count", "language",
           "publisher", "pages", "rating", "ratings_count", "subject"]
SUBJECTS = ["fiction", "history", "science", "romance", "fantasy", "mystery",
            "biography", "art", "poetry", "children"]
API = "https://openlibrary.org/search.json"
FIELDS = ("title,author_name,first_publish_year,edition_count,language,publisher,"
          "number_of_pages_median,ratings_average,ratings_count,subject")


def first(v):
    return v[0] if isinstance(v, list) and v else (v if v is not None and not isinstance(v, list) else "")


def to_row(d):
    return [d.get("title", ""), first(d.get("author_name")), d.get("first_publish_year", ""),
            d.get("edition_count", ""), first(d.get("language")), first(d.get("publisher")),
            d.get("number_of_pages_median", ""),
            round(d["ratings_average"], 2) if d.get("ratings_average") else "",
            d.get("ratings_count", ""), ", ".join(d.get("subject", [])[:3])]


class Scraper(QThread):
    progress = pyqtSignal(int)
    status = pyqtSignal(str)
    batch = pyqtSignal(list)

    def __init__(self, keys, total, si=0, page=1):
        super().__init__()
        self.keys, self.total, self.si, self.page = keys, total, si, page
        self.run_ev = threading.Event(); self.run_ev.set()
        self.stopped = False

    def pause(self): self.run_ev.clear()
    def resume(self): self.run_ev.set()
    def stop(self): self.stopped = True; self.run_ev.set()

    def run(self):
        while self.total < TARGET and self.si < len(SUBJECTS) and not self.stopped:
            self.run_ev.wait()
            if self.stopped: break
            try:
                r = requests.get(API, params={"q": "subject:" + SUBJECTS[self.si], "page": self.page,
                                              "limit": 100, "fields": FIELDS}, timeout=30)
                docs = r.json().get("docs", [])
            except Exception as e:
                self.status.emit(f"Error: {e} - retrying"); self.msleep(2000); continue
            if not docs:
                self.si += 1; self.page = 1; continue
            rows = []
            for d in docs:
                row = to_row(d)
                k = (row[0], row[1])
                if row[0] and row[1] and k not in self.keys:
                    self.keys.add(k); rows.append(row)
            self.page += 1
            self.total += len(rows)
            self.batch.emit(rows)
            self.progress.emit(self.total)
            self.status.emit(f"Scraping '{SUBJECTS[self.si]}' page {self.page}: {self.total} records")
        self.status.emit("Stopped" if self.stopped else "Done")


class RecordDialog(QDialog):
    def __init__(self, values=None):
        super().__init__()
        self.setWindowTitle("Record")
        form = QFormLayout(self)
        self.edits = []
        for i, c in enumerate(COLUMNS):
            e = QLineEdit(str(values[i]) if values else "")
            form.addRow(c, e); self.edits.append(e)
        bb = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        bb.accepted.connect(self.accept); bb.rejected.connect(self.reject)
        form.addRow(bb)

    def values(self): return [e.text() for e in self.edits]


class Main(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("CS200 Project 1 - Books")
        self.resize(1200, 700)
        self.data = []
        self.keys = set()
        self.thread = None
        self.load_csv()

        w = QWidget(); self.setCentralWidget(w)
        lay = QVBoxLayout(w)
        bar = QHBoxLayout(); lay.addLayout(bar)
        self.btns = {}
        for name, fn in [("Start", self.start), ("Pause", self.pause_resume), ("Stop", self.stop),
                         ("Add", self.add), ("Edit", self.edit), ("Delete", self.delete)]:
            b = QPushButton(name); b.clicked.connect(fn); bar.addWidget(b); self.btns[name] = b
        self.btns["Pause"].setEnabled(False); self.btns["Stop"].setEnabled(False)
        self.progress = QProgressBar(); self.progress.setMaximum(TARGET)
        self.progress.setValue(min(len(self.data), TARGET)); lay.addWidget(self.progress)
        self.lbl = QLabel(f"{len(self.data)} records loaded"); lay.addWidget(self.lbl)

        self.table = QTableWidget(0, len(COLUMNS))
        self.table.setHorizontalHeaderLabels(COLUMNS)
        self.table.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.table.setEditTriggers(QAbstractItemView.NoEditTriggers)
        lay.addWidget(self.table)
        self.refresh()

    # ---------- persistence ----------
    def load_csv(self):
        if os.path.exists(CSV_FILE):
            with open(CSV_FILE, newline="", encoding="utf-8") as f:
                r = csv.reader(f); next(r, None)
                self.data = [row for row in r if len(row) == len(COLUMNS)]
            self.keys = {(r[0], r[1]) for r in self.data}

    def save_csv(self):
        with open(CSV_FILE, "w", newline="", encoding="utf-8") as f:
            w = csv.writer(f); w.writerow(COLUMNS); w.writerows(self.data)

    # ---------- table ----------
    def refresh(self):
        self.table.setUpdatesEnabled(False)
        self.table.setRowCount(len(self.data))
        for i, row in enumerate(self.data):
            for j, v in enumerate(row):
                self.table.setItem(i, j, QTableWidgetItem(str(v)))
        self.table.setUpdatesEnabled(True)
        self.lbl.setText(f"{len(self.data)} records")

    def append_rows(self, rows):
        self.data.extend(rows)
        self.table.setUpdatesEnabled(False)
        for row in rows:
            i = self.table.rowCount(); self.table.insertRow(i)
            for j, v in enumerate(row):
                self.table.setItem(i, j, QTableWidgetItem(str(v)))
        self.table.setUpdatesEnabled(True)
        self.save_csv()

    # ---------- scraper controls ----------
    def start(self):
        if self.thread and self.thread.isRunning(): return
        si, page = (self.thread.si, self.thread.page) if self.thread else (0, 1)
        self.thread = Scraper(self.keys, len(self.data), si, page)
        self.thread.batch.connect(self.append_rows)
        self.thread.progress.connect(self.progress.setValue)
        self.thread.status.connect(self.lbl.setText)
        self.thread.finished.connect(lambda: self.set_running(False))
        self.thread.start(); self.set_running(True)

    def set_running(self, on):
        self.btns["Start"].setEnabled(not on)
        self.btns["Pause"].setEnabled(on); self.btns["Stop"].setEnabled(on)
        self.btns["Pause"].setText("Pause")

    def pause_resume(self):
        if not self.thread: return
        if self.btns["Pause"].text() == "Pause":
            self.thread.pause(); self.btns["Pause"].setText("Resume")
        else:
            self.thread.resume(); self.btns["Pause"].setText("Pause")

    def stop(self):
        if self.thread: self.thread.stop()

    # ---------- CRUD ----------
    def add(self):
        d = RecordDialog()
        if d.exec_():
            self.data.append(d.values()); self.save_csv(); self.refresh()

    def edit(self):
        r = self.table.currentRow()
        if r < 0: return QMessageBox.information(self, "Edit", "Select a row first")
        d = RecordDialog(self.data[r])
        if d.exec_():
            self.data[r] = d.values(); self.save_csv(); self.refresh()

    def delete(self):
        r = self.table.currentRow()
        if r < 0: return QMessageBox.information(self, "Delete", "Select a row first")
        if QMessageBox.question(self, "Delete", "Delete this record?") == QMessageBox.Yes:
            del self.data[r]; self.save_csv(); self.refresh()

    def closeEvent(self, e):
        if self.thread and self.thread.isRunning():
            self.thread.stop(); self.thread.wait(5000)
        self.save_csv(); e.accept()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    m = Main(); m.show()
    sys.exit(app.exec_())