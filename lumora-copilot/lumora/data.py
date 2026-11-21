import json, pathlib
ROOT = pathlib.Path(__file__).resolve().parent.parent
DATA = ROOT / "data"

def load(name):
    p = DATA / name
    return json.loads(p.read_text()) if p.suffix == ".json" else p.read_text()

TICKETS = load("tickets.json")
SCORECARD_SET = TICKETS[:20]   # T001-T020: re-run after each chapter
EVAL_SET = TICKETS             # all 40: the final evaluation
FACTS = load("company_facts.md")
GUIDE = load("labeling_guide.md")
MANUAL = load("manual.md")
CUSTOMERS = load("customers.json")
SLOTS = load("slots.json")
