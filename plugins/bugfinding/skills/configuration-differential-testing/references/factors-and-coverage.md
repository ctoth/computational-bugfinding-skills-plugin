# Factor model and exercised coverage

This is the pack's experiment-design procedure. Use the target's real supported contracts and producers; the literature supplies coverage distinctions, not a ready target model; value selection stays a modeling choice, and "test effectiveness is also dependent on the values selected" ([Kuhn et al., §II, p.2](https://tsapps.nist.gov/publication/get_pdf.cfm?pub_id=917142)).

For each factor save its requested value, concrete control (binary, build option, runtime setting or platform), documented support constraint, effective-value observation, and the guarantee tested. An unavailable runner is unexecuted support, not evidence of product invalidity. A capability documented to fall back when absent must remain in the valid domain; do not constrain away its crash. PICT constraints "express inherent limitations of the modelled domain", not observed failures ([PICT, Constraints](https://raw.githubusercontent.com/microsoft/pict/ab76c2548f551fcb46314e58653a1bd1172f3a72/doc/pict.md)).

Separate semantic classes before comparison: a relaxed numeric mode, deliberately stale read mode or different format version may change the promise. Establish shared input/state preconditions and observe the actual promised result/effects. This is contract selection, not a covering-array feature: the paper's fault-coverage model assumes "deterministic software that computes the same output" for one system under test ([Kuhn et al., §III, p.3](https://tsapps.nist.gov/publication/get_pdf.cfm?pub_id=917142)); the detailed paired oracle belongs to `semantic-differential-testing`.

## Define the constrained universe

For factor subset J, define V_J as tuples extendable to at least one supported full configuration; define E_J from configurations whose relevant test and oracle actually executed. The proposed constrained measure is |E_J|/|V_J|, with empty denominators explicit. It adapts the paper's simple t-way, total variable-value and minimum-coverage distinctions (in its Table I, simple 2-way coverage is 33% while total variable-value coverage is 79%); it is not its theorem about fault detection ([Kuhn et al., §II, pp.2–3](https://tsapps.nist.gov/publication/get_pdf.cfm?pub_id=917142)).

Save model/constraint provenance, exclusions, generated rows and actual execution dispositions. A tuple's occurrence in a table is less evidence than its execution with a relevant input. Report the tested input family too: configuration-only coverage on inert inputs can omit the decisive branch values; for predicates on "internal variables not included in the test set", the paper's branch condition must be validated by inspecting internal state, which it says "may in most cases be impractical" ([Kuhn et al., §IV, p.7](https://tsapps.nist.gov/publication/get_pdf.cfm?pub_id=917142)).

Use exhaustive valid rows for small domains. Otherwise state chosen strength, higher-order groups, regression rows and untested residual space. PICT sub-models are parameter groups that "get their own combinatory orders"; its packing heuristics are not a universal strength policy ([PICT, Sub-Models](https://raw.githubusercontent.com/microsoft/pict/ab76c2548f551fcb46314e58653a1bd1172f3a72/doc/pict.md)).

## Illustrative capability model

The following names are invented. The implication is legitimate only if the actual target requires the capability; a promised fallback would make this exclusion wrong ([PICT, Constraints and Conditional Constraints](https://raw.githubusercontent.com/microsoft/pict/ab76c2548f551fcb46314e58653a1bd1172f3a72/doc/pict.md)):

```text
Runtime: base, candidate
Backend: portable, accelerated
Capability: absent, present
Optimize: off, on
IF [Backend] = "accelerated" THEN [Capability] = "present";
```

A supported failing tuple remains in the campaign. Record unsupported syntax, an ignored option and a genuine supported build failure separately; adjusting constraints merely to remove red output changes the experiment.

## JavaScript and React factors

Illustrative model in the same PICT format. Take the values from the target's `engines` field, `package.json` `"exports"`, Playwright projects and build scripts, not from this list:

```text
Node: 22, 24, 26
Load: esm, cjs
ReactBuild: development, production
Browser: chromium, firefox, webkit
```

On 2026-11-09 the nodejs/Release table listed 22.x and 24.x as Maintenance LTS, 26.x as Active LTS and 27.x as Alpha, with "Dates are subject to change"; 20.x ended on 2026-04-30 ([README](https://raw.githubusercontent.com/nodejs/Release/6065a837c0c151577f449c666fec019069ffba77/README.md), [schedule.json](https://raw.githubusercontent.com/nodejs/Release/6065a837c0c151577f449c666fec019069ffba77/schedule.json)). Re-read it for each campaign.

| Factor | Requested control | Effective-value evidence | Notes |
|---|---|---|---|
| Node | CI image or version manager | `process.version` | Server and Node lanes only |
| Load | entry file, `"type"`, `import` versus `require` | resolved file path per run via `import.meta.resolve` or `require.resolve` | In `"exports"` "key order is significant" and "the `"import"` and `"require"` conditions can lead to some hazards" ([Node packages](https://raw.githubusercontent.com/nodejs/node/daaa22aeddb87085542376ea1f4854dcea080baf/doc/api/packages.md)); CommonJS named exports seen from ESM come from detection that "does not always correctly detect named exports" ([Node ESM](https://raw.githubusercontent.com/nodejs/node/daaa22aeddb87085542376ea1f4854dcea080baf/doc/api/esm.md)) |
| ReactBuild | bundler `process.env.NODE_ENV` | proposed, unexecuted probe: `typeof React.captureOwnerStack`, since it "is only exported in development builds" and "will be `undefined` in production builds" ([captureOwnerStack](https://raw.githubusercontent.com/reactjs/react.dev/7594a2b008489121bdf25f97320d11ac0422510e/src/content/reference/react/captureOwnerStack.md)) | React's npm entry loads `./cjs/react.production.js` when `process.env.NODE_ENV === 'production'` and the development file otherwise ([react npm index](https://raw.githubusercontent.com/facebook/react/61aa00df822d0eb76d0362eb8b6fdd3527693efe/packages/react/npm/index.js)); the build changes what hydration reports (see `semantic-differential-testing`) |
| Browser | Playwright `--project` | Playwright version and browser version recorded per run (probe not checked in the docs) | Client lanes only; Playwright's WebKit "is derived from the latest WebKit main branch sources" and "doesn't work with the branded version of Safari" ([Playwright browsers](https://raw.githubusercontent.com/microsoft/playwright/95e5dca31981bcd0970165853fcc713269d2433a/docs/src/browsers.md)); a project is a "group of tests running with the same configuration" ([Playwright projects](https://raw.githubusercontent.com/microsoft/playwright/95e5dca31981bcd0970165853fcc713269d2433a/docs/src/test-projects-js.md)) |

`Browser` applies to client lanes and `Node` to server lanes: run them as separate sub-models or record "n/a" instead of inventing constraints. A package with no CommonJS entry makes `Load` single-valued by contract, not by constraint.

Load also changes Jazzer.js instrumentation. Jazzer.js instruments ESM through `module.register` and requires Node.js 20.6, or 20.11 for function hooks ([Jazzer.js fuzz targets](https://raw.githubusercontent.com/CodeIntelligenceTesting/jazzer.js/f23bc5aeb7a6d50cd6256cfc3be44b868da5e7b1/docs/fuzz-targets.md)), so on the lines above that floor adds no constraint. Node.js 26 runtime-deprecates `module.register` as DEP0205, and it "will be removed in a future version of Node.js" ([Node deprecations](https://raw.githubusercontent.com/nodejs/node/daaa22aeddb87085542376ea1f4854dcea080baf/doc/api/deprecations.md)). If registration throws, Jazzer.js prints "Failed to register ESM loader hooks. ES modules will not be instrumented." and continues ([instrument.ts, `registerEsmHooks`](https://raw.githubusercontent.com/CodeIntelligenceTesting/jazzer.js/f23bc5aeb7a6d50cd6256cfc3be44b868da5e7b1/packages/instrumentor/instrument.ts)). Treat Node × Load as an interaction to execute, and use the absence of that warning plus rising coverage on ESM code as effective-value evidence; behavior on Node.js 26 was not run.
