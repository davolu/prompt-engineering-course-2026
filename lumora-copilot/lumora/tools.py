"""Fake Lumora back-office tools for the ReAct / tool-use chapter."""
import json
from .data import CUSTOMERS, SLOTS

CREATED = []

def get_customer(customer_id):
    for c in CUSTOMERS:
        if c["customer_id"] == customer_id:
            return c
    return {"error": f"customer {customer_id} not found"}

def get_install_slots(date=None, slot_type="technician_visit"):
    return [s for s in SLOTS if s["available"] and s["type"] == slot_type and (date is None or s["date"] == date)]

def create_ticket(customer_id, summary, slot_date, slot_window, approved_by_human=False):
    if not approved_by_human:
        return {"status": "pending_approval", "message": "A human must approve this booking before it is created."}
    t = {"ticket": f"LUM-{5000 + len(CREATED)}", "customer_id": customer_id, "summary": summary, "slot": f"{slot_date} {slot_window}"}
    CREATED.append(t)
    return {"status": "created", **t}

TOOLS = [
    {"name": "get_customer", "description": "Look up a Lumora customer by id (like C1004). Returns name, system (panels, inverter, battery), install date and open invoices.",
     "input_schema": {"type": "object", "properties": {"customer_id": {"type": "string"}}, "required": ["customer_id"]}},
    {"name": "get_install_slots", "description": "List free 2-hour slots. slot_type is 'technician_visit' or 'site_survey'. date is YYYY-MM-DD, optional.",
     "input_schema": {"type": "object", "properties": {"date": {"type": "string"}, "slot_type": {"type": "string", "enum": ["technician_visit", "site_survey"]}}, "required": ["slot_type"]}},
    {"name": "create_ticket", "description": "Book a visit in a free slot. Only call after checking slots. If the result is pending_approval, tell the customer a team member must approve it; if it is created, the booking is confirmed.",
     "input_schema": {"type": "object", "properties": {"customer_id": {"type": "string"}, "summary": {"type": "string"}, "slot_date": {"type": "string"}, "slot_window": {"type": "string"}},
                      "required": ["customer_id", "summary", "slot_date", "slot_window"]}},
]
FUNCS = {"get_customer": get_customer, "get_install_slots": get_install_slots, "create_ticket": create_ticket}

def run_tool(name, args):
    return json.dumps(FUNCS[name](**args))
