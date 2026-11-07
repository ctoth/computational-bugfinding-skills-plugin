# Model and sequence design

## Establish a useful initial state

Use a small contract model plus a mapping from stable logical identities to actual returned handles. Separate generation/model transitions from real execution; RapidCheck's command interface separates model `apply`, SUT `run` and precondition checking ([Command interface](https://raw.githubusercontent.com/emil-e/rapidcheck/2c3c4365aca21ef4e612768fdc95b1ce8b39a651/include/rapidcheck/state/Command.h)). Do not perform a target mutation in a precondition just to discover whether the operation is allowed: `checkPreconditions(const Model &s0)` receives only the model, which lets RapidCheck generate valid sequences "without even running the actual System Under Test" ([Command interface](https://raw.githubusercontent.com/emil-e/rapidcheck/2c3c4365aca21ef4e612768fdc95b1ce8b39a651/include/rapidcheck/state/Command.h), [stateful guide, rc::state](https://raw.githubusercontent.com/emil-e/rapidcheck/2c3c4365aca21ef4e612768fdc95b1ce8b39a651/doc/state.md)).

Construct initial state through real operations when hidden lifecycle matters. Hughes's historical storage failure required opening, closing and reopening a file, because "the first call to open *creates* the file, while the second call opens an *existing* file"; removing the first open and close preserved an apparently equivalent visible state but erased the failure. That open/close/open sequence was the sequential prefix of a parallel test whose failure also needed three concurrent operations. Its independent corruption check observed something the result model missed ([Hughes, PDF pp. 14-16](https://publications.lib.chalmers.se/records/fulltext/232550/local_232550.pdf)). This motivates inspecting actual setup paths, not adding reopen calls universally.

## Worked experiment: permissioned object lifecycle

This is an illustrative design, not a claim about a particular engine. First obtain the target's actual ownership, permission, denial and deletion guarantees. Adapt the rows only where those contracts exist. Model-based commands can use a simpler specification rather than duplicate the implementation; fast-check warns against "comparing it to itself" ([fast-check model design, Overview](https://raw.githubusercontent.com/dubzzz/fast-check/5ec2e3aceae60eb510b8b967bcb153274f3abad7/website/docs/advanced/model-based-testing.md)).

| Operation | State needed for a useful call | Contract observation to implement |
|---|---|---|
| Create | An admitted principal/session | Retain returned handle and logical owner; verify promised initial state |
| Permitted mutation | Live handle and authority | Compare promised returned value and visible state change |
| Permission transition | Authorized owner and valid policy | Update abstract permission facts from the documented semantics |
| Deliberately denied mutation | Live object, actor lacking required authority | Verify documented denial and allowed/forbidden side effects |
| Observe / delete / later use | Correct live or deliberately stale identity | Check documented content/lifetime semantics; keep deliberate invalid use distinct |

Prefer useful interaction sequences over independently sampled nonexistent IDs. Log resolved object names when choosing by a model index: fast-check's command documentation makes this distinction to keep a failing trace understandable, so a command may need to "capture the state within the scope of the command when it executes" ([command serialization, Print the commands](https://raw.githubusercontent.com/dubzzz/fast-check/5ec2e3aceae60eb510b8b967bcb153274f3abad7/website/docs/advanced/model-based-testing.md)).

Track which operations actually executed and which reached their assertions. A false fast-check `check` bypasses `run`; many generated commands therefore need not mean many exercised effects ([runner source, internalModelRun](https://raw.githubusercontent.com/dubzzz/fast-check/5ec2e3aceae60eb510b8b967bcb153274f3abad7/packages/fast-check/src/check/model/ModelRunner.ts)). Keep exact counts, not a universal success-rate target.

## Preserve dependencies through reduction

After deleting a prefix, recompute identity/lifetime/permission facts and operation admissibility. Do not rely on captured generation-time state: RapidCheck documents this failure mode explicitly: the state given to the generator "is not necessarily the state that will be used for the generated command" ([stateful guide, Command generation](https://raw.githubusercontent.com/emil-e/rapidcheck/2c3c4365aca21ef4e612768fdc95b1ce8b39a651/doc/state.md)). Shrink unrelated objects and matching uses together; if a reduction changes a denied mutation into a missing-handle error, it has not preserved the chosen effect violation.

Keep original setup, actual operation sequence, raw outcomes/effects, resolved identity mapping and selected framework/build/configuration. Preserve the smallest demonstrated same-violation trace, with any unresolved replay material. Framework replay fields are necessary operational details, not a complete model of external nondeterminism ([fast-check replay, Replay model-based tests](https://raw.githubusercontent.com/dubzzz/fast-check/5ec2e3aceae60eb510b8b967bcb153274f3abad7/website/docs/advanced/model-based-testing.md), [Rapid replay handling, checkTB and checkFailFile](https://raw.githubusercontent.com/flyingmutant/rapid/6706a6fd83736ba24aaf55ef2621fdf00c2c27e8/engine.go)).

For protocol/session tests, derive states from the real protocol: establish, authenticate, use, close and reopen only if supported. Preserve opaque handles and transcript. Sequence validity and a session-state oracle do not supply controlled network or thread scheduling; use the pack's scheduling/history skills when that is the search dimension.
