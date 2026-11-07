# Common campaign mistakes

## Extending time before identifying the bottleneck

**Wrong:** “The target found nothing; double its fuzz duration.”

**Better:** Inspect whether the intended producer and property were reached. A function outside the harness call graph needs a different entrypoint, while an unvisited reachable branch needs a different diagnosis. Fuzz Introspector explicitly separates static reachability from dynamic coverage ([official guide](https://google.github.io/oss-fuzz/advanced-topics/fuzz-introspector/)). More time remains an option when the lane is informative.

## Counting throughput as semantic progress

**Wrong:** Prefer the lane with the most inputs even when its intended operation rejects every one.

**Better:** Keep operation/property reach alongside speed and coverage. OSS-Fuzz's integration guidance asks for target progress, useful seeds and code coverage; its recommendations do not define execution count as the complete result ([integration guide](https://google.github.io/oss-fuzz/advanced-topics/ideal-integration/)).

## Multiplying identical workers without a search hypothesis

**Wrong:** Allocate all new compute to copies of the same configuration by default.

**Better:** Compare whether a complementary build, mutation or observation lane explores something distinct. AFL++ documents variation among cooperating instances; exact choices depend on the target ([depth guide, §3.c](https://aflplus.plus/docs/fuzzing_in_depth/)). This is not a universal requirement to split every small run.

## Treating raw failures as unique product defects

**Wrong:** “There are 100 crashes, therefore 100 bugs,” or “similar stacks prove one cause.”

**Better:** Preserve candidates and distinguish reproduced violations, verified duplicates, harness faults and unresolved cases. ClusterFuzz retains reproduction reliability, job, crash state and platform evidence for triage ([triage guide](https://google.github.io/clusterfuzz/using-clusterfuzz/workflows/triaging-new-crashes/)). LLM grouping is a hypothesis until evidence establishes the shared cause.

## Replaying only the seed

**Wrong:** Keep a random seed and summary while discarding the actual failing input, build and raw outputs.

**Better:** Keep the original case and configuration; include controlled decisions for any schedule/fault search. OSS-Fuzz reproduction uses actual testcase bytes and compatible sanitizer/architecture, not only a seed ([reproduction guide](https://google.github.io/oss-fuzz/advanced-topics/reproducing/)). A native input replay does not itself replay an external schedule.

## Confusing observation limits with product guarantees

**Wrong:** Treat a successful history check as every possible isolation property, or a timeout as proof of a product hang.

**Better:** State the selected model, recorded information and limit that ended the case. Elle's paper explicitly excludes predicate analysis; libFuzzer separately defines campaign and per-case resource controls ([Elle §9](https://arxiv.org/abs/2003.10554), [libFuzzer options](https://llvm.org/docs/LibFuzzer.html#options)). Investigate the actual violated contract.

## Declaring a winner from a lucky pilot

**Wrong:** One run found more coverage, so it is a proven better bugfinding method.

**Better:** Use a small pilot for a provisional allocation decision. If asserting comparative performance, retain matched repeated trials and variability; coverage is still distinct from confirmed defect yield ([FuzzBench report](https://google.github.io/fuzzbench/reference/report/)). Report zero findings honestly when that is the observation.
