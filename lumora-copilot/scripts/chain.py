"""Chapter 9: prompt chaining. triage -> extract -> draft -> check -> fix, each step small and testable."""
import _path  # noqa: F401
import json, re, sys
from lumora.llm import ask, spend
from lumora.data import FACTS
from lumora.prompts import SYSTEM_FEW, SCHEMA, BRAND_VOICE, BY_ID, v3, ticket_text
from lumora.score import run_parallel

def step_triage(t):
    return json.loads(ask(v3(t), system=SYSTEM_FEW, tag="chain", output_config={"format": {"type": "json_schema", "schema": SCHEMA}}))

EXTRACT_SCHEMA = {"type": "object", "additionalProperties": False,
                  "required": ["customer_name", "invoice_numbers", "amounts_usd", "dates_or_deadlines", "customer_wants"],
                  "properties": {"customer_name": {"type": "string"}, "invoice_numbers": {"type": "array", "items": {"type": "string"}},
                                 "amounts_usd": {"type": "array", "items": {"type": "number"}},
                                 "dates_or_deadlines": {"type": "array", "items": {"type": "string"}}, "customer_wants": {"type": "string"}}}
def step_extract(t):
    return json.loads(ask(f"Extract the key facts from this ticket.\n<ticket>\n{ticket_text(t)}\n</ticket>", tag="chain",
                          output_config={"format": {"type": "json_schema", "schema": EXTRACT_SCHEMA}}))

WRITER = "You write Lumora Solar support replies.\n<facts>\n" + FACTS + "\n</facts>\n" + BRAND_VOICE
def step_draft(t, tri, facts):
    return ask(f"<triage>{json.dumps(tri)}</triage>\n<extracted>{json.dumps(facts)}</extracted>\n<ticket>\n{ticket_text(t)}\n</ticket>\n"
               "Write the reply email to the customer. Follow company policy exactly.", system=WRITER, tag="chain", max_tokens=500)

CHECK_SCHEMA = {"type": "object", "additionalProperties": False,
                "required": ["problems", "facts_correct", "no_unsupported_promises", "safety_first_if_needed"],
                "properties": {"problems": {"type": "array", "items": {"type": "string"}, "description": "only real errors, at most 3 short items; empty if none"},
                               "facts_correct": {"type": "boolean", "description": "false only if a number, time limit or policy in the reply contradicts <facts>"},
                               "no_unsupported_promises": {"type": "boolean", "description": "false only if the reply commits to something <facts> does not allow"},
                               "safety_first_if_needed": {"type": "boolean", "description": "true if there is no safety sign, or if safety advice comes first"}}}
def body_words(reply):   # words between the greeting and the sign-off
    lines = [l for l in reply.strip().splitlines() if l.strip() and not l.lower().startswith(("subject:", "dear", "hi ", "hello"))]
    lines = [l for l in lines if not re.match(r"^(kind|warm|best)? ?regards|^lumora", l.strip().lower())]
    return len(" ".join(lines).split())
def step_check(t, reply):   # the reviewer thinks briefly (adaptive thinking, low effort) before it fills in the booleans
    llm = json.loads(ask(f"<ticket>\n{ticket_text(t)}\n</ticket>\n<reply>\n{reply}\n</reply>\nReview the reply against <facts>. Report only real errors, not style or omissions.",
                         system="You are Lumora's QA reviewer.\n<facts>\n" + FACTS + "\n</facts>", tag="chain", thinking=None, effort="low", max_tokens=3000,
                         output_config={"format": {"type": "json_schema", "schema": CHECK_SCHEMA}}))
    checks = {"facts": llm["facts_correct"], "promises": llm["no_unsupported_promises"], "safety": llm["safety_first_if_needed"],
              "<=90 words": body_words(reply) <= 90, "no '!'": "!" not in reply}   # the last two are checked in code
    return checks, llm["problems"]
def step_fix(t, reply, problems):
    return ask(f"<ticket>\n{ticket_text(t)}\n</ticket>\n<reply>\n{reply}\n</reply>\n<problems>\n" + "\n".join(problems) +
               "\n</problems>\nRewrite the reply to fix the problems. Body under 90 words, no exclamation marks, one next step. Output only the reply.",
               system=WRITER, tag="chain", max_tokens=500)

def full_chain(t, verbose=False):
    tri = step_triage(t); facts = step_extract(t); draft = step_draft(t, tri, facts)
    c1, probs = step_check(t, draft)
    if verbose:
        print("1 triage :", tri); print("2 extract:", facts); print("3 draft  :\n" + draft); print("4 check  :", c1)
    if all(c1.values()):
        return t["id"], True, True
    fixed = step_fix(t, draft, probs + [f"failed check: {k}" for k, v in c1.items() if not v])
    c2, _ = step_check(t, fixed)
    if verbose:
        print("5 fixed  :\n" + fixed); print("6 check  :", c2)
    return t["id"], False, all(c2.values())

if __name__ == "__main__":
    if len(sys.argv) > 1:                       # python scripts/chain.py T002  -> show every step for one ticket
        full_chain(BY_ID[sys.argv[1]], verbose=True)
    else:                                       # python scripts/chain.py       -> run 8 tickets and count passes
        ids = ["T002", "T003", "T007", "T013", "T016", "T018", "T022", "T024"]
        res = run_parallel(full_chain, [BY_ID[i] for i in ids], workers=8)
        for tid, first, final in res:
            print(f"{tid}: passes all checks first time: {first!s:<5} | after fix step: {final}")
        print(f"replies passing every check: {sum(r[1] for r in res)}/{len(res)} -> {sum(r[2] for r in res)}/{len(res)}")
    print(f"cost ${spend('chain')['usd']:.4f}")
