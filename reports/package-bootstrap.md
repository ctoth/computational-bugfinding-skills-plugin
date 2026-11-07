# Computational bugfinding package bootstrap

## State

Local repository and manifest bootstrap complete for the approved marketplace and one `bugfinding` plugin. No publication, installation or remote repository is authorized.

## Evidence

- The intended target directory did not exist before bootstrap.
- No `AGENTS.md` file exists at the probed ancestors `C:/Users/Q/code`, `C:/Users/Q`, `C:/Users` or `C:/`.
- Read the actual sibling Go marketplace manifests at `C:/Users/Q/code/golang-skills-plugin/.claude-plugin/marketplace.json` and `.agents/plugins/marketplace.json`, and both host manifests under `plugins/golang/`.
- The sibling establishes local plugin sources, a Claude marketplace owner field, and Codex plugin `skills` ownership. No remote URL or license will be inferred from that sibling.

## Canonical paths

- Domain research: `reports/skill-research-computational-bugfinding.md`.
- Approved plan: `reports/skill-plan-computational-bugfinding.md`.
- Living task note: `agent-notes/computational-bugfinding-marketplace.md`.
- Skill owner: `plugins/bugfinding/skills/`.

The three task documents were moved with the editing tool; no second copy remains at the old task paths. Existing papers remain at `C:/Users/Q/code/papers/` and are not distributed dependencies.

## Primary packaging documentation

- [Claude marketplace creation](https://code.claude.com/docs/en/plugin-marketplaces), accessed 2026-11-07: requires marketplace name, owner and plugin entries with name/source; source paths are rooted at the marketplace directory. The existing user identification Q supplies the required local owner name; no contact or remote identity is invented.
- [Claude manifest reference](https://code.claude.com/docs/en/plugins-reference), accessed 2026-11-07: default `skills/` is discovered at plugin root; `.claude-plugin/plugin.json` supplies metadata. The actual installed `claude plugin validate --help` exposes manifest validation without installation.
- [OpenAI plugin packaging](https://developers.openai.com/plugins/build/plugins), accessed 2026-11-07: the former Codex build URL redirects here. Local marketplaces use `.agents/plugins/marketplace.json`, with relative plugin sources and installation/authentication policies. The documented portable format now uses root `plugin.json`; `.codex-plugin/plugin.json` remains a compatibility fallback. Bootstrap preserves the approved compatibility layout rather than silently adding another manifest. No OpenAI host validation is claimed from JSON parsing.
- Installed `codex plugin --help` exposes add/list/marketplace/remove/help; no validation subcommand. The searched installed cache has no plugin-validator script matching the probed names.

## Validation evidence

Commands executed at repository root:

```text
git init -b main
claude plugin validate . --json
claude plugin validate ./plugins/bugfinding --json
```

Both Claude reports returned `success: true`, zero manifest errors and exit 0. Both warn that author information is absent; optional author/contact details are intentionally not invented. The plugin report separately emits directory-submission findings: `README_MISSING` and `LICENSE_MISSING` are blocking for that directory profile; `ICON_MISSING` is a warning. No `--profile directory` or `--strict` claim is made. This is local manifest validation, not public-directory submission readiness. No license was chosen and no icon or README was added to satisfy an unrequested public submission.

The two Codex manifests parsed through PowerShell `ConvertFrom-Json`. The marketplace has one local `bugfinding` entry, and both hosts point to existing `./plugins/bugfinding`. Codex plugin version is `0.1.0` and its skills path is `./skills/`. The canonical skills directory is deliberately owned by the foundation drafter and did not yet exist at bootstrap validation; component-level validation must follow drafting. Codex host loading and installation were not performed.

`git rev-parse --show-toplevel` initially returned “not a git repository”; `.git` was absent. `git init -b main` then created the local repository. No remote was configured.

## Next step

Separate agents research and draft the foundation and remaining skills. Re-run component validation after their skill files exist; audit the complete collection and evaluate behavior before reporting the plugin complete.
