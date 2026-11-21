# Prompt Engineering Full Course 2026

Hands-on companion code for **David Oluyale, Agentic AI Hub**: *Prompt Engineering Full Course 2026: Beginner to Advanced (Hands-On)*.

Watch the full course on YouTube: https://youtu.be/MkY-3PZEMWE

Free cheat sheet: https://535214083743.gumroad.com/l/znjjvv

- YouTube channel: https://www.youtube.com/@AgenticAIHub1
- Notebook on Google Colab: https://colab.research.google.com/drive/1UstrHf0EMx6B0Ed3jHser50djLVUnSsX

You build one project, the **Lumora Solar Support Copilot**. Lumora is a fictional home-solar installer. Every ticket, customer, invoice, and manual page in this repo is synthetic. Each chapter adds one prompting technique, and a 20-ticket scorecard measures what that technique changes.

The course code lives in [`lumora-copilot/`](lumora-copilot/). The notebook finds a folder with that name, which is why the project is not flattened onto the repository root.

## What the course covers

The notebook has 21 chapters:

1. Setup and the anatomy of a prompt
2. Zero-shot, clear instructions, and delimiters
3. System prompts, roles, persona, and tone
4. Few-shot prompting
5. Output formatting and structured outputs (JSON Schema)
6. Prompt templates, variables, and versioning
7. Chain-of-thought and reasoning models (and when not to use chain-of-thought)
8. Self-consistency and program-aided reasoning
9. Prompt chaining
10. Decomposition: least-to-most, step-back, and plan-and-solve
11. ReAct and tool use (function calling)
12. RAG prompting and grounding with citations
13. Long-context techniques
14. Multimodal prompting (images and documents)
15. Tree of Thoughts
16. Reflection, self-critique, and Chain-of-Verification
17. Meta-prompting, prompt generation, and automatic optimisation
18. Prompt caching, cost, and latency
19. Security: prompt injection and layered defences
20. Evaluating prompts: a test set, LLM-as-judge, and Promptfoo
21. Wrap-up: the scorecard

