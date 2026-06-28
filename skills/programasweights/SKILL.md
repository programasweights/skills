---
name: programasweights
description: Compile a natural-language spec into a tiny neural function that runs locally with ProgramAsWeights (PAW). Use it for fuzzy text-in / text-out tasks that a regex can't handle but that are too slow, costly, or overkill to send to a full LLM on every item - classify, categorize, label, or tag text (sentiment, urgency, intent, topic, spam, support tickets, ALERT vs QUIET log lines); extract fields from messy text (emails, names, dates, IDs, invoice numbers); repair or normalize formats (broken JSON, dates); fuzzy or typo-tolerant matching, near-duplicate detection, and deduplication; map a misspelled value to the closest option; semantic search; log and error triage; and intent routing. Compile once on the hosted API, then run the function locally and offline via the Python or browser/JavaScript SDK; cheaper and faster than calling a large model per item. Not for long-form generation, open-ended chat, writing code, or multi-step reasoning.
license: MIT
version: 0.1.0
metadata:
  short-description: Compile fuzzy text-in/text-out functions that run locally
---

# ProgramAsWeights (PAW)

ProgramAsWeights compiles a short natural-language spec into a tiny neural function
("neural software") that takes one text input and returns one text output and runs
locally. You compile once on the hosted API; the resulting function then runs locally
and offline forever.

- Website: https://programasweights.com
- Docs: https://programasweights.readthedocs.io

## When to use this

Reach for PAW when a task is fuzzy `text -> text` and you want it cheap, fast, local,
and repeatable:

- **Classification / categorization** - sentiment, urgency, intent, topic, spam, or `ALERT` vs `QUIET` log lines.
- **Extraction** - pull emails, names, dates, IDs, or fields out of messy/unstructured text.
- **Format repair / normalization** - fix broken JSON, normalize dates, clean inconsistent inputs.
- **Fuzzy matching** - typo-tolerant matching, near-duplicate detection, map a phrase to the closest option.
- **Triage / routing** - filter noise from logs, route a request to the right handler.

It replaces a brittle regex or an expensive per-item LLM call with one small function
that, after compiling, runs in roughly 0.05-0.5s locally with no network.

## When NOT to use it

- Long-form or open-ended generation (essays, code, chat) - use a full LLM instead.
- Multi-step reasoning, math, or tasks that need broad world knowledge.
- Anything that is not single text in -> single text out. Functions are stateless and
  share a ~2048-token window across spec + input + output.

## How to use it (the workflow)

**1. Check the Hub first.** Someone may have already published a function; try a slug
before compiling:

```python
import programasweights as paw

fn = paw.function("email-triage")   # downloads once, then runs locally
fn("Urgent: server is down!")        # "immediate"
fn("Newsletter: spring picnic")      # "wait"
```

**2. Otherwise compile your own.** A good spec is a description PLUS a few
`Input: ... Output: ...` examples and an explicit output constraint:

```python
import programasweights as paw

fn = paw.compile_and_load("""
Classify support tickets. Return ONLY one of: billing, bug, feature, other.

Input: I was charged twice this month
Output: billing

Input: The export button does nothing
Output: bug

Input: Please add a dark mode
Output: feature
""")

fn("my card got charged again")   # "billing"
```

**3. Iterate with test cases - the #1 practice.** Do not accept the first result.
Build a small set of input/expected pairs, measure accuracy, then refine the wording
and examples and recompile until it is good enough. Treat it like software: test, debug
the specific failures, fix the spec, retest. A minimal eval loop:

```python
import programasweights as paw

tests = [
    {"input": "I was charged twice this month", "expected": "billing"},
    {"input": "The export button does nothing", "expected": "bug"},
    {"input": "Please add a dark mode",          "expected": "feature"},
]

fn = paw.compile_and_load(open("spec.txt").read())
results = [(t, fn(t["input"]).strip()) for t in tests]
misses = [(t, got) for t, got in results if got != t["expected"]]
print(f"accuracy: {(len(tests) - len(misses)) / len(tests):.0%}")
for t, got in misses:        # inspect failures, then fix the spec + recompile
    print("FAIL:", t["input"], "-> got", repr(got), "want", repr(t["expected"]))
```

See `references/writing-good-specs.md` for how to debug the misses.

**4. Save the program id or slug and reuse it locally.** Inference needs no server after
the first asset download.

## Install

```bash
pip install programasweights --extra-index-url https://pypi.programasweights.com/simple/
```

Browser / JavaScript: `npm install @programasweights/web`. Functions compiled with
`compiler="paw-4b-gpt2"` run client-side via WebAssembly. See `references/browser-sdk.md`.

## What runs where (data flow - read before using)

- **Compile** sends your spec to the hosted PAW API (`https://programasweights.com`) and
  returns a program id. Do not put secrets in a spec.
- **Inference runs locally** through the SDK and works offline after the first download.
- **Auth is optional** - anonymous use works. Sign in only for higher compile rate limits
  and named slugs (`export PAW_API_KEY=paw_sk_...`).

## More detail (load on demand)

- Full API, compilers, versioning, chaining, auth: `references/api.md`
- Writing and debugging specs: `references/writing-good-specs.md`
- Browser / JavaScript SDK: `references/browser-sdk.md`
- Common errors and fixes: `references/troubleshooting.md`
- Worked case studies (log monitoring, semantic search, tool calling): https://programasweights.readthedocs.io
