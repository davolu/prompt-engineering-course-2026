# Prompt Engineering: Beginner to Advanced (2026 Full Course, Hands-On)

Hands-on companion code for **David Oluyale, Agentic AI Hub**: *Prompt Engineering: Beginner to Advanced (2026 Full Course, Hands-On)*.

Watch the full course on YouTube: https://youtu.be/c9dAjdGX8D4

- Notebook on Google Colab (run it yourself): https://colab.research.google.com/drive/1UstrHf0EMx6B0Ed3jHser50djLVUnSsX
- Free 2-page cheat sheet: https://535214083743.gumroad.com/l/znjjvv (also in this repo: [`beginners-2026/Prompt_Engineering_for_Beginners_Cheat_Sheet.pdf`](beginners-2026/Prompt_Engineering_for_Beginners_Cheat_Sheet.pdf))
- YouTube channel: https://www.youtube.com/@AgenticAIHub1

No coding experience needed. The course teaches 16 prompting techniques, one at a time. Each lesson has its own small, everyday example and follows the same five steps: what it is in one sentence, a weak prompt and its answer, the technique explained line by line, the two answers side by side with a real measured number, and a one-line recap of when to use it.

## The 16 lessons

| # | Technique | Everyday example | Result in the recorded run |
|---|---|---|---|
| 1 | Clear instructions | A birthday message | Rules followed: 0/5 vs 5/5 |
| 2 | Delimiters | Summarising product reviews | Clean summaries: 6/10 vs 10/10 |
| 3 | Roles (system prompts) | Doctor, teacher, comedian | Reading grade 11.5 with no role, 5.6 as a teacher |
| 4 | Few-shot examples | Labelling tweets | Exact labels: 0/10 vs 10/10 |
| 5 | Structured output (JSON) | A recipe turned into data | Valid JSON: 0/5 vs 5/5 |
| 6 | Templates | Product descriptions | 241 words vs 3/3 under 60 words |
| 7 | Chain-of-thought | A big shopping bill | Correct total: 2/8 vs 8/8 |
| 8 | Self-consistency | Asking 5 times and voting | Single answers 18/20, majority vote 4/4 |
| 9 | Prompt chaining | A blog post: outline, draft, edit | 540 words (grade 8.0) vs 221 words (grade 3.3) |
| 10 | Breaking a big task into small questions | A $400 family weekend | Within budget: 4/5 vs 5/5 |
| 11 | Tool use | Should I take an umbrella? | The answer used the weather tool's 80% forecast |
| 12 | RAG (answering from your own documents) | A school handbook, with sources | Correct: 0/5 vs 5/5 |
| 13 | Prompts with images | A shopping receipt photo | 6/6 prices and the total read correctly |
| 14 | Reflection | An email to a landlord | Checklist score: 1/4 vs 4/4 |
| 15 | Prompt injection and how to defend | An email summariser | Warnings: 0/6 vs 6/6; bad links repeated: 1 vs 0 |
| 16 | Testing your prompts | A 12-tweet scorecard | Vague 0/12, one-word 12/12, few-shot 12/12 |

The whole recorded notebook run used 30,788 input and 33,126 output tokens on `claude-haiku-5-5` and cost about **$0.02**. Prices change, so check [Anthropic's pricing page](https://platform.claude.com/docs/en/about-claude/pricing) before you run it. Results will vary a little from run to run.

## Files

| File | What it is |
|---|---|
| [`beginners-2026/Prompt_Engineering_for_Beginners_2026.ipynb`](beginners-2026/Prompt_Engineering_for_Beginners_2026.ipynb) | The notebook to run yourself (empty outputs) |
| [`beginners-2026/Prompt_Engineering_for_Beginners_2026_EXECUTED.ipynb`](beginners-2026/Prompt_Engineering_for_Beginners_2026_EXECUTED.ipynb) | The same notebook with every output from the recorded run |
| [`beginners-2026/Prompt_Engineering_for_Beginners_Cheat_Sheet.pdf`](beginners-2026/Prompt_Engineering_for_Beginners_Cheat_Sheet.pdf) | 2-page cheat sheet: a pattern to copy for each technique |
| [`beginners-2026/receipt.jpg`](beginners-2026/receipt.jpg) | The made-up receipt photo used in Lesson 13 |

## Run it in Google Colab (easiest)

1. Open the Colab link above, then choose **File → Save a copy in Drive**.
2. Click the key icon on the left (Secrets), add a secret named `ANTHROPIC_API_KEY` with your own key, and switch **Notebook access** on. Get a key at https://console.anthropic.com/.
3. Run the cells from top to bottom with **Shift + Enter**. Lesson 13 downloads the receipt photo by itself.

The notebook only prints whether the key was found. Never paste your key into a cell, a screenshot, or a commit.

## Run it on your own computer

```bash
git clone https://github.com/davolu/prompt-engineering-course-2026
cd prompt-engineering-course-2026/beginners-2026
python -m venv .venv
source .venv/bin/activate        # Windows: .venv\Scripts\activate
pip install anthropic jupyterlab
export ANTHROPIC_API_KEY=your-key-here   # Windows PowerShell: $env:ANTHROPIC_API_KEY="your-key-here"
jupyter lab Prompt_Engineering_for_Beginners_2026.ipynb
```

---

# Going further: the Lumora Solar project (first edition)

The rest of this repository is the earlier, more advanced edition of the course. It has one bigger project, the **Lumora Solar Support Copilot**, with 21 chapters measured on a 20-ticket scorecard. It covers extra topics such as long context, Tree of Thoughts, meta-prompting, prompt caching and a Promptfoo eval. The code lives in [`lumora-copilot/`](lumora-copilot/). Every ticket, customer, invoice and manual page in it is synthetic.

That full notebook run made 950 API calls (1,716,921 input tokens and 117,203 output tokens) and cost about **$0.48**.

## Lumora: prerequisites

- Python 3.10 or newer, with `pip`. Python 3.11 or 3.12 is a good choice.
- An Anthropic API key of your own, for any chapter that calls the model: https://console.anthropic.com/
- Optional: JupyterLab, or VS Code with the Jupyter extension, to run the notebook.
- Optional: Node.js 20 or newer, only for the Promptfoo eval in Chapter 20.

The data files and the pure-Python helpers (quote math, retrieval, the scheduling checker, and the fake tools) run with no API key and no spend. The notebook and `scripts/` call the API once a key is loaded.

## Lumora: setup

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

## Lumora: how to run each part

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

## Lumora: project structure

```
prompt-engineering-course-2026/
├── README.md                 this guide
├── LICENSE                   MIT License, copyright David Oluyale
├── .gitignore
├── beginners-2026/           the beginner course: notebooks, cheat sheet, receipt photo
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
