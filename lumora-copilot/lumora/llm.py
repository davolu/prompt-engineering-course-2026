"""One small wrapper around the Anthropic Messages API, with a cost ledger.

Prices are USD per 1M tokens from https://platform.claude.com/docs/en/about-claude/pricing
(checked 21 Nov 2026). Haiku 5.5 prices shown are for prompts up to 100K tokens.
"""
import time, anthropic

HAIKU = "claude-haiku-5-5"
SONNET = "claude-sonnet-5-5"

PRICES = {  # input, output, cache_write_5m, cache_read
    HAIKU: (0.10, 0.50, 0.125, 0.01),
    SONNET: (2.00, 10.00, 2.50, 0.10),
}
HAIKU_LONG = (0.50, 2.50, 0.625, 0.05)  # Haiku 5.5 prompts over 100K tokens

client = anthropic.Anthropic()  # reads ANTHROPIC_API_KEY from the environment
LEDGER = []  # one dict per call


def cost_of(model, usage):
    i, o, cw, cr = PRICES[model]
    prompt_len = usage.input_tokens + (usage.cache_creation_input_tokens or 0) + (usage.cache_read_input_tokens or 0)
    if model == HAIKU and prompt_len > 100_000:
        i, o, cw, cr = HAIKU_LONG
    return (usage.input_tokens * i + usage.output_tokens * o
            + (usage.cache_creation_input_tokens or 0) * cw
            + (usage.cache_read_input_tokens or 0) * cr) / 1e6


def ask(prompt=None, *, system=None, messages=None, model=HAIKU, max_tokens=1024,
        thinking=False, effort=None, tag="", raw=False, **kw):
    """Send one request. thinking=False turns adaptive thinking off (Haiku 5.5)."""
    if messages is None:
        messages = [{"role": "user", "content": prompt}]
    args = dict(model=model, max_tokens=max_tokens, messages=messages, **kw)
    if system is not None:
        args["system"] = system
    if thinking is False and model == HAIKU:
        args["thinking"] = {"type": "disabled"}
    elif isinstance(thinking, dict):
        args["thinking"] = thinking
    if effort:
        args.setdefault("output_config", {})["effort"] = effort
    t0 = time.time()
    r = client.messages.create(**args)
    dt = time.time() - t0
    LEDGER.append({"tag": tag, "model": model, "stop": r.stop_reason, "in": r.usage.input_tokens, "out": r.usage.output_tokens,
                   "cache_w": r.usage.cache_creation_input_tokens or 0, "cache_r": r.usage.cache_read_input_tokens or 0,
                   "sec": round(dt, 2), "usd": cost_of(model, r.usage)})
    if raw:
        return r
    return "".join(b.text for b in r.content if b.type == "text")


def spend(tag=None):
    rows = [x for x in LEDGER if tag is None or x["tag"] == tag]
    return {"calls": len(rows), "input_tokens": sum(x["in"] for x in rows), "output_tokens": sum(x["out"] for x in rows),
            "usd": round(sum(x["usd"] for x in rows), 4), "avg_sec": round(sum(x["sec"] for x in rows) / max(1, len(rows)), 2)}
