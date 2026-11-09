# Matched state and observable effects

Use this when compared operations depend on objects, sessions or prior work. The following design procedure extends paired comparison to a target's actual state contract; it is not a generic engine adapter. SQLancer's replay logs include database setup because the query alone does not identify the case: the log holds the last query "along with the other statements to set up the database state" ([SQLancer README, Logs](https://raw.githubusercontent.com/sqlancer/sqlancer/a7d60ee450e6a22ca38599c14e984a49773f4745/README.md)).

## Choose the replay unit

- **Independent operation:** restore the relevant logical state through an existing supported fixture/reset owner, execute one case, observe the promised effects and discard its state.
- **Dependent sequence:** replay setup and the operation prefix through public producers, comparing the relevant states along the sequence. Do not remove a lifecycle transition simply because its final visible fields resemble another setup.
- **Execution-mode comparison:** match the starting state and behavioral guarantee while varying a supported strategy. SQLite uses optimization-on/off comparisons for answer tests, but "Not all test cases can be handled this way": tests that count disk accesses, sorts or scan steps "will appear to fail when optimizations are disabled" ([SQLite testing, §9](https://www.sqlite.org/testing.html)).

The independent/sequence choice is this pack's experiment design. Inspect the real runner to establish which one it currently provides. In a batched worker, initially equal fixtures do not establish equal later pre-states after earlier operations; inspect or replay the causal prefix before interpreting a later mismatch ([SQLancer README, Logs and Reducing bugs](https://raw.githubusercontent.com/sqlancer/sqlancer/a7d60ee450e6a22ca38599c14e984a49773f4745/README.md)).

## Define logical observations

Derive the observation from the target's public guarantee, not its internal serialization. For an effectful object operation, a proposed observation can include the returned value/error, reachable property values, identity/alias relationships and allowed external output. For recovery, use acknowledged operations and recovered state under a specified failure model; same-answer checking does not replace storage-order/failure testing. SQLite's journal-test VFS checks "that nothing is written into the database file" before it is written and synced to the rollback journal, separately from its answer comparisons ([SQLite testing, §§3, 8.5 and 9](https://www.sqlite.org/testing.html)).

When implementations allocate different physical handles, retain a justified correspondence between logical identities. The mapping must preserve equality, reuse and alias relationships required by the contract. Mapping every handle to the same placeholder would remove that information. This is an observation-design consequence, not a promised general-purpose identity library; use the target's existing supported observations and retain both raw states. SQLancer's DQE is a real producer that makes row identity explicit before comparing effects: "We append two extra columns to each table in a database to uniquely identify each row and track whether a row has been modified" ([SQLancer README, Approaches and Papers: DQE](https://raw.githubusercontent.com/sqlancer/sqlancer/a7d60ee450e6a22ca38599c14e984a49773f4745/README.md)).

Record observer effects too. If the observation itself changes a session/cache/world, define the comparison boundary accordingly. Unsupported observation or an unavailable state-establishing prefix leaves the comparison unresolved rather than proving an implementation difference. Use `correctness-oracles` to settle the guarantee before building a new query/reset seam. SQLancer logs "every SQL statement that is sent to the DBMS" by default, and its CODDTest oracle states its observation assumption explicitly: "we can assume the database state to be constant for a database session" ([SQLancer README, Logs and Approaches and Papers: CODDTest](https://raw.githubusercontent.com/sqlancer/sqlancer/a7d60ee450e6a22ca38599c14e984a49773f4745/README.md)).

### JavaScript server and client environments

When a server render and a browser render, or two Node processes, must start from matched conditions, control each documented source of difference rather than normalizing its output. React's hydration mismatch message lists `typeof window` branches, "`Date.now()` or `Math.random()`", "Date formatting in a user's locale which doesn't match the server" and external data sent without a snapshot ([`throwOnHydrationMismatch`](https://raw.githubusercontent.com/facebook/react/61aa00df822d0eb76d0362eb8b6fdd3527693efe/packages/react-reconciler/src/ReactFiberHydrationContext.js)).

| Source | Control |
|---|---|
| Time, `Math.random()` | Pass the value in as data; `suppressHydrationWarning` only for one unavoidable element ([hydrateRoot](https://raw.githubusercontent.com/reactjs/react.dev/7594a2b008489121bdf25f97320d11ac0422510e/src/content/reference/react-dom/client/hydrateRoot.md)) |
| `Intl` locale and time zone | Pass explicit `locales` and `timeZone`; the defaults are "the runtime's default locale" and "the runtime's time zone" ([MDN `Intl.DateTimeFormat()`](https://raw.githubusercontent.com/mdn/content/0a6ff1e3b8887f979b66c34cefdb73f846041879/files/en-us/web/javascript/reference/global_objects/intl/datetimeformat/datetimeformat/index.md)) |
| Server time zone | Node reads the `TZ` environment variable, with IDs such as `'Etc/UTC'` ([Node CLI, `TZ`](https://raw.githubusercontent.com/nodejs/node/18b32a3b1552e199a01f1a8d9fd64aa756d3b75b/doc/api/cli.md)) |
| Browser time zone and locale | Playwright `timezoneId` and `locale`; this "only affects the browser timezone and locale, not the test runner timezone" ([Playwright emulation](https://raw.githubusercontent.com/microsoft/playwright/95e5dca31981bcd0970165853fcc713269d2433a/docs/src/emulation.md)) |
| `typeof window`, `window.matchMedia` | Two-pass `isClient` render for intended differences (hydrateRoot); Playwright `colorScheme` emulation for media queries (Playwright emulation) |
| `useId` | Identical tree and the same `identifierPrefix` on both sides ([useId](https://raw.githubusercontent.com/reactjs/react.dev/7594a2b008489121bdf25f97320d11ac0422510e/src/content/reference/react/useId.md)) |
| External store data | `getServerSnapshot` returning the serialized server data; "The server snapshot must be the same between the client and the server" ([useSyncExternalStore](https://raw.githubusercontent.com/reactjs/react.dev/7594a2b008489121bdf25f97320d11ac0422510e/src/content/reference/react/useSyncExternalStore.md)) |
| Whitespace, invalid nesting, browser extensions | Not render controls; use them to adjudicate a mismatch seen only in a real browser (hydrateRoot; `throwOnHydrationMismatch`) |

Record the values each side actually used, not only the requested settings.

## Localize before reducing

Keep setup, workload and paired raw observations together. If a sequence diverges, identify the earliest demonstrated unequal observable state where possible; later output differences may depend on it. Shrink the prefix and operation together, re-establishing validity on both sides. Retain the original if a smaller case changes the selected mismatch or loses legal state; invalid reduction is a documented wrong-code hazard: reduced C programs with new undefined behavior "are small but useless" ([Csmith, §4](https://users.cs.utah.edu/~regehr/papers/pldi11-preprint.pdf)).
