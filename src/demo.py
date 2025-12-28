import time, json, os, random, argparse
from live_store import ensure, list_scans, is_new_or_updated, mark_processed, append_history, last_rows, INBOX_DIR, now_iso
from pipeline import parse_scan, features, predict, labels, confidence, alerts, render_card
from agent import summary, trend_lines

def gen_scan(out_name=None, seed=None):
    ensure()
    if seed is not None:
        random.seed(seed)
    base = random.uniform(1100, 2400)
    def n(): return random.uniform(-140, 140)
    keys = ["A","B","C","D","E","F","G","H","I","J","K","L","R","S","T","U","V","W"]
    ch = {k: max(200, min(4095, base + n() + random.uniform(-120, 120))) for k in keys}
    ch["W"] = max(200, min(4095, ch["W"] + random.uniform(0, 260)))
    ch["A"] = max(200, min(4095, ch["A"] + random.uniform(-180, 180)))
    scan_id = f"scan_{int(time.time())}"
    obj = {"scan_id": scan_id, "channels": ch, "meta": {"mode": "demo_generated"}}
    name = out_name or f"{scan_id}.json"
    path = os.path.join(INBOX_DIR, name)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(obj, f, indent=2)
    return path

def process_file(path):
    scan_id, ch, meta = parse_scan(path)
    feat = features(ch)
    metrics = predict(feat)
    lbl = labels(metrics)
    conf = confidence(feat)
    al = alerts(lbl)
    hist = last_rows(4)
    trend = trend_lines(hist)
    summ = summary(metrics, lbl, conf)

    ts = now_iso()
    append_history([
        ts, scan_id, os.path.basename(path),
        metrics["Hb"], metrics["SpO2"], metrics["GlucoseTrend"], metrics["Hydration"],
        lbl["Hb"], lbl["SpO2"], lbl["GlucoseTrend"], lbl["Hydration"],
        ", ".join(al) if al else "None",
        summ
    ])
    card = render_card(scan_id, os.path.basename(path), metrics, lbl, conf, al, trend)
    return card, summ

def live(poll=1.0):
    ensure()
    print("\nAXION AI V2 — Live Spectral Demo")
    print(f"Drop scan JSONs into ./{INBOX_DIR}/")
    print("Commands in another terminal: python -m src.demo gen\n")
    while True:
        for p in list_scans():
            ok, key, mt = is_new_or_updated(p)
            if ok:
                card, summ = process_file(p)
                mark_processed(key, mt)
                print(card)
                print("")
                print("Agent Summary:")
                print(summ)
                print("\n" + "-"*64 + "\n")
        time.sleep(poll)

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("cmd", choices=["live","gen","once","init"])
    ap.add_argument("--poll", type=float, default=1.0)
    ap.add_argument("--file", type=str, default="")
    ap.add_argument("--seed", type=int, default=None)
    args = ap.parse_args()

    if args.cmd == "init":
        ensure()
        starter = os.path.join(INBOX_DIR, "DROP_SCANS_HERE.txt")
        if not os.path.exists(starter):
            open(starter, "w", encoding="utf-8").write("Drop AS7265X-style JSON scans here.\n")
        print("Initialized.")
        return

    if args.cmd == "gen":
        p = gen_scan(seed=args.seed)
        print(p)
        return

    if args.cmd == "once":
        ensure()
        if not args.file or not os.path.exists(args.file):
            print("Use: python -m src.demo once --file inbox_scans/<scan>.json")
            return
        card, summ = process_file(args.file)
        print(card)
        print("\nAgent Summary:\n" + summ)
        return

    if args.cmd == "live":
        live(poll=args.poll)

if __name__ == "__main__":
    main()