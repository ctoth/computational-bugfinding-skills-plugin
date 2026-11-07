# Elle operation

## Match the actual artifact

Use an existing compatible integration. Inspect the selected jar's version, dependency manifest and help before selecting options; current CLI and library main are separate artifacts ([CLI manifest](https://raw.githubusercontent.com/ligurio/elle-cli/master/project.clj), [library manifest](https://raw.githubusercontent.com/jepsen-io/elle/main/project.clj)). The inspected manifests declare EPL-2.0 OR GPL-2.0-or-later WITH Classpath-exception-2.0; preserve selected component/release identity rather than infer licensing from another package.

The CLI README observed on 2026-11-07 requires Java 21+ and documents Leiningen `lein deps`/`lein uberjar` builds; optional graph rendering needs its fitting environment. These are dependency/build changes only when authorized, not prerequisites this skill installs ([CLI setup](https://raw.githubusercontent.com/ligurio/elle-cli/master/README.md)). A non-JVM target can retain its recorder and use the existing file interface.

Do not treat a warning comment as a release verdict. Jepsen's 0.3.15 changelog says Elle 0.2.8 fixes incorrect register cyclic-version inference caused by Bifurcan defects. The register docstring still warns about strengthening options; inspect the selected release/source and validate edge provenance before relying on those assumptions ([release account](https://raw.githubusercontent.com/jepsen-io/jepsen/main/jepsen/CHANGELOG.md), [register options](https://raw.githubusercontent.com/jepsen-io/elle/main/src/elle/rw_register.clj)). Do not suppress a witness or invent a current defect from either text.

## Conditional command

For a selected compatible existing build and a contract promising serializability:

```text
java -jar ELLE_CLI_JAR --model list-append --consistency-models serializable --cycle-search-timeout 1000 --directory EVIDENCE HISTORY.edn
```

Substitute actual paths/model and choose resource values from the authorized budget. The example's 1000ms limits search for one strongly connected component, not total analysis or plot time. The inspected CLI accepts EDN/JSON histories, dispatches frontend/model options and has separate rendering controls ([CLI source](https://raw.githubusercontent.com/ligurio/elle-cli/master/src/elle_cli/cli.clj)). This command is source-verified, not an executed compatibility claim.

## Interpret actual analysis

Require the requested file's explicit true/false/unknown result; exit zero also covers unknown-only output or help without analysis. JSON analysis can preserve the witness; retain file association yourself when checking multiple inputs ([CLI result path](https://raw.githubusercontent.com/ligurio/elle-cli/master/src/elle_cli/cli.clj)).

Preserve prohibited anomalies, inconclusive searches and already-found evidence independently. Current result construction can retain a known prohibited anomaly despite other incomplete work; absence of a graph/plot is not a healthy-history proof ([analysis source](https://raw.githubusercontent.com/jepsen-io/elle/main/src/elle/txn.clj)). Record conversion, graph/search/render cost and an outer resource envelope separately.

For direct Clojure integration, select the matching `elle.list-append/check` or `elle.rw-register/check` API and pass only options supported by that selected version. Retain source/binary/configuration, original/converted history and all inference assumptions ([append API](https://raw.githubusercontent.com/jepsen-io/elle/main/src/elle/list_append.clj), [register API](https://raw.githubusercontent.com/jepsen-io/elle/main/src/elle/rw_register.clj)). Detailed fault generation belongs to `distributed-fault-testing`; schedule control belongs to `schedule-exploration`.
