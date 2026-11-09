# Improvement pass: JS/TS additions to semantic-differential-testing and configuration-differential-testing

Scope: every sentence added under `plugins/` in commit "Add React hydration and JS configuration factors to differential testing" (HEAD of `js-web-bugfinding`).

## Findings

### F1 every nodejs/node URL in both skills (15 occurrences, 7 files) — ERROR
- Said: Node.js v26.13.0 docs cited as `https://raw.githubusercontent.com/nodejs/node/daaa22aeddb87085542376ea1f4854dcea080baf/doc/api/<file>.md` (cli, packages, esm, deprecations, util, assert).
- Source: every such URL returns HTTP 404. `gh api repos/nodejs/node/git/ref/tags/v26.13.0` gives `"object":{"sha":"daaa22aeddb87085542376ea1f4854dcea080baf","type":"tag"}`; `gh api repos/nodejs/node/git/tags/daaa22ae…` gives `"object":{"sha":"18b32a3b1552e199a01f1a8d9fd64aa756d3b75b","type":"commit"}`, `"tag":"v26.13.0"`. The pinned SHA is the annotated tag object, which raw.githubusercontent.com does not serve. The same paths at `18b32a3b1552e199a01f1a8d9fd64aa756d3b75b` return 200.
- Fix: replaced `daaa22aeddb87085542376ea1f4854dcea080baf` with `18b32a3b1552e199a01f1a8d9fd64aa756d3b75b` in every file of both skills (no other skill uses the bad SHA). The quote checks below were done against the files at `18b32a3`.

