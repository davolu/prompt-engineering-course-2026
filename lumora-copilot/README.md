# Lumora Solar Support Copilot: Prompt Engineering Full Course (2026)

Code for the **Agentic AI Hub** video *Prompt Engineering Full Course 2026: Every Technique, Hands-On*.

Watch the full course on YouTube: https://youtu.be/MkY-3PZEMWE

Free cheat sheet: https://535214083743.gumroad.com/l/znjjvv

The guide at the repository root covers cloning, the virtual environment, your API key, Colab, and how to run each part. The commands below assume you are already inside this `lumora-copilot` folder.

Lumora Solar is a **fictional** home-solar installer. Every ticket, customer, invoice and manual page here is synthetic.

## What is inside

| Path | What it is |
|---|---|
| `notebooks/Prompt_Engineering_Full_Course.ipynb` | The course notebook, chapters 1-21 (clean, no outputs) |
| `notebooks/Prompt_Engineering_Full_Course_EXECUTED.ipynb` | The same notebook with the real outputs from the recorded run |
| `lumora/` | Small helpers: `ask()` with a cost ledger, scoring, quote ground truth, tools, RAG search, scheduling puzzle |
| `prompts/triage_v5.md`, `triage_v6.md` | Versioned Jinja prompt templates (Chapter 6) |
| `scripts/` | The VS Code chapters: `structured_output.py`, `chain.py`, `agent.py`, `security.py` |
| `evals/` | Promptfoo eval of the triage prompt, v0 vs v6 on all 40 tickets (Chapter 20) |
| `data/`, `images/` | Synthetic tickets, labels, facts, manual, history, attack cases, two test images |

## Setup (local)

```bash
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env        # then put your own key in .env, and load it into your shell
jupyter lab notebooks/      # or open the notebook in VS Code
```

## Setup (Colab)

The notebook's first cell says to upload `lumora-copilot.zip` and unzip it. Clone the repo instead:

```
!git clone https://github.com/davolu/prompt-engineering-course-2026
%cd prompt-engineering-course-2026
```

The notebook looks for a `lumora-copilot` folder in the current directory, which this clone provides. Then:

1. Add your key in the Secrets panel (key icon) as `ANTHROPIC_API_KEY` and allow notebook access.
2. Uncomment the `%pip install` line in the first code cell and run all cells.

## Scripts and evals

```bash
python scripts/structured_output.py
python scripts/chain.py T002          # every step for one ticket
python scripts/chain.py               # 8 tickets: pass rate before and after the fix step
python scripts/agent.py               # the agent asks before it books
python scripts/agent.py --approve     # customer confirms, a human approves the booking
python scripts/security.py            # poisoned knowledge-base pages vs L0, L1, L2 defences

cd evals
python make_tests.py                  # writes tests.yaml from data/tickets.json
npx promptfoo@latest eval -j 8        # needs Node 20+; set PROMPTFOO_PYTHON to your venv's python
npx promptfoo@latest view
```

## Models and cost

- `claude-haiku-5-5` for almost every call, `claude-sonnet-5-5` for comparisons and judging.
- The executed notebook's final cell records 950 API calls and a cost of **$0.48**. Every cell prints its own cost from the ledger in `lumora/llm.py`.
- Prices change. Check the provider's pricing page before you run.

## Safety notes

- Never print or commit your API key. The notebook only prints whether the key is set.
- The tools in `lumora/tools.py` are fakes. `create_ticket` needs `approved_by_human=True`, the human-in-the-loop switch.
