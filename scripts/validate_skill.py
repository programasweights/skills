#!/usr/bin/env python3
"""Validate every SKILL.md in this repo against the Agent Skills spec.

Checks (per https://agentskills.io and the `skills` CLI):
  - YAML frontmatter present and parseable
  - `name`: present, lowercase + hyphens only, <= 64 chars, equals the parent dir name
  - `description`: present, non-empty, <= 1024 chars
  - referenced `references/` and `scripts/` paths used in SKILL.md exist

Exits non-zero on any failure. No third-party dependencies.
"""

import pathlib
import re
import sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
NAME_RE = re.compile(r"^[a-z0-9]([a-z0-9-]*[a-z0-9])?$")

# Executable / opaque binary types are the main agent-skill abuse vector (e.g. .pyc
# bytecode poisoning, archives hiding payloads). We reject them anywhere in the repo.
# Image assets are allowed (brand icons).
DANGEROUS_EXTS = {
    ".pyc", ".pyo", ".so", ".o", ".a", ".dll", ".dylib", ".exe", ".bin", ".class",
    ".jar", ".wasm", ".zip", ".tar", ".gz", ".tgz", ".bz2", ".xz", ".7z", ".rar",
    ".dmg", ".pkg", ".node",
}


def parse_frontmatter(text: str, rel: str, errors: list[str]) -> dict | None:
    """Parse the YAML frontmatter with the SAME parser the skills ecosystem uses
    (PyYAML), so we catch YAML errors (e.g. an unquoted colon in the description)
    that would make the real CLI silently skip the skill."""
    m = re.match(r"^---\n(.*?)\n---\n", text, re.DOTALL)
    if not m:
        return None
    try:
        import yaml
    except ImportError:
        errors.append(f"{rel}: PyYAML not installed; run `pip install pyyaml` to validate frontmatter")
        return None
    try:
        data = yaml.safe_load(m.group(1))
    except yaml.YAMLError as e:
        errors.append(f"{rel}: frontmatter is not valid YAML ({e})")
        return None
    if not isinstance(data, dict):
        errors.append(f"{rel}: frontmatter did not parse to a mapping")
        return None
    return {k: str(v) for k, v in data.items()}


def check(skill_md: pathlib.Path, errors: list[str]) -> None:
    rel = str(skill_md.relative_to(ROOT))
    fm = parse_frontmatter(skill_md.read_text(encoding="utf-8"), rel, errors)
    if fm is None:
        if not any(rel in e for e in errors):
            errors.append(f"{rel}: missing or malformed YAML frontmatter")
        return
    name = fm.get("name", "")
    desc = fm.get("description", "")
    dirname = skill_md.parent.name

    if not name:
        errors.append(f"{rel}: frontmatter is missing `name`")
    else:
        if not NAME_RE.match(name):
            errors.append(f"{rel}: name '{name}' must be lowercase letters/digits/hyphens")
        if len(name) > 64:
            errors.append(f"{rel}: name '{name}' exceeds 64 chars")
        if name != dirname:
            errors.append(f"{rel}: name '{name}' must equal the parent directory '{dirname}'")
    if not desc:
        errors.append(f"{rel}: frontmatter is missing `description`")
    elif len(desc) > 1024:
        errors.append(f"{rel}: description is {len(desc)} chars (max 1024)")

    body = skill_md.read_text(encoding="utf-8")
    for ref in re.findall(r"`(references/[\w./-]+|scripts/[\w./-]+)`", body):
        if not (skill_md.parent / ref).exists():
            errors.append(f"{rel}: references `{ref}` which does not exist")


def check_no_dangerous_binaries(errors: list[str]) -> None:
    for f in ROOT.rglob("*"):
        if ".git" in f.parts or not f.is_file():
            continue
        if f.suffix.lower() in DANGEROUS_EXTS:
            errors.append(f"{f.relative_to(ROOT)}: committed executable/binary type "
                          f"'{f.suffix}' is not allowed (trust guard)")


def main() -> int:
    skill_files = sorted(ROOT.glob("skills/*/SKILL.md")) + sorted(ROOT.glob("skills/*/*/SKILL.md"))
    if not skill_files:
        print("no SKILL.md found under skills/")
        return 1
    errors: list[str] = []
    for f in skill_files:
        check(f, errors)
    check_no_dangerous_binaries(errors)
    if errors:
        print("INVALID:")
        for e in errors:
            print(f"  - {e}")
        return 1
    print(f"OK: {len(skill_files)} skill(s) valid")
    for f in skill_files:
        print(f"  - {f.relative_to(ROOT)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
