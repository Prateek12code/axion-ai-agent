import json, os, math
from datetime import datetime

CH_KEYS = ["A","B","C","D","E","F","G","H","I","J","K","L","R","S","T","U","V","W"]

def clamp(x,a,b):
    return a if x < a else b if x > b else x

def safe_float(x, d=0.0):
    try:
        return float(x)
    except:
        return d

def parse_scan(path):
    raw = open(path, "r", encoding="utf-8", errors="ignore").read().strip()
    obj = json.loads(raw)
    scan_id = obj.get("scan_id") or os.path.basename(path).split(".")[0]
    ch = obj.get("channels", {})
    channels = {k: safe_float(ch.get(k, 0.0)) for k in CH_KEYS}
    meta = obj.get("meta", {})
    return scan_id, channels, meta

def features(ch):
    w = ch.get("W", 1.0) + 1.0
    r = ch.get("R", 1.0) + 1.0
    v = ch.get("V", 1.0) + 1.0
    a = ch.get("A", 1.0) + 1.0
    s = ch.get("S", 1.0) + 1.0
    t = ch.get("T", 1.0) + 1.0
    u = ch.get("U", 1.0) + 1.0
    return {
        "wr": w / r,
        "av": a / v,
        "ws": w / s,
        "tu": t / u,
        "energy": sum(ch.values()) / max(1.0, len(ch))
    }

def predict(feat):
    hb = 10.1 + 5.2 * clamp(feat["av"], 0.6, 1.5)
    spo2 = 91.5 + 7.5 * clamp(1.25 - (feat["wr"] - 1.0), 0.0, 1.0)
    glucose = 85.0 + 70.0 * clamp(feat["ws"] - 0.78, 0.0, 1.0)
    hydration = 38.0 + 28.0 * clamp(1.28 - feat["ws"], 0.0, 1.0)
    return {
        "Hb": round(clamp(hb, 8.0, 18.0), 2),
        "SpO2": round(clamp(spo2, 85.0, 100.0), 2),
        "GlucoseTrend": round(clamp(glucose, 70.0, 180.0), 2),
        "Hydration": round(clamp(hydration, 30.0, 70.0), 2)
    }

def label(name, v):
    if name == "Hb":
        if v < 11.5: return "Low"
        if v > 16.5: return "High"
        return "Good"
    if name == "SpO2":
        if v < 92.0: return "Low"
        return "Good"
    if name == "GlucoseTrend":
        if v < 85.0: return "Low"
        if v > 140.0: return "High"
        return "Good"
    if name == "Hydration":
        if v < 40.0: return "Low"
        if v > 65.0: return "High"
        return "Good"
    return "Good"

def labels(metrics):
    return {k: label(k, metrics[k]) for k in metrics}

def confidence(feat):
    e = feat["energy"]
    w = feat["wr"]
    av = feat["av"]
    score = 0.55
    score += 0.2 * clamp((e - 700) / 1600, 0.0, 1.0)
    score += 0.15 * (1.0 - clamp(abs(w - 1.05) / 0.6, 0.0, 1.0))
    score += 0.10 * (1.0 - clamp(abs(av - 1.00) / 0.6, 0.0, 1.0))
    return round(clamp(score, 0.15, 0.98), 2)

def alerts(lbl):
    a = []
    if lbl["SpO2"] == "Low": a.append("Low Oxygen")
    if lbl["Hb"] == "Low": a.append("Risk of Anemia")
    if lbl["Hydration"] == "Low": a.append("Monitor Hydration")
    if lbl["GlucoseTrend"] == "High": a.append("Glucose Trend High")
    return a

def render_card(scan_id, src, metrics, lbl, conf, alerts_list, trend):
    lines = []
    lines.append("AXION AI V2 — Spectral Intelligence (Software Prototype)")
    lines.append(f"Scan: {scan_id}")
    lines.append(f"Source: {src}")
    lines.append(f"Confidence: {conf}")
    lines.append("")
    keys = ["Hb","SpO2","GlucoseTrend","Hydration"]
    for k in keys:
        lines.append(f"{k}: {metrics[k]}  [{lbl[k]}]")
    lines.append("")
    if alerts_list:
        lines.append("Alerts:")
        for x in alerts_list:
            lines.append(f"- {x}")
    else:
        lines.append("Alerts: None")
    if trend:
        lines.append("")
        lines.append("Trend:")
        for t in trend:
            lines.append(t)
    return "\n".join(lines)