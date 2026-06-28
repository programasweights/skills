# Writing and debugging PAW specs

The single highest-leverage practice: **iterate with test cases.** Do not accept low
performance on the first try. Treat spec writing like software engineering - test, debug
the specific failures, fix the wording, retest.

## Anatomy of a good spec

A description PLUS a few `Input: ... Output: ...` examples PLUS an explicit output
constraint:

```python
fn = paw.compile_and_load("""
Classify user intent. Return ONLY one of: search, create, delete, other.

Input: Find the latest report
Output: search

Input: Make a new folder
Output: create

Input: Remove old backups
Output: delete
""")
```

## Tips

- **State output constraints explicitly** - "Return ONLY one of: X, Y, Z". Without this
  the model may produce free-form text.
- **Use examples from your actual data** - real examples outperform prose-only descriptions.
- **Debug failures before sweeping** - look at specific failing inputs and understand WHY
  before trying many variants.
- **Keep it inside the window** - spec + input + output share ~2048 tokens. For long
  inputs, trim or pre-chunk.

## The compile -> test -> iterate loop

1. Write a first spec with a few examples.
2. Build a small test set of `input -> expected` pairs (10-30 covers most signal).
3. Compile, run the test set, look at the misses.
4. Add or fix examples / tighten the wording, recompile, re-measure.
5. Stop when accuracy is good enough; save the program id or slug and reuse it.

A minimal eval loop for steps 3-4 - compile, run the test set, print accuracy and the
specific misses, then fix the spec and recompile:

```python
import programasweights as paw

tests = [{"input": "...", "expected": "..."}]   # your input/expected pairs
fn = paw.compile_and_load(open("spec.txt").read())
results = [(t, fn(t["input"]).strip()) for t in tests]
misses = [(t, got) for t, got in results if got != t["expected"]]
print(f"accuracy: {(len(tests) - len(misses)) / len(tests):.0%}")
for t, got in misses:
    print("FAIL:", t["input"], "-> got", repr(got), "want", repr(t["expected"]))
```

More worked examples and case studies: https://programasweights.readthedocs.io
