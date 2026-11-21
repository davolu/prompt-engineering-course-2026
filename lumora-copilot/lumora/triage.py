"""Run a triage prompt over the 20-ticket scorecard set and score it."""
from .llm import ask, HAIKU, spend
from .data import SCORECARD_SET
from .score import run_parallel, loose_json, parse_json, triage_score

def ticket_text(t):
    return f"Subject: {t['subject']}\nCustomer: {t['customer_id']}\n\n{t['body']}"

def run_triage(build_prompt, *, system=None, model=HAIKU, tag="triage", strict=False, tickets=None, max_tokens=300, **kw):
    """build_prompt(ticket) -> user prompt string. Returns (score dict, predictions)."""
    tickets = tickets or SCORECARD_SET
    def one(t):
        out = ask(build_prompt(t), system=system, model=model, tag=tag, max_tokens=max_tokens, **kw)
        return (parse_json(out) if strict else loose_json(out)), out
    res = run_parallel(one, tickets)
    preds = [p for p, _ in res]
    s = triage_score(preds, tickets)
    s["cost_usd"] = spend(tag)["usd"]
    return s, preds, [o for _, o in res]

def show(s, label=""):
    print(f"{label:<28} all 3 fields right: {s['all_correct']} ({s['all_correct_pct']}%)  | category {s['category_acc']}%  urgency {s['urgency_acc']}%  needs_human {s['needs_human_acc']}%  | valid JSON {s['valid_json']}")
    if s["misses"]:
        print(f"{'':<28} misses: {', '.join(s['misses'])}")
