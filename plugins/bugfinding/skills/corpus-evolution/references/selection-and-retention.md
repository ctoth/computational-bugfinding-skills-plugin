# Selection and retention

Treat these as this pack's corpus decisions, adapted to the project's existing artifacts. Native minimizers preserve their selected coverage/features; that is not a general claim about all behavioral differences ([AFL++ preparation](https://aflplus.plus/docs/fuzzing_in_depth/), [libFuzzer corpus](https://llvm.org/docs/LibFuzzer.html)).

| Purpose | Selection decision |
|---|---|
| Acquired/generated original | Retain provenance and the original when producing a working subset. |
| Confirmed regression or unresolved failure | Preserve the input and required witness/state independently of active-set selection. |
| Active discovery input | Select against the receiving target/configuration and actual useful reach. |
| Deliberate contract case | Retain when its distinct state/effect is demonstrated, even if the current coverage view is identical. |

The last row is a target-specific design choice, not proof that every coverage-equivalent input is semantically distinct. Record the observation that justifies its cost.

## Spend selection compute deliberately

Rebert et al. model seed reduction as set cover over measured blocks and examine scheduler-dependent results; their preprocessing example can exceed a short campaign's budget. Use that evidence to compare total cost, not to copy a historical corpus size or an omniscient schedule ([§§2.2, 6.2–6.3](https://www.usenix.org/system/files/conference/usenixsecurity14/sec14-paper-rebert.pdf)).

Record acquisition, decoding, baseline execution, selection and replay cost alongside actual property evaluations and discoveries. For an expensive source corpus, compare a bounded selection pilot with directly exploring a useful subset. Keep the denominators and tested property visible; the choice is provisional until observations support it.

When a slow input dominates, preserve it and determine whether it demonstrates a resource violation, valid costly behavior, or a harness problem. Route the contract to `resource-complexity-testing` or `liveness-testing`; active-set scheduling and evidence retention can differ. Do not redefine the product's resource contract to make the selection complete.

## Revisit meaning, not just filenames

After changes to generation, schema, decoding or enabled features, replay where meaning may change. A retired active input can remain an original or regression; explain its unsupported state or migration. For Go, preserve actual typed values and relevant generator identity rather than assume an opaque file still means the same thing ([Go corpus format](https://go.dev/doc/security/fuzz/)).
