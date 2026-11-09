# Common mistakes

Each entry is **Wrong** first, then **Right**, then why.

## Treating the same input file as comparable semantics

**Wrong:** "Both compilers got the same C file, so any output difference is a compiler bug."

**Right:** Check the effective contract and implementation-defined target class first; Csmith compares "within an equivalence class but not across classes" ([Csmith, §2.6](https://users.cs.utah.edu/~regehr/papers/pldi11-preprint.pdf)).

**Why:** Csmith programs "do not generate the same output across compilers" that differ in integer width or signed behavior, so the difference can be legal.

## Assuming a shared initial fixture keeps every batched case equivalent

**Wrong:** "Both workers started from the same database copy, so case 40's mismatch is about case 40."

**Right:** Inspect the producer and preserve or re-establish the relevant setup or causal prefix; SQLancer logs the failing query "along with the other statements to set up the database state" ([SQLancer README, Logs](https://raw.githubusercontent.com/sqlancer/sqlancer/a7d60ee450e6a22ca38599c14e984a49773f4745/README.md)).

**Why:** earlier effects can diverge the two worlds, so the query alone does not identify the case.

## Treating equal returned values as equal effects

**Wrong:** "Both calls returned `1`, so the implementations agree."

**Right:** Observe the promised state/output boundary; SQLite runs "exactly the same answer" optimization comparisons separately from journal and anomaly tests ([SQLite testing, §§3, 8.5 and 9](https://www.sqlite.org/testing.html)).

**Why:** a return-only observer accepts any pair whose world effects differ behind the same return.

## Sorting everything or comparing sets universally

**Wrong:** Sort both result lists, deduplicate them and compare.

**Right:** Derive order and multiplicity from the contract and retain complete required rows: `SELECT ALL` keeps rows "including duplicates", and unsorted order "must not be relied on" ([PostgreSQL 18 SELECT, Description step 6](https://www.postgresql.org/docs/18/sql-select.html), [§7.5 Sorting Rows](https://www.postgresql.org/docs/18/queries-order.html)).

**Why:** sorting hides a promised-order violation and deduplication hides lost or extra duplicate rows.

## Trusting a helper named result equality to compare every result dimension

**Wrong:** "The oracle calls `assumeResultSetsAreEqual`, so full rows are compared."

**Right:** Read its actual caller and extraction/comparison path; SQLancer's helper reads `result.getString(1)` and compares size plus `HashSet` contents, and the MySQL DQP caller uses it ([SQLancer comparator](https://raw.githubusercontent.com/sqlancer/sqlancer/a7d60ee450e6a22ca38599c14e984a49773f4745/src/sqlancer/ComparatorHelper.java), [real DQP caller](https://raw.githubusercontent.com/sqlancer/sqlancer/a7d60ee450e6a22ca38599c14e984a49773f4745/src/sqlancer/mysql/oracle/MySQLDQPOracle.java)).

**Why:** other columns and per-value multiplicities are never observed by that path.

## Counting a missing output or expected-error skip as agreement

**Wrong:** "No assertion fired, so the two runs matched."

**Right:** Keep skipped comparisons separate from successfully evaluated equality; SQLancer's helper throws `IgnoreMeException` for a null result or an expected error ([SQLancer comparator, `getResultSetFirstColumnAsString`](https://raw.githubusercontent.com/sqlancer/sqlancer/a7d60ee450e6a22ca38599c14e984a49773f4745/src/sqlancer/ComparatorHelper.java)).

**Why:** a skipped case never reached the comparison, so it is no evidence either way.

## Declaring the majority implementation correct

**Wrong:** "Two of three engines agree, so the third is buggy."

**Right:** Treat disagreement as evidence to adjudicate against the contract; Csmith verifies failure-inducing programs "by hand" and calls an undetected shared wrong answer "an inherent limitation of differential testing without an oracle" ([Csmith, §2.6](https://users.cs.utah.edu/~regehr/papers/pldi11-preprint.pdf)).

**Why:** agreeing implementations can share a wrong answer.

## Accepting any smaller mismatch as the reduced finding

**Wrong:** Keep whatever the reducer emits as long as the outputs still differ.

**Right:** Revalidate input validity and the selected mismatch after shrinking; Csmith found reduced C programs with new undefined behavior "are small but useless", and LLVM's first step is to "make sure it is not using undefined behavior" ([Csmith, §4](https://users.cs.utah.edu/~regehr/papers/pldi11-preprint.pdf), [LLVM 23.1.0 Miscompilations](https://releases.llvm.org/23.1.0/docs/HowToSubmitABug.html#miscompilations)).

**Why:** a reducer can swap the original defect for an invalid input that differs for a different reason.

## Reading a silent production hydration as agreement

**Wrong:** "No `onRecoverableError` fired in production, so server and client rendered the same thing."

**Right:** Compare the server HTML against a client render directly, or also run a development build; production `hydrateProperties` compares text children only, and attribute mismatches reach a `console.error` inside `if (__DEV__)` ([ReactDOMComponent.js](https://raw.githubusercontent.com/facebook/react/61aa00df822d0eb76d0362eb8b6fdd3527693efe/packages/react-dom-bindings/src/client/ReactDOMComponent.js), [ReactFiberHydrationContext.js](https://raw.githubusercontent.com/facebook/react/61aa00df822d0eb76d0362eb8b6fdd3527693efe/packages/react-reconciler/src/ReactFiberHydrationContext.js)).

**Why:** the production observer cannot see the attribute dimension of the identity contract.

## Diffing a `createRoot` render against server HTML

**Wrong:** Render with `createRoot` and `flushSync` in the browser and diff `innerHTML` against the server HTML.

**Right:** Compare server `renderToString` with in-browser `renderToString` (a proposed, unexecuted comparator) and keep real hydration as a second observation; `flushSync` "may run pending Effects" ([flushSync](https://raw.githubusercontent.com/reactjs/react.dev/7594a2b008489121bdf25f97320d11ac0422510e/src/content/reference/react-dom/flushSync.md)) and `getServerSnapshot` is used "only during server rendering and during hydration" ([useSyncExternalStore](https://raw.githubusercontent.com/reactjs/react.dev/7594a2b008489121bdf25f97320d11ac0422510e/src/content/reference/react/useSyncExternalStore.md)).

**Why:** legal two-pass components and store snapshots look like mismatches, and SSR's `<!-- -->` text separators differ from client DOM ([hydrateRoot](https://raw.githubusercontent.com/reactjs/react.dev/7594a2b008489121bdf25f97320d11ac0422510e/src/content/reference/react-dom/client/hydrateRoot.md)).

## Adding `suppressHydrationWarning` to make the pair pass

**Wrong:** Put `suppressHydrationWarning` on the element that keeps failing.

**Right:** Use it only for one documented, unavoidably different element and exclude that element from the equality claim; it "only works one level deep" and React "will **not** attempt to patch mismatched text content" ([hydrateRoot](https://raw.githubusercontent.com/reactjs/react.dev/7594a2b008489121bdf25f97320d11ac0422510e/src/content/reference/react-dom/client/hydrateRoot.md)).

**Why:** in production it also disables the text check for that element ([ReactDOMComponent.js, `hydrateProperties` and `hydrateText`](https://raw.githubusercontent.com/facebook/react/61aa00df822d0eb76d0362eb8b6fdd3527693efe/packages/react-dom-bindings/src/client/ReactDOMComponent.js)), so the server text stays and nothing reports it.

## Matching production hydration errors by message text

**Wrong:** Search production `onRecoverableError` messages for "Hydration failed".

**Right:** Match on the error code (418, 421 to 424) ([codes.json](https://raw.githubusercontent.com/facebook/react/61aa00df822d0eb76d0362eb8b6fdd3527693efe/scripts/error-codes/codes.json)).

**Why:** production builds emit "Minified React error #" plus the code instead of the full message ([formatProdErrorMessage](https://raw.githubusercontent.com/facebook/react/61aa00df822d0eb76d0362eb8b6fdd3527693efe/packages/shared/formatProdErrorMessage.js)).

## Saving server HTML at `onShellReady`

**Wrong:** Capture the streamed HTML when `onShellReady` fires.

**Right:** Save after `onAllReady`, or use the `renderToString` string; `onAllReady` output "will contain the final HTML" ([renderToPipeableStream](https://raw.githubusercontent.com/reactjs/react.dev/7594a2b008489121bdf25f97320d11ac0422510e/src/content/reference/react-dom/server/renderToPipeableStream.md)).

**Why:** at `onShellReady` "components in nested `<Suspense>` boundaries might still be loading data", so the server observation is incomplete.

## Comparing JavaScript results with `JSON.stringify`

**Wrong:** `JSON.stringify(a) === JSON.stringify(b)` across two library versions.

**Right:** Use a serializer that tags `undefined`, `NaN`, `Infinity`, `-0`, Map, Set, BigInt and cycles; JSON omits or nulls `undefined`, nulls `NaN` and `Infinity`, turns Map and Set into `"{}"` and throws on cycles and BigInt ([MDN `JSON.stringify()`](https://raw.githubusercontent.com/mdn/content/0a6ff1e3b8887f979b66c34cefdb73f846041879/files/en-us/web/javascript/reference/global_objects/json/stringify/index.md)).

**Why:** distinct results collapse to one string; `-0` also prints as `"0"` ([ECMA-262, Number::toString](https://raw.githubusercontent.com/tc39/ecma262/828d35d00f8584c4a0fbcac7742b57c7b959c3f3/spec.html)).

## Deep-comparing values from two library copies

**Wrong:** `util.isDeepStrictEqual(resultV1, resultV2)` where the results come from two loaded versions or contain Promises.

**Right:** Compare settled values and constructor names, or set `skipPrototype` deliberately ([Node util](https://raw.githubusercontent.com/nodejs/node/daaa22aeddb87085542376ea1f4854dcea080baf/doc/api/util.md)).

**Why:** prototypes are compared with `===` and Promises are "only equal if they reference the same object" ([Node assert, Comparison details](https://raw.githubusercontent.com/nodejs/node/daaa22aeddb87085542376ea1f4854dcea080baf/doc/api/assert.md)).

## Comparing only the return value of a higher-order function

**Wrong:** "Both `find` implementations returned `undefined`, so they agree."

**Right:** Record callback arguments at every invocation and the invocation count (LambdaTester, [Selakovic et al. 2018, Def. 4.1, p.13](https://doi.org/10.1145/3276531)), plus arguments before and after each call (Nessie, [Arteca et al. 2022, p.1501](https://doi.org/10.1145/3510003.3510106)).

**Why:** the polyfill.io `find` difference returns `undefined` on both sides and shows only in callback count (Selakovic et al., pp.19–20).

## Running each asynchronous test once per version

**Wrong:** Run every async test once on each version and report any difference.

**Right:** Repeat each test and compare output sets; report only an output never seen on the other side. Nessie runs each test 10 times per commit for this ([Arteca et al. 2022, p.1501](https://doi.org/10.1145/3510003.3510106)).

**Why:** callback and scheduling order can vary between runs of the same version.

## Calling every cross-version difference a bug

**Wrong:** "Version 2 behaves differently from version 1, so version 2 has a bug."

**Right:** Classify each difference against the changelog and contract as bug, bug fix or upgrade, as Nessie does ([Arteca et al. 2022, p.1502](https://doi.org/10.1145/3510003.3510106)).

**Why:** intended API changes produce differences, and Nessie had to configure out renames and supported Node.js version changes by hand (p.1501).
