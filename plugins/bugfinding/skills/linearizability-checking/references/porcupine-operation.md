# Porcupine operation

## Select the existing integration

Use the target's Go test/model/recorder if it fits. Inspect the selected Porcupine version's API; the source read for this skill on 2026-11-07 is tag v1.3.1 (commit `97cd067defd99df172053ba7f4ca5bbae57fe446`), which declares `module github.com/anishathalye/porcupine` and `go 1.16`, under "The MIT License (MIT)", and whose `Model` has the optional `StepContext` field. A module declaration alone is not a complete future compatibility matrix ([go.mod](https://raw.githubusercontent.com/anishathalye/porcupine/97cd067defd99df172053ba7f4ca5bbae57fe446/go.mod), [license](https://raw.githubusercontent.com/anishathalye/porcupine/97cd067defd99df172053ba7f4ca5bbae57fe446/LICENSE.md), [model](https://raw.githubusercontent.com/anishathalye/porcupine/97cd067defd99df172053ba7f4ca5bbae57fe446/model.go)).

Only where dependency changes are in scope, select a compatible module version using `go get github.com/anishathalye/porcupine@SELECTED_VERSION`; this changes dependency files/downloads: `go get` "updates the `require` directive in your go.mod file" and "downloads module source code" when needed. Reuse project tooling and keep the actual selected version with evidence ([Go dependency management](https://go.dev/doc/modules/managing-dependencies)). No special CLI or container is required by this integration.

Porcupine reads no history files: `Input`, `Output` and `Value` are `interface{}`, and `model.go` declares no JSON struct tags. A history recorded outside Go, for example by a Node.js client (see [model and history](model-and-history.md)), needs a small Go decoder into the model's typed values that builds `Operation{ClientId, Input, Call, Output, Return}` or `Event{ClientId, Kind, Value, Id}`; `ClientId` is commented "optional, unless you want a visualization; zero-indexed" ([model.go](https://raw.githubusercontent.com/anishathalye/porcupine/97cd067defd99df172053ba7f4ca5bbae57fe446/model.go)).

## Call the bounded API

The following fragment assumes the real model, validated complete operation history and chosen finite checker budget already exist. It is an integration sketch, not an executed or standalone test ([Porcupine API](https://raw.githubusercontent.com/anishathalye/porcupine/97cd067defd99df172053ba7f4ca5bbae57fe446/porcupine.go)):

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

For matched ordered events use `CheckEventsVerbose`; "A timeout of 0 is interpreted as an unlimited timeout." Non-verbose bounded APIs (`CheckOperationsTimeout`, `CheckEventsTimeout`) return the explicit result without visualization data. The unbounded `CheckOperations`/`CheckEvents` return `res == Ok` as a boolean; avoid replacing a bounded result with a boolean that hides exhaustion ([API](https://raw.githubusercontent.com/anishathalye/porcupine/97cd067defd99df172053ba7f4ca5bbae57fe446/porcupine.go)). If the selected release differs from v1.3.1, confirm it has `StepContext` before relying on cancellation; see [partitioning and cost](partition-and-cost.md).

Conditional focused runner for an existing authorized test:

```text
go test ./path/to/pkg -run '^TestLinearizability$' -count=1 -timeout=60s
```

Choose actual names and limits from the task. The illustrative test-binary timeout is separate from `checkerBudget`: `-timeout d` means "If a test binary runs longer than duration d, panic." ([Go testing flags, go1.27.3](https://pkg.go.dev/cmd/go@go1.27.3#hdr-Testing_flags)). "The idiomatic way to disable test caching explicitly is to use -count=1." ([Go test packages, go1.27.3](https://pkg.go.dev/cmd/go@go1.27.3#hdr-Test_packages)). Follow the project's permitted runner rather than treating this example as authorization. This command was not executed for the skill.

## Keep inspectable evidence

Save raw and converted histories, initialization, model/adapter source, version/build/configuration, exact invocation/limits and actual result. With verbose `info`, `VisualizePath(model, info, outputPath)` writes "an HTML file with embedded JavaScript and data"; keep the raw evidence too. Visualization replays model steps through `model.Step` and panics with "valid partial linearization returned non-ok result from model step" if the model rejects a step it accepted during checking, so an impure model can break rendering. Partial linearizations are not a minimal unsatisfiable core or demonstrated root cause; for a rejected history the page shows "the longest partial linearization" per partition ([visualization source](https://raw.githubusercontent.com/anishathalye/porcupine/97cd067defd99df172053ba7f4ca5bbae57fe446/visualization.go), [usage](https://raw.githubusercontent.com/anishathalye/porcupine/97cd067defd99df172053ba7f4ca5bbae57fe446/README.md)).

If checking or rendering stalls, inspect callback cost/cancellation and actual progress before changing the model or history. Do not suppress coupled operations or real overlap to manufacture a faster verdict ([checker](https://raw.githubusercontent.com/anishathalye/porcupine/97cd067defd99df172053ba7f4ca5bbae57fe446/checker.go), [paper, pp.5-6](https://arxiv.org/abs/1504.00204)). Preserve bounded partial results and original artifacts for reduction/triage.
