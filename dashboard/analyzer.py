from collections import Counter
from datetime import datetime
import pandas as pd

def analyze_file(file_path):
    level_counts = Counter()
    component_counts = Counter()
    service_counts = Counter()
    error_messages = Counter()
    error_counts_by_component = Counter()
    timeline = Counter()

    # ✅ Read Excel ONLY
    try:
        df = pd.read_excel(file_path)
    except Exception as e:
        print("Excel read error:", e)
        return {"levels": {}, "error": "Invalid Excel file"}

    # 🔥 Debug once (optional)
    print("Columns:", df.columns)

    # ✅ Ensure correct column exists
    if "@message" not in df.columns:
        return {"levels": {}, "error": "@message column missing"}

    for _, row in df.iterrows():
        message = row["@message"]

        if pd.isna(message):
            continue

        message = str(message).strip()

        parts = [p.strip() for p in message.split("|")]

        if len(parts) < 5:
            continue

        timestamp, level, component, service, msg = parts[:5]

        # counts
        level_counts[level] += 1
        component_counts[component] += 1
        service_counts[service] += 1

        if level == "ERROR":
            error_messages[msg] += 1
            error_counts_by_component[component] += 1

        # timeline
        try:
            ts = timestamp.split(",")[0]
            dt = datetime.strptime(ts, "%Y-%m-%d %H:%M:%S")
            minute = dt.strftime("%Y-%m-%d %H:%M")
            timeline[minute] += 1
        except:
            pass

    if not level_counts:
        return {"levels": {}}

    error_rate_per_component = {}
    for comp in component_counts:
        total = component_counts[comp]
        errors = error_counts_by_component.get(comp, 0)
        error_rate_per_component[comp] = round((errors / total) * 100, 2) if total else 0

    return {
        "levels": dict(level_counts),
        "components": dict(component_counts),
        "services": dict(service_counts),
        "timeline": dict(sorted(timeline.items())),
        "top_errors": dict(error_messages.most_common(5)),
        "error_rate_per_component": error_rate_per_component
    }