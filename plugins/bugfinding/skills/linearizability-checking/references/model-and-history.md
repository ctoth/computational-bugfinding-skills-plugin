# Model and history

## Choose the observable object

Derive abstract state and legal responses from the actual API, including error effects and initialization. A contract can cover one key, a whole map, or coupled operations; that scope determines real-time obligations. Do not infer a multi-object guarantee from an individual-key promise ([Jepsen](https://jepsen.io/consistency/models/linearizable)).

Keep returned handles/values distinct from implementation internals. Porcupine requires a nonmutating transition, fitting state equality and equal hashes for equal states when hashing is supplied. Its default equality uses Go `==`; select explicit equality for unsuitable state types. Nondeterministic successor sets describe permitted behavior, not permission to discard inconvenient observations ([model source](https://raw.githubusercontent.com/anishathalye/porcupine/master/model.go)).

## Preserve recorder evidence

Bracket the actual operation. Keep matching calls/responses, immutable serialized inputs/outputs and genuine order; do not invent real-time edges from unsynchronized client clocks. The upstream README warns that timestamp instrumentation itself can be unsound on weakly ordered machines ([recorder notes](https://github.com/anishathalye/porcupine)). A checker cannot recover ordering lost before import.

For Porcupine, choose either completed `Operation` intervals or an ordered matched `Event` sequence. Equal numeric endpoints allow overlap. Validate duplicate IDs, missing responses and within-operation order before checking; the implementation pairs events rather than repairing them ([model](https://raw.githubusercontent.com/anishathalye/porcupine/master/model.go), [entry conversion](https://raw.githubusercontent.com/anishathalye/porcupine/master/checker.go)). Preserve rejected recorder data separately.

## Keep uncertainty semantic

A timeout does not establish that a write had no effect. Derive possible applied/unapplied outcomes and admissible completion boundaries from the real operation. Porcupine's etcd example appends modeled unknown responses for pending calls; inspect its actual model with its adapter before adapting that technique. The parser is an example producer, not a universal incomplete-history contract ([test adapter](https://raw.githubusercontent.com/anishathalye/porcupine/master/porcupine_test.go)).

When investigating rejection, preserve all relevant contract-permitted interpretations. Use supported nondeterministic modeling or explicit justified completions where they express that uncertainty; otherwise leave the case undecided. Never delete an uncertain mutation just to obtain a verdict. The paper's algorithm assumes completed histories under its stated assumptions ([paper, pp.3-5](https://arxiv.org/abs/1504.00204)).

## Worked distinction

Illustrative contract: a register starts at zero and promises linearizable reads/writes. An acknowledged write of one followed by a later-starting read of zero contradicts the sequential contract. An overlapping read may legally observe zero. If the write's response was lost, record its possible effect and completion; treating it as a known failed write changes the premise. Construct both legal and illegal controls from the actual API before applying this example ([real-time definition](https://jepsen.io/consistency/models/linearizable), [adapter example](https://raw.githubusercontent.com/anishathalye/porcupine/master/porcupine_test.go)). This example is not an executed product finding.
