import csv              #csv.DictReader,csv.DictWriter
import json             #json.load(f),json.dump(..)
import os               #os.path.exists(..)
import threading        #threading.Event()
import time             #time.sleep(..)
from urllib.parse import urlparse, parse_qsl      #to break URL into parts

import requests         #requests.get(..)
from PyQt5.QtCore import QThread, pyqtSignal

CSV_FILE = "articles.csv"
STATE_FILE = "scrape_state.json"
API = "https://api.crossref.org/works"
MAILTO = "2025cs341@student.edu.pk"  #Crossref polite pool
FIELDS = ["doi", "title", "journal", "publisher", "year", "type",
          "citations", "references", "author_count", "first_author", "language"]
SELECT = ("DOI,title,container-title,publisher,issued,type,"
          "is-referenced-by-count,references-count,author,language")


def parse_item(it):
    title = (it.get("title") or [""])[0].strip()    #get title or empty title in list,gives 1st element,and strip=removes extra spaces

    journal = (it.get("container-title") or [""])[0].strip()

    parts = (it.get("issued") or {}).get("date-parts") or [[None]]    #get("date-parts") gives year,month,date
    if parts and parts[0]:
        year = parts[0][0]
    else:
        year = None

    if not (title and journal and year and it.get("DOI")):
        return None
    
    authors = it.get("author") or []
    first = ""
    if authors:
        a = authors[0]
        first = (a.get("given", "") + " " + a.get("family", "")).strip() or a.get("name", "")
    return {
        "doi": it["DOI"],
        "title": title.replace("\n", " "),    #if new line then replace with space,\n breaks csv row
        "journal": journal,
        "publisher": it.get("publisher", ""),    #if no publisher ,empty text
        "year": int(year),
        "type": it.get("type", ""),      #only journal-article,no other type
        "citations": int(it.get("is-referenced-by-count", 0)),      #how much time this article is used on cites,if not then 0
        "references": int(it.get("references-count", 0)),          #how much refrences this article used
        "author_count": len(authors),     #No.of authors
        "first_author": first,
        "language": it.get("language", ""),
    }


def load_csv(path=CSV_FILE):
    #Return list of dict rows (numeric columns converted)

    if not os.path.exists(path):     #base case if file doesnot exists
        return []
    rows = []      #empty list that collects all rows 

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
    def _params(self):                  # no "select": full records are safe from invalid-field 400 errors
        p = {"rows": 1000, "mailto": MAILTO,
             "filter": "type:journal-article"}
        if self.url:
            q = dict(parse_qsl(urlparse(self.url).query))
            for k in ("cursor", "rows", "select"):         #loop runs for 3 times
                q.pop(k, None)       #try:del q[k]       except KeyError:pass
            p.update(q)
        return p

    def run(self):
        rows = load_csv()
        seen = {r["doi"] for r in rows}    #making set compression of each row
        #seen = set()   
        #for r in rows:  
        #   seen.add(r["doi"])
        cursor = "*"
        if os.path.exists(STATE_FILE) and not self.url:   #check if scrape_state.json exists or if user give URL

            try:     #use try except if during scrape any problem cause
                with open(STATE_FILE) as f:
                    cursor = json.load(f).get("cursor", "*")
                    #json.load(f)=converts whats in file into dictionary
                    #get("cursor", "*")= works like trigger
            except Exception:
                pass

        self.progress.emit(len(rows), self.target)   #for making the progress bar starts from where it left last time
        self.status.emit("Running")
        params = self._params()

        fails = 0   #initializing the fail count

        while len(rows) < self.target and not self._stop:     #this loop runs repeatedly and send request to cressref for 1000 articles

            self._run.wait()          # blocks while paused
            if self._stop:
                break

            params["cursor"] = cursor   #in every loop,cursor changes,so we add mark here

            try:
                resp = requests.get(API, params=params, timeout=60)    #send request to crossref and result store in response

                if resp.status_code == 400 and cursor != "*":
                    cursor = "*"      # saved cursor expired-start over
                    continue
                
                if resp.status_code >= 400:
                    raise RuntimeError(f"HTTP {resp.status_code}: {resp.text[:200]}")
                msg = resp.json()["message"]

                fails = 0      #no any if conditions haooens then fail count remains 0

            except Exception as e:
                fails += 1
                self.status.emit(f"Error ({fails}/5): {e}")

                if fails >= 5:     #limitation of fail count,and loop starts again
                    break
                time.sleep(3)
                continue

            items = msg.get("items", [])   #make list of articles from msg

            if not items:
                self.status.emit("No more results")
                break
            for it in items:
                r = parse_item(it)
                if r and r["doi"] not in seen:    #r not empty and no previous DOI match
                    seen.add(r["doi"])
                    rows.append(r)
                    if len(rows) >= self.target:
                        break

            cursor = msg.get("next-cursor", cursor)
            save_csv(rows)
            with open(STATE_FILE, "w") as f:
                json.dump({"cursor": cursor}, f)
            self.progress.emit(len(rows), self.target)    #progress bar increase as articles increase

        save_csv(rows)
        self.status.emit("Stopped" if self._stop else "Finished")
        self.done.emit(len(rows))