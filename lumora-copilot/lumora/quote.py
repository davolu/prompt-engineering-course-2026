"""Ground truth for quote questions, computed in code from the company facts."""
PANEL, KIT, HX5, HX8, BATTERY = 210, 95, 1150, 1690, 3400
KWH_PER_PANEL, PRICE_KWH = 450 * 4.5 * 365 * 0.8 / 1000, 0.18   # 591.3 kWh

def quote(panels, batteries=0):
    if panels > 18:
        return {"needs_survey": True}
    inverter = HX5 if panels <= 11 else HX8
    equipment = panels * PANEL + inverter + batteries * BATTERY + panels * KIT
    discount = round(equipment * 0.05, 2) if panels >= 10 else 0
    labour = 900 + 40 * panels
    total = round(equipment - discount + labour, 2)
    kwh = KWH_PER_PANEL * panels
    savings = round(kwh * PRICE_KWH, 2)
    return {"inverter": "HX5" if inverter == HX5 else "HX8", "equipment": equipment, "discount": discount,
            "labour": labour, "total": total, "annual_kwh": round(kwh), "annual_savings": savings,
            "payback_years": round(total / savings, 1)}

QUESTIONS = [  # (question, panels, batteries)
    ("We want a dozen panels and one battery. What's the total installed price?", 12, 1),
    ("Price for 8 panels, no battery, everything installed?", 8, 0),
    ("I'd like one fewer than 11 panels plus a Cell-10 battery. Total?", 10, 1),
    ("Eleven panels, no battery. What do I pay in total?", 11, 0),
    ("Quote for 9 panels and a battery please, all in.", 9, 1),
    ("We need 18 panels and two batteries. Total price?", 18, 2),
    ("6 panels for my shop roof, no battery. Total cost installed?", 6, 0),
    ("Half of 28 panels, with one battery. What's the total?", 14, 1),
    ("13 panels, no battery. Total, including any discount?", 13, 0),
    ("Two rows of 8 panels and no battery. Total installed price?", 16, 0),
]

def answers():
    return [quote(p, b)["total"] for _, p, b in QUESTIONS]
