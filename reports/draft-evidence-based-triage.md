# Draft: evidence-based-triage

## State

Draft complete and focused structural validation passed. This report and the named skill directory are the only owned outputs. No target execution, installation, publishing or remote operation occurred.

## Evidence

Read the approved scope, completed research, foundation skill and relevant primary sources. Wrote the portable audit entrypoint plus triage-decisions, maintainer-handoff, common-mistakes and sources inventory. No executable helper, verdict database or generic investigation protocol was added.

- Reread primary ClusterFuzz triage/glossary, OSS-Fuzz reproduction, Go failure/replay, libFuzzer limitations and LLVM maintainer guidance.
- Reread actual OSS-Fuzz-Gen crash/semantic analyzer source; stored LLM booleans remain classifier outputs, not independent confirmation.
- Directly reread processed Elle page images 7, 9 and 12. No new ingestion was started. Latest Q instruction uses paper-reader only; no paper-process/tag/reconcile workflow was run by this drafter.

## Next step

Parent granted the serialized commit slot. Exact owned paths were staged; staged inventory contained five skill files and the two named reports only, and `git diff --cached --check` returned no output. Commit this scoped draft, then parent performs collection/behavior review. No task note, plan or other agent's report is staged.

## Focused validation

Executed from the repository root:

```text
python C:/Users/Q/.codex/skills/.system/skill-creator/scripts/quick_validate.py plugins/bugfinding/skills/evidence-based-triage
Skill is valid!

python -c "from pathlib import Path; import re,yaml; from urllib.parse import urldefrag; p=Path('plugins/bugfinding/skills/evidence-based-triage'); inventory=yaml.safe_load((p/'references/sources.yaml').read_text())['sources']; urls={s['url'] for s in inventory}; errors=[]; cited=set(); files=list(p.rglob('*.md')); [(cited.add(urldefrag(u)[0]) if u.startswith('https://') else errors.append(str(f)+': missing '+u) if not (f.parent/u.split('#')[0]).exists() else None) for f in files for u in re.findall(r'\]\(([^)]+)\)',f.read_text())]; errors.extend('orphan source: '+u for u in cited-urls); errors.extend('unused inventory: '+u for u in urls-cited); print('Sources:',len(urls)); print('Line counts:', {str(f.relative_to(p)):len(f.read_text().splitlines()) for f in files}); print('Link/source errors:',errors); raise SystemExit(bool(errors))"
Sources: 9
Line counts: SKILL.md 35; common-mistakes.md 12; maintainer-handoff.md 22; triage-decisions.md 25
Link/source errors: []

git diff --check -- plugins/bugfinding/skills/evidence-based-triage reports/draft-evidence-based-triage.md reports/research-evidence-based-triage.md
[no output]
```

The inline probe parses YAML, checks every local Markdown link and matches each inline primary URL to its inventory owner, ignoring anchors. This is structural/provenance ownership validation, not proof that every external anchor remains valid, that citations entail every sentence, or that an LLM triages accurately. Primary docs/source and the selected Elle images were read directly as stated above. No independent behavioral evaluation, target campaign, measured LLM accuracy or empirical discovery-yield claim is made. Portable frontmatter deliberately leaves host-specific fork/agent orchestration to the invoking host.
