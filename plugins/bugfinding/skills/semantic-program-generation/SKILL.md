---
name: semantic-program-generation
description: Guides semantic program generators that carry types, live objects, effects and required starting state. Use when grammar-valid fuzz inputs rarely reach successful behavior, or when programs and their worlds must be generated and shrunk together.
---

# Semantic program generation

Generate the prerequisites of the behavior being checked. A source program can be syntactically valid while lacking the object, range, lifetime or effect relationships needed for a useful execution. Csmith interleaves generation with environment and safety analysis; SQLite's joint database-and-SQL mutation supplies a state-plus-program precedent ([Csmith, §§2.2–2.5](https://users.cs.utah.edu/~regehr/papers/pldi11-preprint.pdf), [SQLite testing, §4.1.3](https://www.sqlite.org/testing.html)).

## Choose the intended semantic lane

Read the actual language/API contract, enabled configuration and existing generator/executor. Separate malformed-input robustness, specified runtime errors and successful semantic operations. Preserve useful error lanes; add a successful-path lane when rejection prevents evaluating the intended guarantee. Csmith's defined-behavior restrictions serve its compiler-comparison oracle, not every language or robustness target ([Csmith, §§2.1–2.4](https://users.cs.utah.edu/~regehr/papers/pldi11-preprint.pdf)).

Count existing structured generation as baseline. An advance might establish a live receiver and permitted mutation, combine initial data with a program, or generate a legal alias/effect interaction. It is not simply another grammar. Select only the additional relationships needed for the target guarantee ([Csmith, §§2.3–2.5](https://users.cs.utah.edu/~regehr/papers/pldi11-preprint.pdf), [SQLite testing, §4.1.3](https://www.sqlite.org/testing.html)).

## Construct prerequisites through existing owners

Use the target's maintained AST/IR, formatter and supported world/fixture creation paths. Keep a small generation environment: initialized variables and ranges, live identities, available definitions, permissions/capabilities and relevant read/write effects. Select valid operands from those facts or create their prerequisites before use. Csmith's generation context and dependent-domain combinators illustrate these mechanisms; they do not require porting a whole analyzer ([Csmith, §2.3](https://users.cs.utah.edu/~regehr/papers/pldi11-preprint.pdf), [FuzzTest domains](https://raw.githubusercontent.com/google/fuzztest/main/doc/domains-reference.md)).

Update or invalidate facts after mutations and control-flow joins. A fragment safe at construction can become unsafe after a loop backedge or call changes reachable state; re-establish the relevant facts at that boundary. Do not preserve a stale permission, lifetime or index assumption merely because its expression once compiled ([Csmith, §§2.4–2.5](https://users.cs.utah.edu/~regehr/papers/pldi11-preprint.pdf)). For decisions and a world-effect example, read [semantic environments](references/semantic-environments.md).

## Search useful interactions

Vary target-supported aliasing, state-dependent dispatch, exception effects and boundary values while retaining the lane's validity conditions. Record construction/compile success separately from entry into the intended operation, completion of its effect and evaluation of the oracle. Feature interactions and coverage are different observations; avoid optimizing only syntax variety or execution counts ([Csmith, §§2.2, 3.3 and 3.5](https://users.cs.utah.edu/~regehr/papers/pldi11-preprint.pdf)).

Use `correctness-oracles` to establish the result/effect discriminator, `harness-sensitivity` to test its discrimination, and `coverage-guided-fuzzing` for the chosen runtime's execution mechanics. This skill owns program construction; `stateful-property-testing` owns general API-sequence models. Read [tool choices](references/tool-choices.md) only for a compatible C/C++ generator/domain integration.

## Retain and shrink the semantic case

Preserve generation choices, rendered program, initial-world/setup construction, selected semantics/configuration and raw witness. Reduce dependencies together, regenerate through the same owner and check that the selected operation still reaches the same violated guarantee. Wrong-code reduction can introduce undefined behavior; a smaller error or mismatch need not preserve the original finding ([Csmith, §4](https://users.cs.utah.edu/~regehr/papers/pldi11-preprint.pdf)).

Read [world/program replay](references/world-program-replay.md) for dependency-aware moves and a concrete experiment. Route reducer algorithms and attribution to `failure-reduction` and `evidence-based-triage`. Report actual successful property reach, excluded/rejected cases, replay evidence and remaining validity assumptions; do not infer discovery yield from the generator's existence ([Csmith, §§3.3, 3.5 and 4](https://users.cs.utah.edu/~regehr/papers/pldi11-preprint.pdf)). For misleading constructions, read [common mistakes](references/common-mistakes.md).
