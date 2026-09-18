# PAW API reference

Canonical and always-current: https://programasweights.com/AGENTS.md and
https://programasweights.readthedocs.io

## Core Python API

```python
import programasweights as paw

program = paw.compile(
    spec,                 # natural-language specification (str)
    compiler=None,        # omit for the server default (today: paw-4b-qwen3-0.6b)
    slug=None,            # URL-safe handle (requires auth)
    public=True,          # list on the public Hub
)
# -> Program(id, slug, status, version, version_action, timings, error)

fn = paw.function(program)                  # Program object, hash id, or slug
fn = paw.function("a6b454023d41ac9ca845")
fn = paw.function("da03/my-classifier")
fn = paw.function("da03/my-classifier@v2")  # pinned, immutable version
fn = paw.function("da03/my-classifier", offline=True)  # skip the server check

result: str = fn(input_text, max_tokens=None, temperature=0.0)

fn = paw.compile_and_load(spec)             # compile + load in one step

paw.list_versions("da03/my-classifier")     # version history
paw.list_programs(sort="recent", per_page=20)  # requires auth
paw.list_compilers()                        # discover compilers at runtime
paw.login()
```

## Remote inference (optional)

Use the hosted API for fast inference in around 150 ms, without a local model download.

```python
import httpx

with httpx.Client(timeout=60.0) as client:
    response = client.post(
        "https://programasweights.com/api/v1/infer",
        json={
            "program_id": "email-triage",
            "input": "Urgent: server is down!"
        },
    )
    response.raise_for_status()
    print(response.json()["output"])
```

Replace `"email-triage"` with your program's ID or slug, or with `program.id` returned by `paw.compile()`.

Public programs work without authentication. For authenticated requests, pass `headers={"X-API-Key": api_key}` to `client.post()`.

Respect `429` responses and `Retry-After`. If the API returns `503` with `error: "artifact_warming"`, wait for `Retry-After` before retrying.

## Compilers

- **Standard** (`paw-4b-qwen3-0.6b`) - server default, higher accuracy, 594 MB base + ~22 MB/program.
- **Compact** (`paw-4b-gpt2`) - smaller (134 MB base + ~5 MB/program), runs in the browser via WebAssembly.

Prefer `paw.compile(spec)` with no explicit compiler for quickstarts. Pass
`compiler="paw-4b-gpt2"` when you need the browser runtime. Call `paw.list_compilers()`
to inspect what the server currently supports.

## Constraints and runtime

- Each function is stateless: one text input, one text output. No conversation history.
- Spec + input + output share a ~2048-token window. Inputs that exceed it error.
- Compile runs on the hosted API; inference runs locally through the SDK.
- GPU acceleration is on by default (Metal/CUDA, CPU fallback). Force CPU with
  `PAW_GPU_LAYERS=0` or `n_gpu_layers=0`.
- First call is ~1-5s (loads the shared base model); later calls ~0.05-0.5s. Offline after
  the first download. Cache root: `~/.cache/programasweights/` (override `PAW_CACHE_DIR`).

## Versioning (slugs)

Recompiling with the same slug creates a new version; bare slugs resolve to the latest
main version, pinned `@vN` are immutable and cached forever.

```python
paw.compile("Count words v1", slug="word-counter")  # v1
paw.compile("Count words v2", slug="word-counter")  # v2 (auto-bumps)
fn = paw.function("da03/word-counter")     # latest
fn = paw.function("da03/word-counter@v1")  # pinned
```

## Chaining

Compose multiple functions with ordinary Python logic:

```python
classifier = paw.compile_and_load("Classify the bug type. Return ONLY: off-by-one, type-error, other")
fixer = paw.compile_and_load("Fix the bug described in the first line. Return only the corrected code.")

label = classifier(code_snippet)
if label != "other":
    fix = fixer(f"{label}: {code_snippet}")
```

## Authentication (optional)

```bash
export PAW_API_KEY=paw_sk_...   # from https://programasweights.com/settings
```

Anonymous: 20 compiles/hr, 1 concurrent. Authenticated: 60 compiles/hr, 2 concurrent,
and named slugs. Inference is local and not rate-limited.

## CLI

`paw compile --spec "..." --json`, `paw run --program <id> --input "..."`,
`paw info <id>`, `paw rename <id> <slug>`, `paw login`. All support `--json`.
