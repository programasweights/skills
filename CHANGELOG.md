# Changelog

All notable changes to the ProgramAsWeights agent skill are documented here. This project
follows [Semantic Versioning](https://semver.org/).

## 0.1.0

Initial polished release.

- **Skill:** `SKILL.md` (trigger + compile -> test -> iterate workflow) plus on-demand
  `references/` (api, writing-good-specs, browser-sdk, troubleshooting).
- **Script-free:** the eval loop is embedded as a copy-pasteable recipe in `SKILL.md`
  instead of a bundled executable, to minimize attack surface and maximize trust.
- **Trust:** added `SECURITY.md`, a per-skill `LICENSE.txt`, and a documented data-flow.
- **Packaging (present but not yet distributed to any directory):** Codex plugin
  (`.codex-plugin/plugin.json`) + Codex marketplace (`.agents/plugins/marketplace.json`),
  Claude plugin (`.claude-plugin/plugin.json`) + Claude marketplace
  (`.claude-plugin/marketplace.json`), and brand assets (`assets/`).
- **CI:** validates frontmatter (name/description, name==dir, description <= 1024),
  reference paths, trigger coverage, and rejects committed executable binaries.
