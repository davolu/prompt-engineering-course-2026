# Ticket labelling guide (ground truth for the scorecard)

category (exactly one):
- quote: asks for a price, sizing, savings or a new system / add-on
- billing: invoices, charges, payments, refunds, disputes
- scheduling: booking, moving or cancelling a site survey, installation or technician visit
- technical_fault: something on an installed system is not working, an error code, low output, safety signs
- app_account: monitoring app, Wi-Fi setup, login, contact details, account changes

urgency:
- urgent: any safety sign (burning smell, smoke, sparks, hot inverter casing) or error E21 ISOLATION FAULT
- normal: something is broken, money is disputed or owed, or a date is at risk
- low: questions and information requests with nothing broken

needs_human (true/false): true if ANY of: urgency is urgent; a refund or billing dispute; a cancellation or reschedule inside 72 hours of installation; the customer threatens to leave, complain publicly or take legal action. Otherwise false.

If a ticket mentions several things, label the main request (what the customer needs done first); safety always wins.
