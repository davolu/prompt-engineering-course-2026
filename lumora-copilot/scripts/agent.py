"""Chapter 11: tool use. The model asks for tools, our code runs them, and booking needs a human's approval."""
import _path  # noqa: F401
import json, sys
from lumora.llm import ask, spend
from lumora.tools import TOOLS, FUNCS

SYSTEM = "You are Lumora's booking assistant. Today is 2026-11-23. Use tools; never invent data."

def agent(user_msg, approve=False, max_turns=8):
    msgs = [{"role": "user", "content": user_msg}]
    for _ in range(max_turns):
        r = ask(messages=msgs, system=SYSTEM, tools=TOOLS, tag="agent", raw=True, max_tokens=800)
        msgs.append({"role": "assistant", "content": r.content})
        for b in r.content:
            if b.type == "text" and b.text.strip():
                print("assistant:", b.text.strip())
        calls = [b for b in r.content if b.type == "tool_use"]
        if not calls:
            return
        results = []
        for c in calls:
            args = dict(c.input)
            if c.name == "create_ticket" and approve:
                args["approved_by_human"] = True        # the human-in-the-loop switch
            out = json.dumps(FUNCS[c.name](**args))
            print(f"  -> {c.name}({c.input}) = {out[:160]}")
            results.append({"type": "tool_result", "tool_use_id": c.id, "content": out})
        msgs.append({"role": "user", "content": results})

if __name__ == "__main__":
    ask_msg = "Hi, I'm customer C1006. My inverter shows E17. Please book a technician on the first free day this week, any window."
    if "--approve" in sys.argv:
        agent(ask_msg + " Yes, I confirm: book the first free slot, no need to ask me again.", approve=True)
    else:
        agent(ask_msg)
    print(f"cost ${spend('agent')['usd']:.4f}")
