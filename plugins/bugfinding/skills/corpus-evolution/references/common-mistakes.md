# Common mistakes

| Misleading action or conclusion | Correction and evidence |
|---|---|
| Prune the only regression/original set with coverage minimization | Select a working subset while preserving chosen failure evidence; coverage merge and crash reduction have distinct predicates ([libFuzzer](https://llvm.org/docs/LibFuzzer.html)). |
| Rename a `[]byte` choice file for a `string` receiver | Call the actual producer/serializer and replay it; Go types/order are part of the encoding ([Go corpus format](https://go.dev/doc/security/fuzz/)). |
| Treat copied seed count as receiver reach | Verify decoded input and intended property execution; AFL++ itself distinguishes corpus count from coverage ([depth guide, §3g](https://aflplus.plus/docs/fuzzing_in_depth/)). |
| Assume the smallest coverage set always improves discovery | Account preprocessing and scheduler-dependent results; use a matched pilot ([Rebert et al., §§6.2–6.3](https://www.usenix.org/system/files/conference/usenixsecurity14/sec14-paper-rebert.pdf)). |
| Treat a component's remembered license as the whole tool's | Check the selected revision's project and file-level scope ([AFL++ licensing](https://raw.githubusercontent.com/AFLplusplus/AFLplusplus/d0070729206a80a9af297b2341edd63f68fdac35/LICENSING.md)). |

For this pack's workflow, explain why a case leaves the active set without erasing its original failure or resource evidence. Use `evidence-based-triage` for cause grouping and `failure-reduction` for witness-preserving simplification.
