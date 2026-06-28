# Contributing

Thanks for helping improve the ProgramAsWeights agent skill.

## Ground rules

- **Keep it script-free.** The installed skill (`skills/programasweights/`) should contain
  only Markdown (`SKILL.md`, `references/*.md`). Do not add executable scripts or compiled
  artifacts to the skill folder; that surface is intentionally minimal for trust.
- **No committed binaries** except image assets (`.png`, `.svg`, `.jpg`, `.ico`, ...). CI
  rejects `.pyc`, archives, shared objects, and other executable binaries.
- **The `description` is the trigger.** Keep it under 1024 characters and clear about both
  *what* the skill does and *when* to use it.

## Before opening a PR

Run the validators locally:

```bash
pip install pyyaml
python scripts/validate_skill.py     # frontmatter, name==dir, description length, ref paths, binaries
python scripts/eval_trigger.py       # heuristic trigger coverage (informational)
```

Then sanity-check that the skill still resolves:

```bash
npx skills add . --list
```

## What to contribute

- Sharper trigger wording or new should/should-not cases in `tests/trigger_cases.yaml`.
- Better worked examples in `references/`.
- Fixes to keep the references in sync with the canonical docs at
  https://programasweights.readthedocs.io.
