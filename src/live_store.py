import os, json, csv
from datetime import datetime

INBOX_DIR = "inbox_scans"
STATE_JSON = "state.json"
HISTORY_CSV = "history.csv"

def now_iso():
    return datetime.utcnow().replace(microsecond=0).isoformat() + "Z"

def ensure():
    os.makedirs(INBOX_DIR, exist_ok=True)
    if not os.path.exists(STATE_JSON):
        with open(STATE_JSON, "w", encoding="utf-8") as f:
            json.dump({"processed": {}}, f, indent=2)
    if not os.path.exists(HISTORY_CSV):
        with open(HISTORY_CSV, "w", newline="", encoding="utf-8") as f:
            w = csv.writer(f)
            w.writerow(["ts","scan_id","file","Hb","SpO2","GlucoseTrend","Hydration","Label_Hb","Label_SpO2","Label_GlucoseTrend","Label_Hydration","Alerts","Summary"])

def load_state():
    with open(STATE_JSON, "r", encoding="utf-8") as f:
        return json.load(f)

def save_state(st):
    with open(STATE_JSON, "w", encoding="utf-8") as f:
        json.dump(st, f, indent=2)

def list_scans():
    ensure()
    files = []
    for name in os.listdir(INBOX_DIR):
        p = os.path.join(INBOX_DIR, name)
        if os.path.isfile(p) and name.lower().endswith(".json"):
            files.append(p)
    files.sort(key=lambda x: os.path.getmtime(x))
    return files

def mark_processed(filename, mtime):
    st = load_state()
    st["processed"][filename] = mtime
    save_state(st)

def is_new_or_updated(path):
    st = load_state()
    key = os.path.basename(path)
    mt = os.path.getmtime(path)
    last = st["processed"].get(key, 0)
    return mt > last, key, mt

def append_history(row):
    ensure()
    with open(HISTORY_CSV, "a", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(row)

def last_rows(n=5):
    if not os.path.exists(HISTORY_CSV):
        return []
    with open(HISTORY_CSV, "r", newline="", encoding="utf-8") as f:
        rows = list(csv.DictReader(f))
    return rows[-n:]