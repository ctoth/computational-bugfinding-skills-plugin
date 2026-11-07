---
name: corpus-evolution
description: Evolves fuzzing corpora through purpose-specific selection, provenance and receiver-validated exchange. Use when importing seeds, minimizing an active corpus, converting generated representations, or retaining discoveries across harness and configuration changes.
---

# Corpus evolution

Make retained inputs useful to the receiving search and oracle. Coverage minimization selects for a measured target, while seed-selection value also depends on scheduling and preprocessing cost ([Rebert et al., §§2.2, 6.2–6.3](https://www.usenix.org/system/files/conference/usenixsecurity14/sec14-paper-rebert.pdf)).

## Establish purpose and compatibility

Read the actual producer, decoder, argument transport, build/configuration and assertion. Identify which material is original evidence, a durable regression, an unresolved candidate or an active search input. Use existing project conventions; this distinction does not require a new store or directory schema. A coverage selector's predicate is narrower than preservation of a particular failure ([libFuzzer corpus and options](https://llvm.org/docs/LibFuzzer.html)).

Before exchange, check input types, arity, encoding, starting state and enabled features on the receiver. Go corpus arguments are typed and ordered; construction-choice bytes are not the rendered source they produce ([Go corpus format](https://go.dev/doc/security/fuzz/)). Call the existing producer/serializer for conversion, retain its provenance, and verify a representative converted case reaches the receiving oracle. Read [exchange and replay](references/exchange-and-replay.md) for dependent cases.

## Select for the actual search

Keep originals and selected failure evidence available while creating an active subset. Choose coverage reduction, compatible incremental merge, or deliberate contract cases according to the intended observation. Do not interpret fewer files as greater semantic reach: native selectors retain measured coverage/features, and their result is target-dependent ([AFL++ preparation and coverage](https://aflplus.plus/docs/fuzzing_in_depth/), [libFuzzer merge](https://llvm.org/docs/LibFuzzer.html)).

Read [selection and retention](references/selection-and-retention.md) when deciding whether reduction is worth its cost. Measure acquisition, decoding/rendering, replay and selection as part of the authorized allocation; historical seed-selection results are not a universal smaller-is-better rule ([Rebert et al., §6.3](https://www.usenix.org/system/files/conference/usenixsecurity14/sec14-paper-rebert.pdf)). Use `bugfinding-campaign` for allocation and `failure-reduction` for preserving a selected violation while shrinking it.

## Run the selected native operation

Use the existing compatible instrumented target and check the installed tool's help/version against its selected release. Read only the relevant [conditional tool recipe](references/tool-recipes.md): AFL++ selection/merge, libFuzzer merge/replay, Go typed replay, or authorized OSS-Fuzz acquisition. The recipes state their predicate and output owner; they do not install a runtime or establish target applicability ([AFL++ preparation](https://aflplus.plus/docs/fuzzing_in_depth/), [OSS-Fuzz corpora](https://google.github.io/oss-fuzz/advanced-topics/corpora/)). Instrumentation and dictionaries belong to `coverage-guided-fuzzing`.

Check receiver results after imports and meaning-changing harness/generator/configuration changes. Preserve malformed, unsupported, excluded, unreached, completed and failing observations where they affect the conclusion. Go's generated cache and saved failure regressions have different execution roles; retaining one does not establish the other was preserved ([Go running and failing inputs](https://go.dev/doc/security/fuzz/)).

## Return useful evidence

Report what was acquired, converted, admitted and actually evaluated; selected output paths and provenance; coverage/semantic additions; preprocessing/replay cost; and retained failures or incompatibilities. Preserve expensive cases for resource/progress investigation rather than silently erase them from evidence. Separate active-set selection from cause-based deduplication; `evidence-based-triage` owns attribution. Read [common mistakes](references/common-mistakes.md) for misleading selection conclusions ([Rebert et al., §§6.1–6.3](https://www.usenix.org/system/files/conference/usenixsecurity14/sec14-paper-rebert.pdf)).

Invocation preserves the user's existing execution and publication scope. No storage service, universal corpus encoding or automatic acquisition account is required.
