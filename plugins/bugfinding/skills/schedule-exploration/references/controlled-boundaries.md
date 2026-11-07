# Controlled boundaries

## Choose the scenario and observer

Start from a real producer and a documented guarantee. Map each decisive transition to the controller's actual event boundary, and identify initialization, dependency internals and external inputs outside it. CHESS distinguishes replay/reset from alternative exploration and shows how atomic component scoping omits internal interactions: not preempting inside selected modules gains scalability "at the cost of missing bugs resulting from adverse interactions" ([CHESS, §§3, 4.1, 4.4.1](https://www.microsoft.com/en-us/research/wp-content/uploads/2016/02/osdi2008-CHESS.pdf)).

Use the existing integration's event/identity model. Different object names alone do not justify pruning orders: actual operation independence is what partial-order reduction needs. Keep fairness and scheduling-point assumptions explicit; a progress counterexample under an inadmissible fairness model does not establish the application's promised liveness failure. Detecting liveness violations "fundamentally requires the fair scheduling capability" ([CHESS, §§4.3–4.5](https://www.microsoft.com/en-us/research/wp-content/uploads/2016/02/osdi2008-CHESS.pdf)).

## Worked extension beyond a held pair

This is an illustrative application design, not an executed product finding:

1. Read the target's actual validation, competing mutation, publication and retry paths. Select a promised state/history invariant and a valid initial world through existing producers.
2. Inventory currently held interleavings. Where an existing controller/seam exposes more decisions, vary admissible orderings and workload values independently. Retain the actual choices that reach the observer.
3. Use a supported semantic assertion or history checker. An absence of memory-access races does not supply this invariant; CHESS calls monitoring an "orthogonal but important problem" relative to driving interleavings ([CHESS, §4.5](https://www.microsoft.com/en-us/research/wp-content/uploads/2016/02/osdi2008-CHESS.pdf)).
4. On failure, replay world plus workload plus choices. If a hidden dependency or initialization prevents replay, preserve that limit rather than describe the schedule as deterministic.

The steps adapt CHESS's separation of scenario, choices and monitoring; they do not prescribe a new scheduler, wrapper library or event protocol ([CHESS, §§3–4](https://www.microsoft.com/en-us/research/wp-content/uploads/2016/02/osdi2008-CHESS.pdf)).

## Report the model actually explored

Loom requires replacement types in relevant dependencies ("that library must _also_ be augmented"); with hidden operations, "certain executions that are possible in the real world won't be modeled". Coyote's pass-through dependencies and supported APIs similarly delimit exploration, and rewriting more code adds scheduling decisions, which "_exponentially_ increases how much time you need to test". Treat additional instrumentation as a target-specific decision with costs and semantics to verify, not automatic proof of full-process control ([Loom, Intrusive Implementation](https://docs.rs/loom/0.7.2/loom/), [Coyote, Which DLLs to rewrite?](https://raw.githubusercontent.com/microsoft/coyote/2202e75a861f4e8a63149366c2e41ea21d73ae54/docs/concepts/binary-rewriting.md)).
