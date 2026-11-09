---
name: corpus-evolution
description: Evolves fuzzing corpora through purpose-specific selection, provenance and receiver-validated exchange. Use when importing seeds, minimizing an active corpus, converting generated representations, or retaining discoveries across harness and configuration changes, including Jazzer.js corpora and V8 coverage selection for Node.js.
---

# Corpus evolution

Make retained inputs useful to the receiving search and oracle. Coverage minimization selects for a measured target, while seed-selection value also depends on scheduling and preprocessing cost: selection's "benefits may not outweigh the costs" ([Rebert et al., §§2.2, 6.2–6.3](https://www.usenix.org/system/files/conference/usenixsecurity14/sec14-paper-rebert.pdf)).

## Establish purpose and compatibility

Read the actual producer, decoder, argument transport, build/configuration and assertion. Identify which material is original evidence, a durable regression, an unresolved candidate or an active search input. Use existing project conventions; this distinction does not require a new store or directory schema. A coverage selector's predicate is narrower than preservation of a particular failure: libFuzzer merge keeps inputs "that trigger new code coverage" ([libFuzzer, Options `-merge`](https://raw.githubusercontent.com/llvm/llvm-project/635f30899dd0914fa89f0b3dc9a9e548e6d0ceec/llvm/docs/LibFuzzer.md)).

Before exchange, check input types, arity, encoding, starting state and enabled features on the receiver. Go corpus entries must have types "identical to the fuzzing arguments, in the same order", so construction-choice bytes are not the rendered source they produce ([Go fuzzing, Requirements and Corpus file format](https://raw.githubusercontent.com/golang/website/a8b66266e226994e2ead51317bace3ee83cedab9/_content/doc/security/fuzz/index.md)). Call the existing producer/serializer for conversion, retain its provenance, and verify a representative converted case reaches the receiving oracle. Read [exchange and replay](references/exchange-and-replay.md) for dependent cases.

## Select for the actual search

Keep originals and selected failure evidence available while creating an active subset. Choose coverage reduction, compatible incremental merge, or deliberate contract cases according to the intended observation. Do not interpret fewer files as greater semantic reach: native selectors retain measured coverage/features, and their result is target-dependent. AFL++ calls `corpus count` "a bad indicator for checking how good the coverage is", and libFuzzer merge minimizes "while still preserving the full coverage" ([AFL++ depth guide, §§2b, 3g](https://raw.githubusercontent.com/AFLplusplus/AFLplusplus/d0070729206a80a9af297b2341edd63f68fdac35/docs/fuzzing_in_depth.md), [libFuzzer, Corpus](https://raw.githubusercontent.com/llvm/llvm-project/635f30899dd0914fa89f0b3dc9a9e548e6d0ceec/llvm/docs/LibFuzzer.md)).

Read [selection and retention](references/selection-and-retention.md) when deciding whether reduction is worth its cost. Measure acquisition, decoding/rendering, replay and selection as part of the authorized allocation; historical seed-selection results are not a universal smaller-is-better rule ([Rebert et al., §6.3](https://www.usenix.org/system/files/conference/usenixsecurity14/sec14-paper-rebert.pdf)). Use `bugfinding-campaign` for allocation and `failure-reduction` for preserving a selected violation while shrinking it.

## Run the selected native operation

Use the existing compatible instrumented target and check the installed tool's help/version against its selected release. Read only the relevant [conditional tool recipe](references/tool-recipes.md): AFL++ selection/merge, libFuzzer merge/replay, Jazzer.js (Node.js) corpus and regression directories, Go typed replay, or authorized OSS-Fuzz acquisition. The recipes state their predicate and output owner; they do not install a runtime or establish target applicability. Instrumentation and dictionaries belong to `coverage-guided-fuzzing`.

Check receiver results after imports and meaning-changing harness/generator/configuration changes. Preserve malformed, unsupported, excluded, unreached, completed and failing observations where they affect the conclusion. Go's generated cache and saved failure regressions have different execution roles: generated entries "are only used while fuzzing", while a saved failing input is run "by default with `go test`". Retaining one does not establish the other was preserved ([Go fuzzing, Failing input and Glossary](https://raw.githubusercontent.com/golang/website/a8b66266e226994e2ead51317bace3ee83cedab9/_content/doc/security/fuzz/index.md)).

## Return useful evidence

Report what was acquired, converted, admitted and actually evaluated; selected output paths and provenance; coverage/semantic additions; preprocessing/replay cost; and retained failures or incompatibilities. Preserve expensive cases for resource/progress investigation rather than silently erase them from evidence. Separate active-set selection from cause-based deduplication; `evidence-based-triage` owns attribution. In the seed-selection study, 2,702 apparent unique crashes came from one overflow that "confused BFF's stack-based uniqueness algorithm". Read [common mistakes](references/common-mistakes.md) for misleading selection conclusions ([Rebert et al., §§6.1–6.3](https://www.usenix.org/system/files/conference/usenixsecurity14/sec14-paper-rebert.pdf)).

Invocation preserves the user's existing execution and publication scope. No storage service, universal corpus encoding or automatic acquisition account is required.
