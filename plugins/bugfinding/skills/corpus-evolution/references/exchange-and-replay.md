# Exchange and replay

Go requires corpus values to match target argument types and order: "These types must match the fuzzing arguments exactly, in that order." A byte-choice generator and a string-source target therefore need an actual producer conversion, not a renamed file. For raw binary seeds, the documented `file2fuzz` tool converts files "to corpus files encoded for `[]byte`"; it does not produce a `string` or multi-argument entry ([Go fuzzing, Corpus file format](https://raw.githubusercontent.com/golang/website/a8b66266e226994e2ead51317bace3ee83cedab9/_content/doc/security/fuzz/index.md)).

## Verify the receiving operation

Inspect its decoder, setup/reset boundary, enabled configuration, resource limits and oracle. Keep the original representation, producer/version, rendered artifact and actual receiver result together where they are required for replay. Use existing metadata conventions instead of introducing a mandatory corpus manifest.

This pack's illustrative conversion: an established IR generator maps choice bytes to source, while a comparison lane consumes one encoded source string. Call the existing generator and the receiver's serializer. Trace one converted case through admission, execution and comparison before bulk import. Keep exclusions visible. A compiling export does not by itself show that the intended effect was observed.

If a case depends on world construction or an operation prefix, retain that dependency rather than exchange its last message alone. `semantic-program-generation` and `stateful-property-testing` own those producers; `semantic-differential-testing` owns equivalent starting states. Compatible queue exchange is an engine feature, not proof of semantic compatibility between arbitrary harnesses: AFL++ syncs a foreign queue by showing the main fuzzer "the `-F` option where the queue/work directory of a different fuzzer is" ([AFL++ depth guide, §3c](https://raw.githubusercontent.com/AFLplusplus/AFLplusplus/d0070729206a80a9af297b2341edd63f68fdac35/docs/fuzzing_in_depth.md)).

## Interpret receiver evidence

Keep separate facts when useful: decoded, admitted, reached the intended operation, evaluated the property, and preserved the selected feature or failure. Recompute receiver measurements instead of transferring feature IDs across different instrumented builds. Same-format transfer in the seed-selection study concerns observed coverage, not assured future bug yield: reduced sets transfer "with respect to code coverage" ([Rebert et al., §6.3](https://www.usenix.org/system/files/conference/usenixsecurity14/sec14-paper-rebert.pdf)).

Illustrative worked decision: two permission/lifetime sequences exercise the same measured branches but establish demonstrably different contract states. Keep representatives for the relevant effect oracle, and record their replay cost. Do not invent semantic diversity from file names or retain every duplicate indefinitely.

For long-lived shared queues, preserve lane identity and exact input representation. A dictionary token is a mutation hint rather than a complete receiving testcase: libFuzzer dictionaries hold "input language keywords or other interesting byte sequences", and AFL++ loads one with `-x` ([libFuzzer, Dictionaries](https://raw.githubusercontent.com/llvm/llvm-project/635f30899dd0914fa89f0b3dc9a9e548e6d0ceec/llvm/docs/LibFuzzer.md), [AFL++ depth guide, §3a](https://raw.githubusercontent.com/AFLplusplus/AFLplusplus/d0070729206a80a9af297b2341edd63f68fdac35/docs/fuzzing_in_depth.md)). Let `coverage-guided-fuzzing` verify its selected engine syntax and measure whether it unlocks useful paths.
