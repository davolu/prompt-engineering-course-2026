"""Scoring helpers. Every number on screen comes from these functions."""
import json, re
from concurrent.futures import ThreadPoolExecutor

FIELDS = ("category", "urgency", "needs_human")

def parse_json(text):
    """Strict parse first; return None if the reply is not valid JSON."""
    try:
        return json.loads(text)
    except Exception:
        return None

def loose_json(text):
    """Find the first {...} block, for prompts that don't force JSON."""
    m = re.search(r"\{.*\}", text or "", re.S)
    return parse_json(m.group(0)) if m else None

def triage_score(preds, tickets):
    """preds: list of dicts (or None). Returns per-field accuracy and all-correct rate."""
    n = len(tickets)
    res = {f: 0 for f in FIELDS}; exact = 0; valid = 0; misses = []
    for p, t in zip(preds, tickets):
        ok_all = True
        if isinstance(p, dict):
            valid += 1
        for f in FIELDS:
            ok = isinstance(p, dict) and str(p.get(f)).lower() == str(t["label"][f]).lower()
            res[f] += ok; ok_all &= ok
        exact += ok_all
        if not ok_all:
            misses.append(t["id"])
    out = {f"{f}_acc": round(res[f] / n * 100) for f in FIELDS}
    out.update(all_correct=f"{exact}/{n}", all_correct_pct=round(exact / n * 100), valid_json=f"{valid}/{n}", misses=misses)
    return out

def run_parallel(fn, items, workers=8):
    with ThreadPoolExecutor(workers) as ex:
        return list(ex.map(fn, items))

SCORECARD = {}  # chapter -> headline metric, filled in as we go

def record(chapter, metric, value):
    SCORECARD.setdefault(chapter, {})[metric] = value
    return None

def show_scorecard():
    print(f"{'Chapter':<26}{'Metric':<58}Value")
    for ch, m in SCORECARD.items():
        for k, v in m.items():
            print(f"{ch:<26}{k:<58}{v}")
