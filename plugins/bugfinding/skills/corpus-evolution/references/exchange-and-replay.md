# Exchange and replay

Go requires corpus values to match target argument types and order. A byte-choice generator and a string-source target therefore need an actual producer conversion, not a renamed file ([Go corpus format](https://go.dev/doc/security/fuzz/)).

## Verify the receiving operation

Inspect its decoder, setup/reset boundary, enabled configuration, resource limits and oracle. Keep the original representation, producer/version, rendered artifact and actual receiver result together where they are required for replay. Use existing metadata conventions instead of introducing a mandatory corpus manifest.

This pack's illustrative conversion: an established IR generator maps choice bytes to source, while a comparison lane consumes one encoded source string. Call the existing generator and the receiver's serializer. Trace one converted case through admission, execution and comparison before bulk import. Keep exclusions visible. A compiling export does not by itself show that the intended effect was observed.

If a case depends on world construction or an operation prefix, retain that dependency rather than exchange its last message alone. `semantic-program-generation` and `stateful-property-testing` own those producers; `semantic-differential-testing` owns equivalent starting states. Compatible queue exchange is an engine feature, not proof of semantic compatibility between arbitrary harnesses ([AFL++ multiple cores](https://aflplus.plus/docs/fuzzing_in_depth/)).

## Interpret receiver evidence

Keep separate facts when useful: decoded, admitted, reached the intended operation, evaluated the property, and preserved the selected feature or failure. Recompute receiver measurements instead of transferring feature IDs across different instrumented builds. Same-format transfer in the seed-selection study concerns observed coverage, not assured future bug yield ([Rebert et al., §6.3](https://www.usenix.org/system/files/conference/usenixsecurity14/sec14-paper-rebert.pdf)).

Illustrative worked decision: two permission/lifetime sequences exercise the same measured branches but establish demonstrably different contract states. Keep representatives for the relevant effect oracle, and record their replay cost. Do not invent semantic diversity from file names or retain every duplicate indefinitely.

For long-lived shared queues, preserve lane identity and exact input representation. A dictionary token is a mutation hint rather than a complete receiving testcase; let `coverage-guided-fuzzing` verify its selected engine syntax and measure whether it unlocks useful paths ([AFL++ dictionaries](https://aflplus.plus/docs/fuzzing_in_depth/)).
