# Common mistakes

| Misleading shortcut | Correction |
|---|---|
| Treat a timeout as a definite abort | Preserve uncertain effect unless the actual contract proves no effect ([history](https://raw.githubusercontent.com/jepsen-io/history/main/README.md)). |
| Split one transaction into independently committed writes | Retain original micro-operation boundaries and order ([append API](https://raw.githubusercontent.com/jepsen-io/elle/main/src/elle/list_append.clj)). |
| Infer all isolation guarantees from a serializable result | Select session/realtime guarantees explicitly; ordinary serializability omits them ([model](https://jepsen.io/consistency/models/serializable)). |
| Accept exit zero as a checked healthy history | Require explicit requested-file verdict and admitted input ([CLI source](https://raw.githubusercontent.com/ligurio/elle-cli/master/src/elle_cli/cli.clj)). |
| Strengthen register inference with an assumed order | Establish the actual exposed ordering and selected-version assumptions ([register source](https://raw.githubusercontent.com/jepsen-io/elle/main/src/elle/rw_register.clj)). |
| Treat more overwritten values as more information | Choose observations that recover relevant write/version provenance ([Elle, §3](https://arxiv.org/abs/2003.10554)). |
| Drop timeout evidence or call every partial search invalid | Retain discovered prohibited anomalies and unresolved analysis separately ([result construction](https://raw.githubusercontent.com/jepsen-io/elle/main/src/elle/txn.clj)). |
| Shrink to a different inferred cycle by erasing setup/uncertainty | Preserve the original and revalidate the selected witness's premises ([Elle, §§4.3 and 6](https://arxiv.org/abs/2003.10554)). |

Use `failure-reduction` for minimizing the dependent evidence and `evidence-based-triage` for supported attribution; this skill owns transaction observations and isolation interpretation.
