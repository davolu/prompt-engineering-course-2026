"""Tiny retrieval for the RAG chapter: split the manual by [Sx.y] sections and rank with TF-IDF."""
import math, re
from collections import Counter
from .data import MANUAL

def sections(text=MANUAL):
    parts = re.split(r"(?=^### \[S\d+\.\d+\])", text, flags=re.M)
    out = []
    for p in parts:
        m = re.match(r"### \[(S\d+\.\d+)\]\s*(.*)", p)
        if m:
            out.append({"id": m.group(1), "title": m.group(2).strip(), "text": p.strip()})
    return out

SECTIONS = sections()
_tok = lambda s: re.findall(r"[a-z0-9]+", s.lower())
_df = Counter(w for s in SECTIONS for w in set(_tok(s["text"])))
_N = len(SECTIONS)

def search(query, k=4):
    q = _tok(query)
    def score(s):
        tf = Counter(_tok(s["text"]))
        return sum(tf[w] * math.log((_N + 1) / (_df[w] + 0.5)) for w in q if w in tf) / math.sqrt(len(tf) + 1)
    return sorted(SECTIONS, key=score, reverse=True)[:k]

def as_documents(hits):
    return "\n".join(f'<document id="{h["id"]}">\n{h["text"]}\n</document>' for h in hits)
