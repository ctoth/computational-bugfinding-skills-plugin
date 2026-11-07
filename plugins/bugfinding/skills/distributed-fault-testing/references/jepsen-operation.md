# Jepsen operation

These are conditional instructions for an existing target-specific Jepsen integration. Commands are illustrative, not executed examples or universal defaults. Read the selected adapter/build and its help before execution; a Jepsen library dependency does not supply an arbitrary application's client, workload or checker ([architecture](https://raw.githubusercontent.com/jepsen-io/jepsen/6766ba09682bcb668d44c025e687dd8b1616e8a2/README.md)).

## Select one actual source/build set

Verify Java/Leiningen and the selected target's node requirements. The inspected 2026-11-07 README specifies JVM 21+, JNA, Gnuplot and Graphviz; many adapters assume Debian/Linux, SSH and privileged node control. Ordinary containers do not provide independent clocks for skew tests ([setup](https://raw.githubusercontent.com/jepsen-io/jepsen/6766ba09682bcb668d44c025e687dd8b1616e8a2/README.md)).

Use the project's actual dependency manifest and artifact identity. Current source and published API documentation may differ; main's `project.clj` is a snapshot, not a release pin. Core project metadata declares EPL with an EPL-1.0 URL; the full core license text was not verified in this research. The separate generator and etcd READMEs declare EPL-2.0 with stated secondary-license conditions. Check the selected components instead of substituting one declaration for all ([core metadata](https://raw.githubusercontent.com/jepsen-io/jepsen/6766ba09682bcb668d44c025e687dd8b1616e8a2/jepsen/project.clj), [generator license](https://raw.githubusercontent.com/jepsen-io/generator/3073ba45cb3db0b6dcc5aa915907a2e67b04eef5/README.md), [adapter license](https://raw.githubusercontent.com/jepsen-io/etcd/b47cc401f27bfb7c28afd9ac088b5f0dca4501b8/README.md)).

## Keep the client faithful

`open!` and `close!` must not reset logical test state; initialization belongs in `setup!`. Preserve the operation's function/process and translate actual results; validation of record shape does not establish semantic correctness ([client source](https://raw.githubusercontent.com/jepsen-io/jepsen/6766ba09682bcb668d44c025e687dd8b1616e8a2/jepsen/src/jepsen/client.clj)).

A Jepsen `:fail` completion promises no logical effect. A response timeout may be `:info`; retries can create additional physical attempts without determining their outcomes. Preserve actual request/attempt provenance, and use the history specialist for faithful conversion ([history contract](https://raw.githubusercontent.com/jepsen-io/history/61d2776c889ad84f7c6922977cf05e8f11970402/README.md)).

## Run a fitting bounded test

For an existing compatible etcd test with an owned-node file and verified register/partition options:

```text
lein run test --help
lein run test --nodes-file OWNED_NODES --workload register --nemesis partition --concurrency 2n --time-limit 60 --test-count 1 --seed 12345
```

Replace resource values and workload/fault selection from the experiment. These option shapes come from the actual CLI and target producer; `--serializable` changes the read contract and must not be silently enabled while checking linearizable reads ([CLI](https://raw.githubusercontent.com/jepsen-io/jepsen/6766ba09682bcb668d44c025e687dd8b1616e8a2/jepsen/src/jepsen/cli.clj), [etcd options](https://raw.githubusercontent.com/jepsen-io/etcd/b47cc401f27bfb7c28afd9ac088b5f0dca4501b8/README.md)).

Reserve an outer budget for the entire run. `--time-limit` excludes setup/teardown; `gen/time-limit` controls emission, not arbitrary in-flight calls. `gen/phases` waits for workers, and `until-ok` can continue until a success arrives. A seed preserves some choices, not real timing/responses ([CLI](https://raw.githubusercontent.com/jepsen-io/jepsen/6766ba09682bcb668d44c025e687dd8b1616e8a2/jepsen/src/jepsen/cli.clj), [generator implementation](https://raw.githubusercontent.com/jepsen-io/generator/3073ba45cb3db0b6dcc5aa915907a2e67b04eef5/src/jepsen/generator.clj)).

## Interpret and retain

The inspected single-test CLI maps `false` to exit 1 and `:unknown` to exit 2; argument/internal errors have separate paths. Require actual intended-history checks and inspect `:results`, sub-results, errors and witnesses rather than treating exit 0 as sufficient. Checker exceptions can become unknown ([CLI](https://raw.githubusercontent.com/jepsen-io/jepsen/6766ba09682bcb668d44c025e687dd8b1616e8a2/jepsen/src/jepsen/cli.clj), [checker](https://raw.githubusercontent.com/jepsen-io/jepsen/6766ba09682bcb668d44c025e687dd8b1616e8a2/jepsen/src/jepsen/checker.clj)).

For failed setup, inspect actual adapter/runtime/SSH evidence; a missing client or mismatched dependency is not a target consistency finding. For unknown, retain the checker error/incomplete observations. For false, inspect the violated contract and witness. For apparent success with no activated fault or successful property evaluations, report the narrower tested space. Reanalysis through `analyze` rebuilds the checker from stored arguments/source; it does not replay the original cluster execution ([analysis command](https://raw.githubusercontent.com/jepsen-io/jepsen/6766ba09682bcb668d44c025e687dd8b1616e8a2/jepsen/src/jepsen/cli.clj)).