The recorded run uses `claude-haiku-5-5` for almost every call, and `claude-sonnet-5-5` when a chapter compares models or asks a judge model to score a reply. That full notebook run made 950 API calls (1,716,921 input tokens and 117,203 output tokens) and cost about **$0.48**. Prices change. Check [Anthropic's pricing page](https://platform.claude.com/docs/en/about-claude/pricing) before you run every cell. Each cell prints its own cost from the ledger in `lumora/llm.py`.

## Prerequisites

- Python 3.10 or newer, with `pip`. Python 3.11 or 3.12 is a good choice.
- An Anthropic API key of your own, for any chapter that calls the model: https://console.anthropic.com/
- Optional: JupyterLab, or VS Code with the Jupyter extension, to run the notebook.
- Optional: Node.js 20 or newer, only for the Promptfoo eval in Chapter 20.

The data files and the pure-Python helpers (quote math, retrieval, the scheduling checker, and the fake tools) run with no API key and no spend. The notebook and `scripts/` call the API once a key is loaded.

## Setup

```bash
git clone https://github.com/davolu/prompt-engineering-course-2026
cd prompt-engineering-course-2026/lumora-copilot
python -m venv .venv
```

Activate the virtual environment:

- macOS and Linux: `source .venv/bin/activate`
- Windows Command Prompt: `.venv\Scripts\activate.bat`
- Windows PowerShell: `.venv\Scripts\Activate.ps1`

```bash
pip install -r requirements.txt
cp .env.example .env
```

On Windows Command Prompt, copy the template with `copy .env.example .env`.

Open `.env` and set your own key:

```
ANTHROPIC_API_KEY=your-key-here
```

Leave the committed `.env.example` empty. `.env` is listed in `.gitignore`. Do not commit it, and do not paste the key into the notebook or into a screenshot.

The Anthropic SDK reads `ANTHROPIC_API_KEY` from the environment. Load `.env` into the same shell you use to run Python:

```bash
set -a
source .env
set +a
```

On Windows PowerShell, from the `lumora-copilot` folder:

```powershell
Get-Content .env | ForEach-Object {
  if ($_ -match '^\s*ANTHROPIC_API_KEY=(.*)$') {
    $env:ANTHROPIC_API_KEY = $matches[1].Trim()
  }
}
```

Confirm the key is present without printing it:

```bash
python -c "import os; print('ANTHROPIC_API_KEY is set:', bool(os.environ.get('ANTHROPIC_API_KEY')))"
```

## How to run each part

Run these from `lumora-copilot/` with the virtual environment active.

### Notebook

| File | When to open it |
|---|---|
| `notebooks/Prompt_Engineering_Full_Course.ipynb` | Run the course yourself. This copy has empty outputs. |
| `notebooks/Prompt_Engineering_Full_Course_EXECUTED.ipynb` | Read the outputs from the recorded run. |

```bash
pip install jupyterlab
jupyter lab notebooks/Prompt_Engineering_Full_Course.ipynb
```

JupyterLab is separate from `requirements.txt`. The scripts do not need it. Install it in this same virtual environment when you want the notebook UI.

### Google Colab

The notebook's first cell tells you to upload `lumora-copilot.zip` and unzip it. Colab users can clone this repo instead. Paste this into a cell:

```python
!git clone https://github.com/davolu/prompt-engineering-course-2026
%cd prompt-engineering-course-2026
```

That leaves a `lumora-copilot` folder in the working directory, which is the folder the notebook adds to `sys.path`. Add `ANTHROPIC_API_KEY` in Colab's Secrets panel (the key icon) and allow notebook access. Uncomment the `%pip install` line in the first code cell, then run the cells.

Published Colab notebook: https://colab.research.google.com/drive/1UstrHf0EMx6B0Ed3jHser50djLVUnSsX

### Scripts

These four scripts call the API. Load your key first.

```bash
python scripts/structured_output.py
python scripts/chain.py T002          # every step for one ticket
python scripts/chain.py               # 8 tickets: pass rate before and after the fix step
python scripts/agent.py               # the agent asks before it books
python scripts/agent.py --approve     # customer confirms, a human approves the booking
python scripts/security.py            # poisoned knowledge-base pages vs L0, L1, and L2 defences
```

`scripts/structured_output.py` is Chapter 5 (a Pydantic model as the response schema). `scripts/chain.py` is Chapter 9 (triage, extract, draft, check, fix). `scripts/agent.py` is Chapter 11 (tool use). `scripts/security.py` is Chapter 19 (prompt injection).

### Promptfoo eval (Chapter 20)

`make_tests.py` reads the local tickets and writes `evals/tests.yaml`. It does not call the API. `promptfoo eval` does.

```bash
cd evals
python make_tests.py
npx promptfoo@latest eval -j 8
npx promptfoo@latest view
```

`npx promptfoo` needs Node.js 20 or newer. If it cannot see this virtual environment, point it at the interpreter:

```bash
export PROMPTFOO_PYTHON="$(pwd)/../.venv/bin/python"
```

## Project structure

```
prompt-engineering-course-2026/
├── README.md                 this guide
├── LICENSE                   MIT License, copyright David Oluyale
├── .gitignore
└── lumora-copilot/
    ├── .env.example          empty ANTHROPIC_API_KEY; copy to .env
    ├── requirements.txt      anthropic, pydantic, jinja2
    ├── README.md             short guide for this folder
    ├── notebooks/            clean notebook and the executed notebook
    ├── lumora/               API wrapper, scoring, quotes, RAG, tools, scheduling
    ├── prompts/              versioned Jinja triage templates (Chapter 6)
    ├── scripts/              structured output, chain, agent, security
    ├── evals/                Promptfoo eval of triage v0 vs v6 on all 40 tickets
    ├── data/                 synthetic tickets, labels, facts, manual, attack cases
    └── images/               a scanned bill and an inverter photo, both synthetic
```

| Path | What it is |
|---|---|
| `lumora/llm.py` | `ask()` and a per-call cost ledger |
| `lumora/score.py` | Accuracy on category, urgency, and needs_human |
| `lumora/quote.py` | Ground-truth quote totals, computed in code |
| `lumora/rag.py` | TF-IDF search over the manual, split on `[Sx.y]` headings |
| `lumora/schedule.py` | Crew-scheduling puzzle and a checker for Tree of Thoughts |
| `lumora/tools.py` | Fake customer, slot, and booking tools |
| `prompts/triage_v5.md`, `prompts/triage_v6.md` | Jinja templates for the triage prompt |
| `data/tickets.json` | 40 labelled tickets. The first 20 are the scorecard set |

## Safety

- Keep the API key in `.env` on your machine. The notebook prints only whether the key is set.
- `create_ticket` in `lumora/tools.py` returns `pending_approval` until the call passes `approved_by_human=True`. Nothing here books a real visit.
- Chapter 19 plants fake refund links, a fake bank account, and a fake billing contact on the reserved `.example` domain inside customer text and manual pages. Those strings are the attack examples for the defence lesson. The account details are fictional.

## License

[MIT License](LICENSE). Copyright (c) 2026 David Oluyale.
