# Common mistakes

## Pruning the only regression set with coverage minimization

**Wrong:** Run `afl-cmin` or `-merge=1` over the only regression/original set and keep only the output.

**Better:** Select a working subset into a separate destination while keeping the chosen failure evidence. Coverage merge and crash reduction have different predicates: `-merge=1` keeps inputs "that trigger new code coverage", while `-minimize_crash` "minimizes the provided crash input" ([libFuzzer, Options](https://raw.githubusercontent.com/llvm/llvm-project/635f30899dd0914fa89f0b3dc9a9e548e6d0ceec/llvm/docs/LibFuzzer.md)). By default `afl-cmin` also leaves crashing and timing-out inputs out of its output unless `-A` is given ([selected cmin source, usage](https://raw.githubusercontent.com/AFLplusplus/AFLplusplus/d0070729206a80a9af297b2341edd63f68fdac35/src/afl-cmin.c)).

**Why:** a coverage selector can silently discard the one input that reproduces a known failure.

## Renaming a byte-choice file for a string receiver

**Wrong:** Copy a `[]byte(...)` choice file into a fuzz test whose argument is `string` and edit the type name.

**Better:** Call the actual producer/serializer and replay the result. Go corpus "types must match the fuzzing arguments exactly, in that order" ([Go fuzzing, Corpus file format](https://raw.githubusercontent.com/golang/website/a8b66266e226994e2ead51317bace3ee83cedab9/_content/doc/security/fuzz/index.md)).

**Why:** the choice bytes are the generator's input, not the source text it renders.

## Treating copied seed count as receiver reach

**Wrong:** Report "imported 50,000 seeds" as the result of an exchange.

**Better:** Verify decoded input and intended property execution on the receiver. AFL++ calls `corpus count` "a bad indicator for checking how good the coverage is" ([AFL++ depth guide, §3g](https://raw.githubusercontent.com/AFLplusplus/AFLplusplus/d0070729206a80a9af297b2341edd63f68fdac35/docs/fuzzing_in_depth.md)).

**Why:** files the receiver rejects or never routes to the property add count without reach.

## Assuming the smallest coverage set always improves discovery

**Wrong:** Always minimize first because a smaller set must find more bugs.

**Better:** Account for preprocessing and scheduler-dependent results, and use a matched pilot. Under optimal scheduling the full set "will *always* find more, or the same amount of bugs", and selection's "benefits may not outweigh the costs" ([Rebert et al., §§6.2.2, 6.3](https://www.usenix.org/system/files/conference/usenixsecurity14/sec14-paper-rebert.pdf)).

**Why:** the benefit of reduction in that study depended on round-robin scheduling and on affordable coverage collection.

## Treating a component's remembered license as the whole tool's

**Wrong:** "AFL++ is Apache-2.0" (or "AGPL") applied to every binary and file.

**Better:** Check the selected revision's project and file-level scope. The project as a whole is AGPL-3.0-or-later, and the Apache-2.0 option applies to files "taken individually, not to the combined AGPL work" ([AFL++ licensing](https://raw.githubusercontent.com/AFLplusplus/AFLplusplus/d0070729206a80a9af297b2341edd63f68fdac35/LICENSING.md)).

**Why:** the license depends on which files a binary or reuse combines.

For this pack's workflow, explain why a case leaves the active set without erasing its original failure or resource evidence. Use `evidence-based-triage` for cause grouping and `failure-reduction` for witness-preserving simplification.
