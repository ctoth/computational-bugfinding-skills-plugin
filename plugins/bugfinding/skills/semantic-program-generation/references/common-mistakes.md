# Common mistakes

Each entry gives the wrong move first, then the better move, then why.

## Generating references into an empty world

**Wrong:** `receiver = random_id()` over an empty world, then count compilation as deep semantic testing.

**Better:** Establish the required receiver/definition/state and observe the actual intended effect. Csmith picks "an appropriate target or defines a new one", so definitions are created on demand "at the time that Csmith decides to refer to them"; SQLite's dbsqlfuzz mutates "both the input database and the input SQL at the same time" ([Csmith, §2.3](https://users.cs.utah.edu/~regehr/papers/pldi11-preprint.pdf), [SQLite testing, §4.1.3](https://www.sqlite.org/testing.html)).

**Why:** context-sensitive construction and joint state/program search address different missing prerequisites; a compiled call on a missing receiver never reaches the operation.

## Keeping facts a mutation invalidated

**Wrong:** Keep an index, permission or lifetime fact after a later mutation invalidates it.

**Better:** Recompute the fact through the actual effect/control-flow boundary ([Csmith, §§2.4–2.5](https://users.cs.utah.edu/~regehr/papers/pldi11-preprint.pdf)).

**Why:** "loops and function calls threaten to invalidate previously validated code"; Csmith's locally safe dereference became unsafe once a loop backedge carried a null pointer.

## Treating every exception the same way

**Wrong:** Treat every exception as a bad generator, or accept every exception as exercising the success property.

**Better:** Select the intended valid/error lane and evaluate its specified behavior ([Csmith, §§2.1–2.4](https://users.cs.utah.edu/~regehr/papers/pldi11-preprint.pdf)).

**Why:** Csmith's requirement of "a single meaning according to the C standard" serves its differential comparison; it is not a universal rule for robustness or other languages.

## Shrinking into a different failure

**Wrong:** Delete setup until a wrong-effect finding becomes a missing-object error.

**Better:** Preserve the same valid semantic case and violation through every reduction step ([Csmith, §4](https://users.cs.utah.edu/~regehr/papers/pldi11-preprint.pdf)).

**Why:** existing C reducers "introduce undefined behavior. The resulting programs are small but useless."

## Trusting a domain library for semantics

**Wrong:** Assume a dependent-domain library establishes object lifetime/effects or safe domain arithmetic.

**Better:** Check the target's relationships explicitly in the domain construction ([FuzzTest domains, FlatMap and Filter](https://raw.githubusercontent.com/google/fuzztest/1b4e4f0e4c446aca4660c43a28ec1b8d893b6510/doc/domains-reference.md)).

**Why:** combinators only compose the values you define; the reference's own `Map` example must bound inputs to avoid "integer overflow", and "too restrictive filter functions will trigger an abort in the framework".

## Counting volume or coverage as bugs

**Wrong:** Declare more generated programs or higher ordinary coverage to be more confirmed bugs.

**Better:** Keep semantic reach, cost, candidates and adjudicated findings separate ([Csmith, §§3.3 and 3.5](https://users.cs.utah.edu/~regehr/papers/pldi11-preprint.pdf)).

**Why:** Csmith's crash-detection rate "varies significantly as a function of the sizes", and its incremental coverage was "so small as to be a negative result" despite its discoveries.
