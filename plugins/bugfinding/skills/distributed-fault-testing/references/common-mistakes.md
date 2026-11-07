# Common mistakes

| Mistake | Correction |
|---|---|
| Treat a nemesis log as proof a process died | Observe actual activation; Jepsen 0.3.15 documents fixed no-op faults in earlier releases ([incident](https://raw.githubusercontent.com/jepsen-io/jepsen/6766ba09682bcb668d44c025e687dd8b1616e8a2/jepsen/CHANGELOG.md)). |
| Translate a timeout into a definite aborted write | Preserve possible effects; the timeout wrapper uses `:info` ([client](https://raw.githubusercontent.com/jepsen-io/jepsen/6766ba09682bcb668d44c025e687dd8b1616e8a2/jepsen/src/jepsen/client.clj)). |
| Reset data on reconnect | Keep logical setup out of `open!`/`close!` ([lifecycle](https://raw.githubusercontent.com/jepsen-io/jepsen/6766ba09682bcb668d44c025e687dd8b1616e8a2/jepsen/src/jepsen/client.clj)). |
| Interpret a green empty or incomplete run as the intended guarantee | Verify useful operations and actual subchecker results; exceptions may yield unknown ([checker](https://raw.githubusercontent.com/jepsen-io/jepsen/6766ba09682bcb668d44c025e687dd8b1616e8a2/jepsen/src/jepsen/checker.clj)). |
| End after load or trust a fixed recovery sleep | Observe repair and run final workload checks before teardown ([real producer](https://raw.githubusercontent.com/jepsen-io/etcd/b47cc401f27bfb7c28afd9ac088b5f0dca4501b8/src/jepsen/etcd.clj)). |
| Use one seed or load flag as complete replay/resource control | Record timing/responses and total run cost; CLI explicitly limits those promises ([CLI](https://raw.githubusercontent.com/jepsen-io/jepsen/6766ba09682bcb668d44c025e687dd8b1616e8a2/jepsen/src/jepsen/cli.clj)). |
| Call kill equivalent to power loss | Read the selected storage model; etcd's lazyfs route adds loss of un-fsynced writes ([options](https://raw.githubusercontent.com/jepsen-io/etcd/b47cc401f27bfb7c28afd9ac088b5f0dca4501b8/README.md)). |
| Lose live-state evidence while collecting logs | Capture required observations first; core log gathering may kill the database ([core](https://raw.githubusercontent.com/jepsen-io/jepsen/6766ba09682bcb668d44c025e687dd8b1616e8a2/jepsen/src/jepsen/core.clj)). |
| Upgrade a point-history verdict into every isolation guarantee | Keep the selected observable/model scope explicit ([Elle, §§4.3 and 9](https://arxiv.org/abs/2003.10554)). |
