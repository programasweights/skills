# Security & trust

Agent skills are instructions an AI agent will act on, so treat any skill like code you
install. Here is exactly what this one does, so you can verify it before trusting it.

## What this skill contains

- `skills/programasweights/SKILL.md` and `references/*.md` - **plain Markdown instructions
  only.** There is **no bundled executable code** in the installed skill (it is
  script-free by design, to keep the attack surface minimal).
- `assets/` - brand image files (`paw.svg`, `icon-512.png`) only.

## Data flow (one network boundary)

- **Compile** sends the spec text you give it to the hosted PAW API at
  `https://programasweights.com` and returns a program id. **Do not put secrets in a
  spec.**
- **Inference runs locally** through the official `programasweights` SDK and works
  **offline** after the first asset download. No user data is sent at inference time.
- **Auth is optional** - anonymous use works; an API key only raises compile rate limits
  and enables named slugs.

## What this skill does NOT do

- It does not fetch or execute remote code, scripts, or instructions.
- It does not read your environment variables, credentials, or files beyond the spec/test
  text you explicitly pass to the SDK.
- It does not request broad tool permissions.

## Provenance & pinning

- Published from the official ProgramAsWeights GitHub organization under the MIT license.
- Releases are tagged. For reproducibility, pin to a release tag or commit rather than a
  moving branch, and re-review the diff before upgrading.

## Reporting

If you find a security issue, please open a GitHub security advisory on this repository or
reach us via https://programasweights.com. Do not file sensitive reports as public issues.
