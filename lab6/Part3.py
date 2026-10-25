import sys
import json
import os
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QTableWidget, QTableWidgetItem, QLabel, QPushButton, QMessageBox
)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QColor

ROWS, COLS = 10, 10
SAVE_FILE = "grid_data.json"


class ExcelGrid(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Excel Grid View")
        self.resize(900, 500)

        central = QWidget()
        self.setCentralWidget(central)
        layout = QVBoxLayout(central)

        # Toolbar: address label + buttons
        bar = QHBoxLayout()
        bar.addWidget(QLabel("Selected cell:"))
        self.address = QLabel("A1")
        self.address.setMinimumWidth(60)
        self.address.setAlignment(Qt.AlignCenter)
        self.address.setStyleSheet(
            "border:1px solid #999; background:white; font-weight:bold; padding:3px;")
        bar.addWidget(self.address)

        save_btn = QPushButton("Save")
        clear_btn = QPushButton("Clear All")
        save_btn.clicked.connect(self.save)
        clear_btn.clicked.connect(self.clear_all)
        bar.addWidget(save_btn)
        bar.addWidget(clear_btn)
        self.status = QLabel("")
        self.status.setStyleSheet("color:#217346;")
        bar.addWidget(self.status)
        bar.addStretch()
        layout.addLayout(bar)

        # Grid
        self.table = QTableWidget(ROWS, COLS)
        self.table.setHorizontalHeaderLabels([chr(65 + c) for c in range(COLS)])
        self.table.setVerticalHeaderLabels([str(r + 1) for r in range(ROWS)])
        self.table.setStyleSheet(
            "QTableWidget::item:selected { background:#c6e0b4; color:black; }"
            "QTableWidget::item:focus { border:2px solid #217346; }")
        for r in range(ROWS):
            for c in range(COLS):
                self.table.setItem(r, c, QTableWidgetItem(""))
        self.table.currentCellChanged.connect(self.on_cell_changed)
        layout.addWidget(self.table)

        self.load()
        self.table.setCurrentCell(0, 0)
        self.table.setFocus()

    def on_cell_changed(self, r, c, *_):
        if r >= 0 and c >= 0:
            self.address.setText(f"{chr(65 + c)}{r + 1}")

    def keyPressEvent(self, e):
        # Enter: commit the edit (if any) and move down
        if e.key() in (Qt.Key_Return, Qt.Key_Enter):
            r, c = self.table.currentRow(), self.table.currentColumn()
            if self.table.state() == QTableWidget.EditingState:
                self.table.setFocus()  # commits the editor
            self.table.setCurrentCell(min(r + 1, ROWS - 1), c)
            return
        super().keyPressEvent(e)

    def show_status(self, msg):
        self.status.setText(msg)
        from PyQt5.QtCore import QTimer
        QTimer.singleShot(2000, lambda: self.status.setText(""))

    def get_data(self):
        return [[self.table.item(r, c).text() for c in range(COLS)]
                for r in range(ROWS)]

    def save(self):
        self.table.setFocus()  # commit any open editor
        with open(SAVE_FILE, "w", encoding="utf-8") as f:
            json.dump(self.get_data(), f)
        self.show_status("Saved!")

    def load(self):
        if not os.path.exists(SAVE_FILE):
            return
        try:
            with open(SAVE_FILE, encoding="utf-8") as f:
                data = json.load(f)
            for r in range(ROWS):
                for c in range(COLS):
                    self.table.item(r, c).setText(data[r][c])
        except (ValueError, IndexError, OSError):
            pass

    def clear_all(self):
        if QMessageBox.question(self, "Clear All", "Clear all cells?") != QMessageBox.Yes:
            return
        for r in range(ROWS):
            for c in range(COLS):
                self.table.item(r, c).setText("")
        if os.path.exists(SAVE_FILE):
            os.remove(SAVE_FILE)
        self.table.setCurrentCell(0, 0)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    win = ExcelGrid()
    win.show()
    sys.exit(app.exec_())