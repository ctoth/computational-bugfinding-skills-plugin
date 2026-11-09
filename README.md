# Computational Bugfinding

25 agent skills for finding and reproducing software defects through executable correctness checks, generated workloads, controlled search, and evidence-based triage.

Start with `bugfinding-campaign` to inspect an existing test setup and choose a useful search direction. Use a specialist to design or extend the experiment, then reduce and investigate its failures. Each skill includes method guidance and references to primary sources; these are agent instructions, not bundled fuzzers or a test runner.

## Install

### Claude Code

In a Claude Code session:

```text
/plugin marketplace add ctoth/computational-bugfinding-skills-plugin
/plugin install bugfinding@computational-bugfinding-marketplace
```

For a local checkout, replace the repository slug with its absolute path.

### Codex

```text
codex plugin marketplace add ctoth/computational-bugfinding-skills-plugin
codex plugin add bugfinding@computational-bugfinding-marketplace
```

The first command registers the catalog; the second installs the plugin. For a local checkout, replace the repository slug with its absolute path.

## Use

Ask your agent to use a skill by name, for example:

- “Use bugfinding-campaign to find gaps in this project's existing fuzzing setup.”
- “Use correctness-oracles to check whether this harness observes state changes as well as return values.”
- “Use failure-reduction and evidence-based-triage to investigate this counterexample.”

In Claude Code, invoke the entry point directly with `/bugfinding:bugfinding-campaign`.

Skills guide the agent to read the target's actual code and guarantees, establish an executable observation, search within the authorized resource budget, and preserve replay evidence. Tool installation, target changes, paid compute, production fault injection, and publication remain subject to the user's authorization. Individual tool routes depend on the target's language, platform, and build.

## Skills

| Skill | Focus |
|---|---|
| [bugfinding-campaign](plugins/bugfinding/skills/bugfinding-campaign/SKILL.md) | Inspect current capabilities, choose a search gap, and allocate compute from observed results. |
| [correctness-oracles](plugins/bugfinding/skills/correctness-oracles/SKILL.md) | Turn actual guarantees into executable observations. |
| [harness-sensitivity](plugins/bugfinding/skills/harness-sensitivity/SKILL.md) | Check that a harness reaches relevant behavior and detects representative violations. |
| [stateful-property-testing](plugins/bugfinding/skills/stateful-property-testing/SKILL.md) | Generate dependent API and protocol operation sequences. |
| [semantic-program-generation](plugins/bugfinding/skills/semantic-program-generation/SKILL.md) | Generate programs with the types, objects, effects, and initial state they need. |
| [semantic-differential-testing](plugins/bugfinding/skills/semantic-differential-testing/SKILL.md) | Compare implementations and execution modes under matched semantic conditions. |
| [metamorphic-testing](plugins/bugfinding/skills/metamorphic-testing/SKILL.md) | Derive valid relations between transformed executions. |
| [coverage-guided-fuzzing](plugins/bugfinding/skills/coverage-guided-fuzzing/SKILL.md) | Configure instrumented search, reset, and replay for supported runtimes. |
| [corpus-evolution](plugins/bugfinding/skills/corpus-evolution/SKILL.md) | Select, retain, convert, and exchange useful search inputs. |
| [native-memory-instrumentation](plugins/bugfinding/skills/native-memory-instrumentation/SKILL.md) | Observe native memory defects through sanitizers and Memcheck. |
| [race-detection-campaigns](plugins/bugfinding/skills/race-detection-campaigns/SKILL.md) | Exercise shared-memory access and object lifetimes under race detectors. |
| [schedule-exploration](plugins/bugfinding/skills/schedule-exploration/SKILL.md) | Search controlled interleavings and preserve replay choices. |
| [linearizability-checking](plugins/bugfinding/skills/linearizability-checking/SKILL.md) | Check concurrent object histories against sequential specifications. |
| [transactional-history-testing](plugins/bugfinding/skills/transactional-history-testing/SKILL.md) | Generate informative transaction histories and check isolation with Elle. |
| [distributed-fault-testing](plugins/bugfinding/skills/distributed-fault-testing/SKILL.md) | Exercise real deployments under network, process, and clock faults. |
| [deterministic-simulation](plugins/bugfinding/skills/deterministic-simulation/SKILL.md) | Search reproducible failures through existing supported simulators. |
| [crash-consistency-testing](plugins/bugfinding/skills/crash-consistency-testing/SKILL.md) | Check persistence and recovered state across crashes and storage faults. |
| [symbolic-concolic-execution](plugins/bugfinding/skills/symbolic-concolic-execution/SKILL.md) | Solve hard path constraints and replay candidates against real execution. |
| [bounded-model-checking](plugins/bugfinding/skills/bounded-model-checking/SKILL.md) | Check finite domains with explicit models, bounds, and counterexamples. |
| [resource-complexity-testing](plugins/bugfinding/skills/resource-complexity-testing/SKILL.md) | Search for excessive CPU, allocation, retention, and handle growth. |
| [liveness-testing](plugins/bugfinding/skills/liveness-testing/SKILL.md) | Investigate deadlock, starvation, livelock, and unbounded retries. |
| [configuration-differential-testing](plugins/bugfinding/skills/configuration-differential-testing/SKILL.md) | Search constrained build, runtime, and capability combinations. |
| [numerical-oracles](plugins/bugfinding/skills/numerical-oracles/SKILL.md) | Test numerical accuracy, rounding, and special values with suitable references. |
| [failure-reduction](plugins/bugfinding/skills/failure-reduction/SKILL.md) | Shrink counterexamples while preserving the violation and valid setup. |
| [evidence-based-triage](plugins/bugfinding/skills/evidence-based-triage/SKILL.md) | Separate demonstrated defects, harness problems, expected behavior, and unresolved cases. |

## Layout and evidence

Both hosts load the same files under `plugins/bugfinding/skills/`. Claude uses `.claude-plugin/marketplace.json` and the plugin's `.claude-plugin/plugin.json`; Codex uses `.agents/plugins/marketplace.json` and the plugin's `.codex-plugin/plugin.json`.

Each skill's `references/` directory holds detailed guidance and a `sources.yaml` inventory. `reports/` contains research, drafting, audit, and evaluation records. The separate local papers and evaluation workspaces are not required to install the plugin.

The [local evidence integration report](reports/final-integration.md) describes two seeded behavioral evaluations and their limits. They do not establish improved discovery yield on real projects or behavioral coverage of all skills. Audit reports describe their recorded snapshots; subsequent source changes are not covered automatically.

## CI

[GitHub Actions](https://github.com/ctoth/computational-bugfinding-skills-plugin/actions/workflows/ci.yml) checks pull requests and pushes to `main` in one Linux job:

- Both marketplace catalogs and plugin manifests, including source paths and matching identities.
- Skill YAML frontmatter, directory names, descriptions, and nonempty bodies.
- Source inventory YAML and URL structure, plus bundled Markdown file links.
- Workflow syntax with actionlint and workflow security with zizmor in offline mode.

The package check is `uv run --no-project --script scripts/check_package.py`. It does not fetch citation URLs, check citation entailment, execute the referenced bugfinding tools, or establish host loading compatibility.

## License

[MIT](LICENSE).
