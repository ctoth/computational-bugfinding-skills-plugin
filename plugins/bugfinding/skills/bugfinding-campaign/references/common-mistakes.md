# Common campaign mistakes

## Extending time before identifying the bottleneck

**Wrong:** “The target found nothing; double its fuzz duration.”

**Better:** Inspect whether the intended producer and property were reached. A function outside the harness call graph needs a different entrypoint, while an unvisited reachable branch needs a different diagnosis. Fuzz Introspector explicitly compares "static reachability potential" against dynamic coverage ([Fuzz Introspector, overview](https://raw.githubusercontent.com/google/oss-fuzz/156f862e5976b3d23828230a0a5b4fef54074d32/docs/advanced-topics/fuzz_introspector.md)). More time remains an option when the lane is informative.

**Why:** mutation time cannot reach code outside the harness's call graph.

## Counting throughput as semantic progress

**Wrong:** Prefer the lane with the most inputs even when its intended operation rejects every one.

**Better:** Keep operation/property reach alongside speed and coverage. OSS-Fuzz's integration guidance asks for target progress, useful seeds and code coverage ("it must have good coverage in the code that it is testing"); its recommendations do not define execution count as the complete result ([OSS-Fuzz integration, Fuzz Target, Seed Corpus and Coverage](https://raw.githubusercontent.com/google/oss-fuzz/156f862e5976b3d23828230a0a5b4fef54074d32/docs/advanced-topics/ideal_integration.md)).

**Why:** an input that is rejected before the intended operation evaluates no property, however fast it runs.

## Multiplying identical workers without a search hypothesis

**Wrong:** Allocate all new compute to copies of the same configuration by default.

**Better:** Compare whether a complementary build, mutation or observation lane explores something distinct. AFL++ documents variation among cooperating instances ("For every secondary fuzzer there should be a variation"); exact choices depend on the target ([AFL++ depth, §3.c Using multiple cores](https://raw.githubusercontent.com/AFLplusplus/AFLplusplus/d0070729206a80a9af297b2341edd63f68fdac35/docs/fuzzing_in_depth.md)). This is not a universal requirement to split every small run.

**Why:** identical copies repeat one search strategy; a distinct lane can reach what that strategy misses.

## Treating raw failures as unique product defects

**Wrong:** “There are 100 crashes, therefore 100 bugs,” or “similar stacks prove one cause.”

**Better:** Preserve candidates and distinguish reproduced violations, verified duplicates, harness faults and unresolved cases. ClusterFuzz retains reproduction reliability, job, crash state and platform evidence for triage ([ClusterFuzz triage, Filtering testcases and Crash statistics](https://raw.githubusercontent.com/google/clusterfuzz/77bbad2432fb931906c523786defac928d12afdb/docs/using-clusterfuzz/workflows/triaging-new-crashes.md)). LLM grouping is a hypothesis until evidence establishes the shared cause.

**Why:** a raw count conflates duplicates, harness faults and distinct causes, so it misstates both yield and remaining work.

## Replaying only the seed

**Wrong:** Keep a random seed and summary while discarding the actual failing input, build and raw outputs.

**Better:** Keep the original case and configuration; include controlled decisions for any schedule/fault search. OSS-Fuzz reproduction uses actual testcase bytes and compatible sanitizer/architecture, not only a seed; some bugs "are reproducible only in 32 bit mode or only in 64 bit mode" ([OSS-Fuzz reproduction, Fuzz target bugs and Build the image and the fuzzers](https://raw.githubusercontent.com/google/oss-fuzz/156f862e5976b3d23828230a0a5b4fef54074d32/docs/advanced-topics/reproducing.md)). A native input replay does not itself replay an external schedule.

**Why:** a seed regenerates the failure only under the same generator, build and configuration, which drift.

## Confusing observation limits with product guarantees

**Wrong:** Treat a successful history check as every possible isolation property, or a timeout as proof of a product hang.

**Better:** State the selected model, recorded information and limit that ended the case. Elle's paper states "Our approach ignores predicates and deals only in individual objects"; libFuzzer separately defines campaign and per-case resource controls, and a per-input limit means "the process is treated as a failure case" ([Elle §9](https://arxiv.org/abs/2003.10554), [libFuzzer 23.1.0 options](https://releases.llvm.org/23.1.0/docs/LibFuzzer.html#options)). Investigate the actual violated contract.

**Why:** a checker's model and a runner's limit bound what the observation can show; neither is the product's guarantee.

## Declaring a winner from a lucky pilot

**Wrong:** One run found more coverage, so it is a proven better bugfinding method.

**Better:** Use a small pilot for a provisional allocation decision. If asserting comparative performance, retain matched repeated trials and variability; coverage is still distinct from confirmed defect yield. FuzzBench reports "the number of trials, mean, median, standard" deviation per benchmark ([FuzzBench report, Per-benchmark summary](https://raw.githubusercontent.com/google/fuzzbench/3234e151d70f6093272a9b4155e68ee57faf986c/docs/reference/report.md)). Report zero findings honestly when that is the observation.

**Why:** fuzzing outcomes vary run to run, so one run cannot separate a better method from luck.
