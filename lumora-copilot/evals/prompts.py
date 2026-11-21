"""Prompt functions for Promptfoo. Each gets the test vars and returns the prompt text."""
import json, pathlib, sys
ROOT = pathlib.Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from jinja2 import Template
from lumora.data import GUIDE, TICKETS

BY_ID = {t["id"]: t for t in TICKETS}
FEW = ["T023", "T037", "T021", "T030", "T031", "T022"]   # never from the 20-ticket scorecard set

def ticket_text(t):
    return f"Subject: {t['subject']}\nCustomer: {t['customer_id']}\n\n{t['body']}"

def example(tid):
    x = BY_ID[tid]; lab = x["label"]
    return (f'<example>\n<ticket>\n{ticket_text(x)}\n</ticket>\n<answer>{{"category": "{lab["category"]}", '
            f'"urgency": "{lab["urgency"]}", "needs_human": {str(lab["needs_human"]).lower()}}}</answer>\n</example>')

def v0(context):
    t = BY_ID[context["vars"]["ticket_id"]]
    return f"Classify this customer support ticket. Return JSON with category, urgency and needs_human.\n\n{ticket_text(t)}"

def v6(context):
    t = BY_ID[context["vars"]["ticket_id"]]
    tpl = Template((ROOT / "prompts" / "triage_v6.md").read_text())
    return tpl.render(company="Lumora Solar", guide=GUIDE, examples=[example(i) for i in FEW], ticket=ticket_text(t))
