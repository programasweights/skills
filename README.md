# ProgramAsWeights agent skill

An [Agent Skill](https://agentskills.io) that teaches your AI coding agent to use
**[ProgramAsWeights (PAW)](https://programasweights.com)** - compile a natural-language
spec into a tiny neural function that runs locally - for fuzzy text tasks like
classification, extraction, format repair, fuzzy matching, log triage, and routing.

## Install

```bash
npx skills add programasweights/skills
```

Works with Claude Code, Cursor, Codex, GitHub Copilot, and 65+ other agents (the
[`skills` CLI](https://github.com/vercel-labs/skills) installs it into each one's skill
directory). Add `-g` to install globally for every project:

```bash
npx skills add programasweights/skills -g
```

Or try it without installing:

```bash
npx skills use programasweights/skills@programasweights | claude
```

## What it does

Once installed, the skill activates automatically when you ask your agent to do fuzzy
`text -> text` work that regex can't handle but a full LLM call per item is overkill for:

- Classify / categorize (sentiment, urgency, intent, topic, spam, ALERT vs QUIET)
- Extract fields from messy text (emails, names, dates, IDs)
- Repair / normalize formats (broken JSON, dates)
- Fuzzy / typo-tolerant matching and near-duplicate detection
- Log triage and intent routing

The agent will check the PAW Hub for a ready-made function, or compile one from a spec
with examples, iterate it against test cases, and reuse it locally.

## What's inside

```
skills/programasweights/
  SKILL.md          # the skill (trigger + workflow); the eval loop is embedded inline
  LICENSE.txt       # per-skill MIT license
  references/       # api, writing-good-specs, browser-sdk, troubleshooting (loaded on demand)
assets/             # brand icon (paw.svg, icon-512.png)
SECURITY.md         # exactly what the skill does + data flow
```

The installed skill is **script-free** - Markdown instructions only, no bundled executable
code. (The Codex/Claude plugin + marketplace manifests in this repo are packaging only and
are not yet listed in any directory.)

## Manual install (without the CLI)

Copy `skills/programasweights/` into your agent's skills directory, e.g.:

- Claude Code: `~/.claude/skills/programasweights/`
- Codex: `~/.codex/skills/programasweights/`
- GitHub Copilot: `.github/skills/programasweights/`

## Data flow and trust

- **Compile** sends your spec to the hosted PAW API (`https://programasweights.com`) and
  returns a program id. Do not put secrets in a spec.
- **Inference runs locally** through the official `programasweights` SDK and works offline
  after the first download. No user data is sent at inference time.
- Auth is optional (anonymous use works). MIT licensed; read every file before installing.
- Full details, including what the skill does **not** do, are in [SECURITY.md](SECURITY.md).
  For reproducibility, pin to a release tag or commit and re-review before upgrading.

## Links

- Website: https://programasweights.com
- Agent guide (always current): https://programasweights.com/AGENTS.md
- Docs: https://programasweights.readthedocs.io

## License

MIT - see [LICENSE](LICENSE).
