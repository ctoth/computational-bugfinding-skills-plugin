# Selection and retention

Treat these as this pack's corpus decisions, adapted to the project's existing artifacts. Native minimizers preserve their selected coverage/features; that is not a general claim about all behavioral differences. `afl-cmin` removes inputs "that do not produce a new path/coverage in the target", and libFuzzer `-merge=1` adds only "inputs that trigger new coverage" ([AFL++ depth guide, §2b](https://raw.githubusercontent.com/AFLplusplus/AFLplusplus/d0070729206a80a9af297b2341edd63f68fdac35/docs/fuzzing_in_depth.md), [libFuzzer, Corpus](https://raw.githubusercontent.com/llvm/llvm-project/635f30899dd0914fa89f0b3dc9a9e548e6d0ceec/llvm/docs/LibFuzzer.md)).

| Purpose | Selection decision |
|---|---|
| Acquired/generated original | Retain provenance and the original when producing a working subset. |
| Confirmed regression or unresolved failure | Preserve the input and required witness/state independently of active-set selection. |
| Active discovery input | Select against the receiving target/configuration and actual useful reach. |
| Deliberate contract case | Retain when its distinct state/effect is demonstrated, even if the current coverage view is identical. |

The last row is a target-specific design choice, not proof that every coverage-equivalent input is semantically distinct. Record the observation that justifies its cost.

## Spend selection compute deliberately

Rebert et al. model seed reduction as set cover over measured code blocks ([§2](https://www.usenix.org/system/files/conference/usenixsecurity14/sec14-paper-rebert.pdf)). Their results depend on the scheduler: under optimal scheduling "the full set will *always* find more, or the same amount of bugs", while under round-robin the reduced set did better. Their preprocessing example, 368 CPU-days to collect coverage for one JPG bucket, can exceed a campaign's budget. Use that evidence to compare total cost, not to copy a historical corpus size or an omniscient schedule ([§§6.2.2, 6.3](https://www.usenix.org/system/files/conference/usenixsecurity14/sec14-paper-rebert.pdf)).

Record acquisition, decoding, baseline execution, selection and replay cost alongside actual property evaluations and discoveries. For an expensive source corpus, compare a bounded selection pilot with directly exploring a useful subset. Keep the denominators and tested property visible; the choice is provisional until observations support it.

When a slow input dominates, preserve it and determine whether it demonstrates a resource violation, valid costly behavior, or a harness problem. Route the contract to `resource-complexity-testing` or `liveness-testing`; active-set scheduling and evidence retention can differ. Do not redefine the product's resource contract to make the selection complete.

## Revisit meaning, not just filenames

After changes to generation, schema, decoding or enabled features, replay where meaning may change. A retired active input can remain an original or regression; explain its unsupported state or migration. For Go, preserve actual typed values and relevant generator identity rather than assume an opaque file still means the same thing; a corpus file's first line records "the file's encoding version" ([Go fuzzing, Corpus file format](https://raw.githubusercontent.com/golang/website/a8b66266e226994e2ead51317bace3ee83cedab9/_content/doc/security/fuzz/index.md)).
