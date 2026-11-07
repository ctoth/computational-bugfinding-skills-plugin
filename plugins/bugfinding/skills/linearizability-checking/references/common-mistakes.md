# Common mistakes

| Misleading shortcut | Correction |
|---|---|
| Relabel an isolation or race-detector result as linearizability | Establish the object's actual sequential contract and real-time ordering ([Jepsen](https://jepsen.io/consistency/models/linearizable)). |
| Sort calls into completion-order pairs | Retain observed overlap and matched event identity; the checker searches admissible orders, not an invented serialization ([conversion source](https://raw.githubusercontent.com/anishathalye/porcupine/master/checker.go)). |
| Feed pending calls as raw unmatched events, or assume timeout means no effect | Validate pairing and derive a justified uncertainty model; the existing etcd adapter's unknown completion is specific to its model ([adapter](https://raw.githubusercontent.com/anishathalye/porcupine/master/porcupine_test.go)). |
| Mutate prior model state while stepping | Keep model transitions pure so backtracking revisits the intended state ([model](https://raw.githubusercontent.com/anishathalye/porcupine/master/model.go)). |
| Split every history by key despite global size/transfer calls | Establish the partition's semantic equivalence or keep the coupled model ([paper, pp.5-6](https://arxiv.org/abs/1504.00204)). |
| Count `Unknown` as a completed accepted history | Preserve exhausted checking distinctly and report the actual budget/result ([API](https://raw.githubusercontent.com/anishathalye/porcupine/master/porcupine.go)). |
| Treat a nominal checker deadline as a hard interrupt for any callback | Use a supported cancellation-aware model and fitting outer limit; verbose checking waits for workers ([checker](https://raw.githubusercontent.com/anishathalye/porcupine/master/checker.go)). |
| Infer a minimal cause from the HTML display | Retain raw histories/model; visualized partial orders are search evidence ([visualization](https://raw.githubusercontent.com/anishathalye/porcupine/master/visualization.go)). |
