"""Crew-scheduling puzzle for the Tree of Thoughts chapter, with a code verifier."""
CREWS = ["A", "B", "C"]
SLOTS = ["morning", "midday", "afternoon"]
JOBS = {
    "J1": {"type": "fault",   "area": "Northgate", "note": "URGENT safety call-out, must be a morning slot"},
    "J2": {"type": "battery", "area": "Riverside", "note": "battery job"},
    "J3": {"type": "install", "area": "Westbrook", "note": ""},
    "J4": {"type": "battery", "area": "Northgate", "note": "battery job"},
    "J5": {"type": "survey",  "area": "Hillcrest", "note": "same street as J6"},
    "J6": {"type": "survey",  "area": "Hillcrest", "note": "same street as J5"},
    "J7": {"type": "install", "area": "Old Mill",  "note": "customer only available in the afternoon"},
}
RULES = """1. Each crew does at most one job per slot (morning, midday, afternoon). Every job gets exactly one crew and slot.
2. Battery jobs (J2, J4) need a battery-certified crew: only crews B and C are certified.
3. J1 is urgent and must be in a morning slot.
4. J7 must be in the afternoon.
5. J5 and J6 are on the same street, so they must be done by the same crew in consecutive slots.
6. Crew A cannot work in the afternoon (training).
7. No crew may go Westbrook -> Northgate or Northgate -> Westbrook in consecutive slots (40 minutes apart)."""

def check(plan):
    """plan: dict job -> (crew, slot). Returns list of rule violations (empty list = valid)."""
    v = []
    if set(plan) != set(JOBS):
        v.append(f"jobs assigned {sorted(plan)} != {sorted(JOBS)}")
    used = {}
    for j, (c, s) in plan.items():
        if c not in CREWS or s not in SLOTS:
            v.append(f"{j}: bad crew/slot {c}/{s}"); continue
        if (c, s) in used: v.append(f"rule 1: crew {c} double-booked in {s} ({used[(c,s)]}, {j})")
        used[(c, s)] = j
        if JOBS[j]["type"] == "battery" and c not in "BC": v.append(f"rule 2: {j} needs crew B or C")
        if c == "A" and s == "afternoon": v.append(f"rule 6: crew A busy in afternoon ({j})")
    if "J1" in plan and plan["J1"][1] != "morning": v.append("rule 3: J1 not in the morning")
    if "J7" in plan and plan["J7"][1] != "afternoon": v.append("rule 4: J7 not in the afternoon")
    if "J5" in plan and "J6" in plan:
        (c5, s5), (c6, s6) = plan["J5"], plan["J6"]
        if c5 != c6 or abs(SLOTS.index(s5) - SLOTS.index(s6)) != 1 if s5 in SLOTS and s6 in SLOTS else True:
            v.append("rule 5: J5 and J6 not same crew in consecutive slots")
    for c in CREWS:
        seq = [used.get((c, s)) for s in SLOTS]
        for a, b in zip(seq, seq[1:]):
            if a and b and {JOBS[a]["area"], JOBS[b]["area"]} == {"Westbrook", "Northgate"}:
                v.append(f"rule 7: crew {c} goes {JOBS[a]['area']} -> {JOBS[b]['area']}")
    return v

def partial_ok(plan):
    """Checks only the rules that can already be broken by a partial plan."""
    return [x for x in check(plan) if not x.startswith("jobs assigned")
            and not (x.startswith("rule 5") and not ("J5" in plan and "J6" in plan))]
