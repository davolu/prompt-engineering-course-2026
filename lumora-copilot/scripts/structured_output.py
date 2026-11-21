"""Chapter 5: structured outputs. A Pydantic model becomes the JSON schema the reply must follow."""
import _path  # noqa: F401  (adds the project root to sys.path)
from typing import Literal
from pydantic import BaseModel, Field
from lumora.llm import client, HAIKU
from lumora.prompts import SYSTEM_FEW, v3, BY_ID

class Triage(BaseModel):
    category: Literal["quote", "billing", "scheduling", "technical_fault", "app_account"]
    urgency: Literal["low", "normal", "urgent"]
    needs_human: bool
    reason: str = Field(description="one short sentence")

def triage(ticket) -> Triage:
    r = client.messages.parse(model=HAIKU, max_tokens=300, thinking={"type": "disabled"}, system=SYSTEM_FEW,
                              messages=[{"role": "user", "content": v3(ticket)}], output_format=Triage)
    return r.parsed_output

for tid in ["T001", "T002", "T009"]:
    t = BY_ID[tid]
    tri = triage(t)
    # The schema guarantees the shape. Business rules are still your job:
    rule_ok = not (tri.urgency == "urgent" and not tri.needs_human)
    print(f"{tid} {t['subject'][:38]:<40} -> {tri.category:<16} {tri.urgency:<7} human={tri.needs_human!s:<5} rule ok={rule_ok}")
    print(f"     reason: {tri.reason}")
