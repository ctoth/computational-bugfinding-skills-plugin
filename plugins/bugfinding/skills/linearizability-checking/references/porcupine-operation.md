# Porcupine operation

## Select the existing integration

Use the target's Go test/model/recorder if it fits. Inspect the selected Porcupine version's API; the source snapshot read for this skill on 2026-11-07 declares module `github.com/anishathalye/porcupine` and Go 1.16, with an MIT license. A module declaration alone is not a complete future compatibility matrix ([go.mod](https://raw.githubusercontent.com/anishathalye/porcupine/master/go.mod), [license](https://raw.githubusercontent.com/anishathalye/porcupine/master/LICENSE.md)).

Only where dependency changes are in scope, select a compatible module version using `go get github.com/anishathalye/porcupine@SELECTED_VERSION`; this changes dependency files/downloads. Reuse project tooling and keep the actual selected version with evidence ([Go dependency management](https://go.dev/doc/modules/managing-dependencies)). No special CLI or container is required by this integration.

## Call the bounded API

The following fragment assumes the real model, validated complete operation history and chosen finite checker budget already exist. It is an integration sketch, not an executed or standalone test ([Porcupine API](https://raw.githubusercontent.com/anishathalye/porcupine/master/porcupine.go)):

```go
result, info := porcupine.CheckOperationsVerbose(model, operations, checkerBudget)
switch result {
case porcupine.Ok:
    // Retain completed acceptance for this model/history.
case porcupine.Illegal:
    // Preserve the rejected history and inspect the contradiction.
case porcupine.Unknown:
    // Preserve exhausted checking as inconclusive.
}
```

For matched ordered events use `CheckEventsVerbose`; timeout zero is unlimited. Non-verbose bounded APIs return the explicit result without visualization data. Avoid replacing that result with a boolean that hides exhaustion ([API](https://raw.githubusercontent.com/anishathalye/porcupine/master/porcupine.go)). Verify newer cancellation APIs in the selected release; see [partitioning and cost](partition-and-cost.md).

Conditional focused runner for an existing authorized test:

```text
go test ./path/to/pkg -run '^TestLinearizability$' -count=1 -timeout=60s
```

Choose actual names and limits from the task. The illustrative test-binary timeout is separate from `checkerBudget`; `-count=1` disables successful-result caching. Follow the project's permitted runner rather than treating this example as authorization ([Go testing flags](https://pkg.go.dev/cmd/go#hdr-Testing_flags)). This command was not executed for the skill.

## Keep inspectable evidence

Save raw and converted histories, initialization, model/adapter source, version/build/configuration, exact invocation/limits and actual result. With verbose `info`, `VisualizePath(model, info, outputPath)` writes embedded HTML; keep the raw evidence too. Visualization replays model steps, and partial linearizations are not a minimal unsatisfiable core or demonstrated root cause ([visualization source](https://raw.githubusercontent.com/anishathalye/porcupine/master/visualization.go), [usage](https://github.com/anishathalye/porcupine)).

If checking or rendering stalls, inspect callback cost/cancellation and actual progress before changing the model or history. Do not suppress coupled operations or real overlap to manufacture a faster verdict ([checker](https://raw.githubusercontent.com/anishathalye/porcupine/master/checker.go), [paper, pp.5-9](https://arxiv.org/abs/1504.00204)). Preserve bounded partial results and original artifacts for reduction/triage.
