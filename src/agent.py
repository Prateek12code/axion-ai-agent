def summary(metrics, labels, conf):
    s = []
    if labels.get("SpO2") == "Low":
        s.append("SpO2 appears low — recheck and compare with last scans.")
    if labels.get("Hb") == "Low":
        s.append("Hb trend indicates possible low hemoglobin — focus on trend tracking.")
    if labels.get("Hydration") == "Low":
        s.append("Hydration indicator is low — monitor hydration trend.")
    if labels.get("GlucoseTrend") == "High":
        s.append("Glucose trend appears high — verify with repeat scans and compare history.")
    if not s:
        s.append("Status looks stable — keep monitoring and compare trends.")
    s.append(f"System confidence: {conf}")
    return " ".join(s)

def trend_lines(history_rows):
    out = []
    for r in history_rows:
        out.append(f"{r['ts']} | Hb {r['Hb']}({r['Label_Hb']}) | SpO2 {r['SpO2']}({r['Label_SpO2']})")
    return out[-3:]