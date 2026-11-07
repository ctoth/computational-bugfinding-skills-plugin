# Semantic environments

## Keep facts for the selected operation

First identify the guarantee and the real producer that can exercise it. Csmith maintains global definitions and local context, effects and points-to information while constructing code; safety checks decide whether to commit a fragment. Apply that reasoning at the smallest useful scope rather than reproduce its C-specific analysis in another runtime ([Csmith, §2.3](https://users.cs.utah.edu/~regehr/papers/pldi11-preprint.pdf)).

| Needed behavior | Constructive generation decision | Revalidate after |
|---|---|---|
| Successful lookup/mutation | Establish a live receiver and its required definition through supported setup | Deletion, definition replacement, permission change |
| Valid indexed operation | Establish a nonempty collection; derive index from its actual range | Length change, alias mutation, integer conversion |
| Legal alias/effect interaction | Track identities and operations whose effects can invalidate later assumptions | Calls, branches, exceptions, loop closure |
| A specified denied operation | Establish the actual forbidden relation, then check its documented error and permitted effects | Principal/capability or target state changes |

These rows are design adaptations, not claims about a particular language's permission or error semantics. Derive their precise rules from that target. Csmith's initialization, pointer, array and effect checks show why independent random operands cannot establish all these relationships ([Csmith, §2.4](https://users.cs.utah.edu/~regehr/papers/pldi11-preprint.pdf)).

## Preserve useful error testing

For malformed-input or invalid-operation robustness, the error path may be the intended behavior. For an optimizer result comparison, undefined behavior may invalidate the comparison. Name the lane instead of globally rejecting every runtime error or accepting every error as a successful semantic test ([Csmith, §§2.1–2.4](https://users.cs.utah.edu/~regehr/papers/pldi11-preprint.pdf)).

## Follow effects through control flow

Example: a generated dereference is safe when its pointer targets a local variable, but a later loop-body assignment can supply a null pointer on the next iteration. The earlier local check no longer establishes safety after the backedge. Csmith analyzes this interaction when closing loops; retain the analogous facts your target actually needs at joins, calls and exception boundaries ([Csmith, §2.5](https://users.cs.utah.edu/~regehr/papers/pldi11-preprint.pdf)).

## Worked permissioned-world experiment

This is an illustrative design, not an executed finding. Given a documented permitted-mutation guarantee:

1. Use existing fixture/API owners to create the minimum receiver, definition and principal relationships.
2. Generate program IR that uses those actual identities and satisfies the operation's prerequisites.
3. Execute from that world and observe the promised state effect as well as the returned result/error.
4. Vary supported aliasing, inheritance or exception interactions; update the facts each can invalidate.
5. Reduce unrelated entities and program fragments while retaining the operation and the same effect violation.

The design combines environment/effect-aware construction with joint state/program search. The target's actual semantics must supply its concrete oracle; SQLite's reported combined database-and-SQL search is a precedent, not proof that this experiment will find a bug ([Csmith, §§2.3–2.5](https://users.cs.utah.edu/~regehr/papers/pldi11-preprint.pdf), [SQLite testing, §4.1.3](https://www.sqlite.org/testing.html)).
