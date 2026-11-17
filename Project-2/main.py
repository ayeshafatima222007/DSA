"""
main.py
-------
Start the Solitaire application.

Run from the project folder:
    python main.py
"""

import sys

from PyQt6.QtWidgets import QApplication

from UI.main_window import MainWindow


def main():
    app = QApplication(sys.argv)     # every PyQt program needs exactly one QApplication
    window = MainWindow()
    window.show()
    sys.exit(app.exec())             # start the event loop (waits for clicks, timers...)


if __name__ == "__main__":
    main()