### F2 semantic-differential-testing/references/comparison-and-normalization.md:24 — WARNING
- Said: "Two Promises from two runs therefore never compare equal, and objects from two separately loaded library copies differ by prototype even with equal data."
- Source: Node assert.md at 18b32a3 (https://raw.githubusercontent.com/nodejs/node/18b32a3b1552e199a01f1a8d9fd64aa756d3b75b/doc/api/assert.md), `assert.deepStrictEqual` "Comparison details": "[`[[Prototype]]`][prototype-spec] of objects are compared using the [`===` operator][]." That makes instances of a class defined in each copy unequal; a plain object or array built by either copy has the realm's shared `Object.prototype`/`Array.prototype` and is not distinguished. "objects ... differ by prototype" is stronger than the source.
- Fix: "objects" changed to "instances of classes defined in two separately loaded library copies".

### F3 configuration-differential-testing/references/sources.yaml:70 — WARNING
- Said: schedule.json entry `sections_used: - "v20 end 2026-04-30"`, but references/common-mistakes.md:86 also cites schedule.json for "27.x was Alpha on 2026-11-09".
- Source: schedule.json at 6065a83 (https://raw.githubusercontent.com/nodejs/Release/6065a837c0c151577f449c666fec019069ffba77/schedule.json): `"v27": {"alpha": "2026-10-28", "start": "2027-04-22", ...}`. The claim is entailed; the sources entry omits it.
- Fix: added `"v27 alpha 2026-10-28, current 2027-04-22"` to sections_used.

### F4 semantic-differential-testing/SKILL.md:32 and references/common-mistakes.md:145 — WARNING
- Said: SKILL.md: "Nessie compares two commits of one library and sorts differences into bug, bug fix and upgrade". common-mistakes.md: "Classify each difference ... as bug, bug fix or upgrade, as Nessie does".
- Source: Arteca et al. 2022 notes (C:/Users/Q/code/papers/Arteca_2022_NessieAutomaticallyTestingJavaScript/notes.md:209-210): "## Bugs found (Table 5, manual sample, p.1502)" / "Categories: Bug (commit introduces a bug), Bug fix, Upgrade". The oracle section (notes.md:201-207, p.1501) reports differences by kind (error vs success, return value, argument/callback parameter, callback called in one commit only, mocha internal async error); the three-way classification is the authors' manual inspection of a sample, not something Nessie does to each difference. comparison-and-normalization.md:30 already says this correctly ("sampled differences were classified").
- Fix: SKILL.md now says "and its authors sorted a manual sample of the differences into bug, bug fix and upgrade"; common-mistakes.md now says "as the Nessie authors did by hand for a sample".

## Checked and entailed (no edit)

Each was compared against the pinned raw file fetched this session (Node files at `18b32a3`):
- nodejs/Release README: 22.x/24.x "Maintenance LTS", 26.x "Active LTS", 27.x "Alpha", "Dates are subject to change." (line 15), 20.x End-of-Life 2026-04-30 (line 81).
- Node cli.md `TZ` (lines 4645-4670, `'Etc/UTC'`); packages.md lines 716 and 721 (key order; `"import"`/`"require"` hazards); esm.md lines 625-626 ("does not always correctly detect named exports"); deprecations.md DEP0205 lines 4574-4597 (Runtime since v26.0.0; "removed in a future version of Node.js"); util.md lines 1848-1870 (`skipPrototype`); assert.md lines 608-631 (Object.is, `===` prototype, enumerable own, Map/Set unordered, WeakMap/WeakSet/Promise "only equal if they reference the same object").
- React 19.3.1 (tag v19.3.1 = commit `61aa00d`, package.json `"version": "19.3.1"`): npm/index.js production/development selection; ReactDOMComponent.js `hydrateProperties` lines 3263-3285 (comment "Our requirement is not to produce perfect HTML and attributes"; only string/number/bigint children compared; `suppressHydrationWarning` skips it), attribute diffing inside `if (__DEV__)` in `diffHydratedProperties` (line 3321), `hydrateText` lines 3384-3398; ReactFiberHydrationContext.js `throwOnHydrationMismatch` lines 388-415 (message causes; diff only under `__DEV__`), `upgradeHydrationErrorsToRecoverable` 907-919, `emitPendingHydrationWarnings` 933-950 (`console.error` under `__DEV__`); codes.json 418, 421-424; formatProdErrorMessage "Minified React error #".
- react.dev at `7594a2b`: hydrateRoot (Caveats line 57, `identifierPrefix` line 47, Pitfall lines 192-197, suppression lines 240 and 274, `<!-- -->` line 251, `isClient` line 282, root error options lines 44-46); renderToString lines 54 and 127; renderToPipeableStream lines 61, 344, 437; flushSync line 56; useSyncExternalStore line 48; useId line 174; captureOwnerStack lines 54 and 386.
- Playwright at `95e5dca`: browsers.md line 590; test-projects-js.md line 8; emulation.md line 383 and colorScheme line 589.
- Jazzer.js at `f23bc5a`: fuzz-targets.md lines 110-119 (module.register, >= 20.6, function hooks >= 20.11); instrument.ts `registerEsmHooks` lines 330-406 (version checks; `register` in try; catch prints "WARN: [jazzer.js] Failed to register ESM loader hooks. ES modules will not be instrumented.").
- MDN at `0a6ff1e`: JSON.stringify lines 62, 69-71, 84, 325; structured clone lines 11-22 and supported types; Intl.DateTimeFormat lines 55 and 83. ECMA-262 at `828d35d`: Number::toString line 2151; SerializeJSONProperty finite Number → ToString line 48016.
- LambdaTester claims against Selakovic notes.md lines 88-93 (p.13 Def. 4.1, constructor-name serialization, empty/non-empty streams), 93 (p.16 warnings), 151 (pp.19-20 find), 207 (Node.js 8.5, pp.14, 21). Nessie claims against Arteca notes.md lines 90 (p.1499 re-implementation, ES6+), 201-207 (p.1501 logging, 10 runs, set comparison, ignored renames/Node version changes).

## Validation (after edits)

- `uv run --no-project --quiet --with pyyaml python C:/Users/Q/.codex/skills/.system/skill-creator/scripts/quick_validate.py plugins/bugfinding/skills/semantic-differential-testing` → `Skill is valid!` (exit 0); same for `configuration-differential-testing` → `Skill is valid!` (exit 0).
- Relative links (script over every `.md` in both skills): `broken relative links: none` for both.
- Cited URLs versus sources.yaml, both directions: `cited in md, missing from sources.yaml: none` and `in sources.yaml, not cited in md: none` for both skills.
- HTTP check of all 48 distinct URLs in both skills: 43 return 200 (all raw.githubusercontent.com links, including the 6 corrected Node links, plus releases.llvm.org and postgresql.org). Five got no status from curl: the two DOIs added in this commit return `HTTP/1.1 302 Found` to `https://dl.acm.org/doi/10.1145/3276531` and `https://dl.acm.org/doi/10.1145/3510003.3510106` (dl.acm.org refuses curl); csrc.nist.gov, tsapps.nist.gov and sqlite.org links predate this commit and were not investigated.
- `git diff --check -- plugins/bugfinding/skills/semantic-differential-testing plugins/bugfinding/skills/configuration-differential-testing reports/improve-js-differential.md` → no output, exit 0.
- `grep -rn daaa22a plugins/` → 0 matches.

