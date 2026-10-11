"""Crossref journal-article scraper with pause / resume / stop and progress.

Saves to articles.csv as it goes; cursor kept in scrape_state.json so a
stopped run can continue after restarting the app.

Standalone test (no GUI):  python scraper.py 2000
"""
import csv
import json
import os
import sys
import threading
import time
from urllib.parse import urlparse, parse_qsl

import requests
from PyQt5.QtCore import QThread, pyqtSignal

CSV_FILE = "articles.csv"
STATE_FILE = "scrape_state.json"
API = "https://api.crossref.org/works"
MAILTO = "2025cs341@student.edu.pk"  # change to your email (Crossref polite pool)
FIELDS = ["doi", "title", "journal", "publisher", "year", "type",
          "citations", "references", "author_count", "first_author", "language"]
SELECT = ("DOI,title,container-title,publisher,issued,type,"
          "is-referenced-by-count,references-count,author,language")


def parse_item(it):
    title = (it.get("title") or [""])[0].strip()
    journal = (it.get("container-title") or [""])[0].strip()
    parts = (it.get("issued") or {}).get("date-parts") or [[None]]
    year = parts[0][0] if parts and parts[0] else None
    if not (title and journal and year and it.get("DOI")):
        return None
    authors = it.get("author") or []
    first = ""
    if authors:
        a = authors[0]
        first = (a.get("given", "") + " " + a.get("family", "")).strip() or a.get("name", "")
    return {
        "doi": it["DOI"],
        "title": title.replace("\n", " "),
        "journal": journal,
        "publisher": it.get("publisher", ""),
        "year": int(year),
        "type": it.get("type", ""),
        "citations": int(it.get("is-referenced-by-count", 0)),
        "references": int(it.get("references-count", 0)),
        "author_count": len(authors),
        "first_author": first,
        "language": it.get("language", ""),
    }


def load_csv(path=CSV_FILE):
    """Return list of dict rows (numeric columns converted)."""
    if not os.path.exists(path):
        return []
    rows = []
    with open(path, newline="", encoding="utf-8") as f:
        for r in csv.DictReader(f):
            for k in ("year", "citations", "references", "author_count"):
                try:
                    r[k] = int(r[k])
                except (ValueError, KeyError):
                    r[k] = 0
            rows.append(r)
    return rows


def save_csv(rows, path=CSV_FILE):
    with open(path, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=FIELDS)
        w.writeheader()
        w.writerows(rows)


class ScraperWorker(QThread):
    progress = pyqtSignal(int, int)   # scraped so far, target
    status = pyqtSignal(str)
    done = pyqtSignal(int)            # total rows

    def __init__(self, target=15000, url=None, parent=None):
        super().__init__(parent)
        self.target = target
        self.url = url                # optional: custom Crossref URL (bonus)
        self._run = threading.Event()
        self._run.set()               # set = running, cleared = paused
        self._stop = False

    # --- controls ---
    def pause(self):
        self._run.clear()
        self.status.emit("Paused")

    def resume(self):
        self._run.set()
        self.status.emit("Running")

    def stop(self):
        self._stop = True
        self._run.set()               # release if paused

    # --- main loop ---
    def _params(self):
        # no "select": full records are safe from invalid-field 400 errors
        p = {"rows": 1000, "mailto": MAILTO,
             "filter": "type:journal-article"}
        if self.url:
            q = dict(parse_qsl(urlparse(self.url).query))
            for k in ("cursor", "rows", "select"):
                q.pop(k, None)
            p.update(q)
        return p

    def run(self):
        rows = load_csv()
        seen = {r["doi"] for r in rows}
        cursor = "*"
        if os.path.exists(STATE_FILE) and not self.url:
            try:
                with open(STATE_FILE) as f:
                    cursor = json.load(f).get("cursor", "*")
            except Exception:
                pass
        self.progress.emit(len(rows), self.target)
        self.status.emit("Running")
        params = self._params()
        fails = 0

        while len(rows) < self.target and not self._stop:
            self._run.wait()          # blocks while paused
            if self._stop:
                break
            params["cursor"] = cursor
            try:
                resp = requests.get(API, params=params, timeout=60)
                if resp.status_code == 400 and cursor != "*":
                    cursor = "*"      # saved cursor expired; start over
                    continue
                if resp.status_code >= 400:
                    raise RuntimeError(f"HTTP {resp.status_code}: {resp.text[:200]}")
                msg = resp.json()["message"]
                fails = 0
            except Exception as e:
                fails += 1
                self.status.emit(f"Error ({fails}/5): {e}")
                if fails >= 5:
                    break
                time.sleep(3)
                continue
            items = msg.get("items", [])
            if not items:
                self.status.emit("No more results")
                break
            for it in items:
                r = parse_item(it)
                if r and r["doi"] not in seen:
                    seen.add(r["doi"])
                    rows.append(r)
                    if len(rows) >= self.target:
                        break
            cursor = msg.get("next-cursor", cursor)
            save_csv(rows)
            with open(STATE_FILE, "w") as f:
                json.dump({"cursor": cursor}, f)
            self.progress.emit(len(rows), self.target)

        save_csv(rows)
        self.status.emit("Stopped" if self._stop else "Finished")
        self.done.emit(len(rows))


if __name__ == "__main__":
    # quick console test without opening a window
    n = int(sys.argv[1]) if len(sys.argv) > 1 else 2000
    from PyQt5.QtCore import QCoreApplication
    app = QCoreApplication([])
    w = ScraperWorker(target=n)
    w.progress.connect(lambda a, b: print(f"{a}/{b}"))
    w.status.connect(print)
    w.done.connect(lambda t: (print("rows:", t), app.quit()))
    w.start()
    app.exec_()