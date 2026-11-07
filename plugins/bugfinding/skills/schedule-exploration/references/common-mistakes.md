# Common mistakes

| Shortcut | Correction and evidence |
|---|---|
| Repeated stress runs or fake time described as schedule enumeration | Identify actual controlled choices; synctest documents time/isolation rather than enumeration ([Go](https://pkg.go.dev/testing/synctest)). |
| Top-level controller hides unchanged dependency synchronization | Trace the real controlled path and record omitted internals ([Loom](https://docs.rs/loom/0.7.2/loom/)). |
| A Loom alarm proves a hardware-valid SeqCst failure | Adjudicate documented weakened-access modeling; preserve missed-execution limits too ([README](https://raw.githubusercontent.com/tokio-rs/loom/master/README.md)). |
| A checkpoint filename suffices on the default Loom dependency | Enable the selected checkpoint feature and preserve compatible configuration ([source](https://raw.githubusercontent.com/tokio-rs/loom/master/src/model.rs)). |
| `max_time` guarantees interrupting a stuck Shuttle iteration | Use its actual between-iteration contract and separate owned outer limits ([Config](https://docs.rs/shuttle/0.9.10/shuttle/struct.Config.html)). |
| A Coyote TestingEngine wrapper controls unchanged binaries | Rewrite the selected binaries first; consume lazy traces ([integration](https://microsoft.github.io/coyote/how-to/unit-testing/)). |
| Coyote systematic schedules validate wall-time/weak-memory behavior | State its finite-wait and SC model boundaries ([rewriting semantics](https://microsoft.github.io/coyote/concepts/binary-rewriting/)). |
| Retain only a seed or shrink only source | Keep initial state/workload/choices; replay and choice exposure are distinct ([CHESS, §§3–4](https://www.microsoft.com/en-us/research/wp-content/uploads/2016/02/osdi2008-CHESS.pdf)). |
