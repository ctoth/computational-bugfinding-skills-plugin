# Common mistakes

## Treating a nemesis log as proof a fault happened

**Wrong:** "The history has `:kill` and `:pause` nemesis events, so processes died and paused."

**Right:** Observe actual activation (process state, connectivity, clock offset) separately from the request. Jepsen 0.3.15 records that `control.util/grepkill!` "has silently done nothing since 0.3.12", so kill and pause/resume faults built on it "did nothing" ([Jepsen CHANGELOG, 0.3.15 Bugfixes](https://raw.githubusercontent.com/jepsen-io/jepsen/6766ba09682bcb668d44c025e687dd8b1616e8a2/jepsen/CHANGELOG.md)).

**Why:** a no-op fault yields a healthy history that tested no failure.

## Translating a timeout into a definite aborted write

**Wrong:** Record a timed-out write as `:fail` and drop its value from the possible state.

**Right:** Keep it indeterminate. The timeout wrapper returns `(assoc op :type :info, :error ::timeout)`, and "An `:info` may do either." ([jepsen.client, Timeout](https://raw.githubusercontent.com/jepsen-io/jepsen/6766ba09682bcb668d44c025e687dd8b1616e8a2/jepsen/src/jepsen/client.clj), [jepsen.history README, Operation Semantics](https://raw.githubusercontent.com/jepsen-io/history/61d2776c889ad84f7c6922977cf05e8f11970402/README.md)).

**Why:** `:fail` "*must* have no logical effect on the system"; a later read of a timed-out write's value then contradicts the recorded failure.

## Resetting data on reconnect

**Wrong:** Create tables or clear keys in `open!`.

**Right:** Put initialization in `setup!`; "Open *should not* affect the logical state of the test" and "Close should not affect the logical state of the test." Unless a client is reusable, "crashed clients will be closed and new ones opened to replace them", so `open!` runs again mid-test ([jepsen.client, Client and Reusable protocols](https://raw.githubusercontent.com/jepsen-io/jepsen/6766ba09682bcb668d44c025e687dd8b1616e8a2/jepsen/src/jepsen/client.clj)).

**Why:** a reset mid-run erases the effects the checker is supposed to find.

## Reading a green or incomplete run as the intended guarantee

**Wrong:** Exit code 0, so the guarantee held.

**Right:** Inspect `:results` and each sub-result. `unbridled-optimism` always returns `{:valid? true}`; `check-safe` turns checker exceptions into `:unknown`; the set checker returns `:unknown` with "Set was never read"; `stats` marks a `:f` with no `:ok` operations invalid ("Results are valid only if every :f has at some :ok") ([jepsen.checker](https://raw.githubusercontent.com/jepsen-io/jepsen/6766ba09682bcb668d44c025e687dd8b1616e8a2/jepsen/src/jepsen/checker.clj)). The CLI exits 1 for `false` and 2 for `:unknown` and calls no exit otherwise ([jepsen.cli, single-test-cmd](https://raw.githubusercontent.com/jepsen-io/jepsen/6766ba09682bcb668d44c025e687dd8b1616e8a2/jepsen/src/jepsen/cli.clj)).

**Why:** a checker that never evaluated the property still lets the process exit 0.

## Ending after load or trusting a fixed recovery sleep

**Wrong:** Stop at the time limit, or treat a fixed sleep as proof the cluster converged.

**Right:** Heal, wait on evidence the target supports, then run final client operations. The etcd producer runs the nemesis final generator, `(gen/sleep 10)`, then the workload's final generator; the sleep is its choice for etcd, not a convergence proof ([jepsen.etcd, etcd-test](https://raw.githubusercontent.com/jepsen-io/etcd/b47cc401f27bfb7c28afd9ac088b5f0dca4501b8/src/jepsen/etcd.clj)).

**Why:** loss that appears only after recovery is never observed without final reads.

## Treating a seed or load flag as complete replay or resource control

**Wrong:** "Same `--seed`, same run" and "`--time-limit 60` means the test takes a minute."

**Right:** Record timing, responses and total cost. `--seed` "does not guarantee determinism in general", and `--time-limit` is "Excluding setup and teardown" ([jepsen.cli, test-opt-spec](https://raw.githubusercontent.com/jepsen-io/jepsen/6766ba09682bcb668d44c025e687dd8b1616e8a2/jepsen/src/jepsen/cli.clj)).

**Why:** behavior depends on "the timing and responses to each request", and setup, healing and analysis cost extra.

## Copying the etcd stale-read example into a linearizability check

**Wrong:** Run the README line `lein run test --time-limit 30 -s --nemesis partition --workload register --concurrency 2n` and report stale reads as a linearizability bug.

**Right:** Drop `-s` unless stale reads are the subject; `-s` is `--serializable`, "Use serializable reads, instead of going through consensus." ([jepsen.etcd, cli-opts](https://raw.githubusercontent.com/jepsen-io/etcd/b47cc401f27bfb7c28afd9ac088b5f0dca4501b8/src/jepsen/etcd.clj), [jepsen.etcd README, Quickstart and Options](https://raw.githubusercontent.com/jepsen-io/etcd/b47cc401f27bfb7c28afd9ac088b5f0dca4501b8/README.md)).

**Why:** `--serializable` "allows etcd to serve stale data", so the promise under test changed.

## Calling a process kill equivalent to power loss

**Wrong:** "We killed etcd, so un-fsynced data loss was covered."

**Right:** Read the selected storage model; etcd's `--lazyfs` "alters the `kill` nemesis to also lose un-fsynced writes", which a plain kill does not ([jepsen.etcd README, Options](https://raw.githubusercontent.com/jepsen-io/etcd/b47cc401f27bfb7c28afd9ac088b5f0dca4501b8/README.md)).

**Why:** the two faults lose different data; only the lazyfs route drops un-fsynced writes.

## Losing live-state evidence while collecting logs

**Wrong:** Plan to inspect the database after the run finishes.

**Right:** Record needed observations as operations before teardown, or set `:leave-db-running?`. Log collection kills the database "if possible, before downloading logs", and the checker runs after database teardown ([jepsen.core, snarf-logs! and run!](https://raw.githubusercontent.com/jepsen-io/jepsen/6766ba09682bcb668d44c025e687dd8b1616e8a2/jepsen/src/jepsen/core.clj)).

**Why:** the checker sees only the history; state not recorded is gone.

## Adding a `down` toxic from the Node client

**Wrong:** `proxy.addToxic({ type: "down" })`, because toxiproxy-node-client's `Type` union lists `"down"`.

**Right:** Disable the proxy with `proxy.update({ enabled: false })`. Toxiproxy says `down` "is not technically a toxic" and is done by setting `enabled` to `false` ([Toxiproxy README](https://raw.githubusercontent.com/Shopify/toxiproxy/49299d8838525126e09c85ebe0ba89940a3261e5/README.md), [Toxic.ts](https://raw.githubusercontent.com/ihsw/toxiproxy-node-client/d7782a4ee344ad30f7030f7dc63a8567f052c5e2/src/Toxic.ts)).

**Why:** the server returns `ErrInvalidToxicType` for a type not in its registry ([toxic_collection.go](https://raw.githubusercontent.com/Shopify/toxiproxy/49299d8838525126e09c85ebe0ba89940a3261e5/toxic_collection.go)), so no outage happens.

## Expecting a partial-toxicity run to replay

**Wrong:** Set `toxicity: 0.3` and expect a rerun to fault the same connections.

**Right:** Record which connections were affected, or use toxicity 1 on chosen links.

**Why:** each link draws `rand.Float32()` and compares it to the toxicity, and the toxic exposes no seed ([toxic.go `ToxicStub.Run`](https://raw.githubusercontent.com/Shopify/toxiproxy/49299d8838525126e09c85ebe0ba89940a3261e5/toxics/toxic.go)).

## Counting an MSW network error as a deployment fault

**Wrong:** "MSW returned `HttpResponse.error()` for the write, so we tested a network failure of the service."

**Right:** Fault a real deployment through Toxiproxy or process control; keep MSW for client error-handling tests. `setupServer` "_does not_ establish any servers, operating entirely in the thread of your process" ([MSW setupServer](https://raw.githubusercontent.com/mswjs/mswjs.io/bda552ebaadde6d75870b4d07de734f9de35fd89/src/content/api/setup-server/index.md)).

**Why:** the request never reaches a server, so the ambiguous case of an applied write with a lost response cannot arise unless the handler models it.

## Stopping a test container to simulate a crash, then reading its data

**Wrong:** `await container.stop()` and then inspect the recovered database.

**Right:** Use `restart()` or `stop({ remove: false })`. `stop` defaults to `remove: this.autoRemove` and `removeVolumes: true` ([started-generic-container.ts](https://raw.githubusercontent.com/testcontainers/testcontainers-node/17316dbd001bf7468023087e3620a134466f32c5/packages/testcontainers/src/generic-container/started-generic-container.ts)).

**Why:** with auto-remove on, the container and its volumes are gone, so there is no recovered state to check.

## Upgrading a point-history verdict into every isolation guarantee

**Wrong:** "Elle found no anomaly, so the system is serializable."

**Right:** State the observed objects and model scope. "Our approach ignores predicates and deals only in individual objects", and "In practice, we typically fail to observe the results of some transactions" ([Elle, §§4.3 and 9](https://arxiv.org/abs/2003.10554v1)).

**Why:** predicate anomalies and unobserved outcomes lie outside what the checker can see.
