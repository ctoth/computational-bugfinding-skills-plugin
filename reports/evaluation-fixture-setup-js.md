# Evaluation fixture setup: JS/TS (Node and React)

Status: complete. Three public scenarios (c Node, d React, e control), private key and private self-test written; self-test passes 19/19 (two runs). Nothing committed or pushed; nothing in the plugin repo touched except this report.

Workspace: `C:/Users/Q/code/bugfinding-skill-evaluation/` (not a git repo). Scenarios a and b (Python) and their key were not read or modified.

## Log

1. Read `reports/evaluation-fixture-setup.md` (pattern) and plan "Build pipeline" step 4 (`reports/skill-plan-js-web-bugfinding.md:104-107`). Tooling: node v22.18.0, npm 11.19.1.
2. Version choice for scenario-d (from `npm view`, 2026-11-09): react 19.3.1, react-dom 19.3.1, @testing-library/react 16.3.3, @testing-library/dom 10.4.2 (required peer of RTL 16). Latest jsdom is 31.0.0, but its `engines` is `node: '^22.22.2 || ^24.15.0 || >=26.0.0'`, which excludes the installed 22.18.0; the same holds for 30.x. Pinned jsdom 29.1.1 (`engines: ^20.19.0 || ^22.13.0 || >=24.0.0`), the newest that accepts Node 22.18.0.
3. Test runner choice: `node:test` plus jsdom, components written with `React.createElement` (no JSX), so the server entry, client entry, demo test and private self-test all run in plain Node with no transpiler and no vitest/esbuild install.
4. scenario-c written: `package.json` (no dependencies), `contract.md`, `src/server.js`, `src/store.js`, `src/loader.js`, `demo.js`. `node demo.js` in scenario-c exited 0 with every response matching the contract (201, 200 x3, 409 insufficient_funds, 200, EUR 5850, 400 unsupported_currency, 404, 400 invalid_id, loader results). A probe of the id pattern on `"a".repeat(n) + "!"` gave 9.4, 2.4, 9.4, 38.7, 147.6 ms for n = 16..24 step 2 (about 4x per +2 from n=18 on).
5. scenario-d: `npm install --no-audit --no-fund` in scenario-d only: "added 58 packages in 6s", exit 0. Wrote `package.json`, `contract.md`, `src/App.js`, `src/tasks.js`, `src/server.js`, `src/client.js`, `test/setup-dom.js`, `test/demo.test.js`. `npm test` (= `node --test test/demo.test.js`): 3 tests, 3 pass, 0 fail, exit 0, duration 3089 ms.
6. scenario-e (control, Node, no planted defect): `package.json` (no dependencies), `contract.md`, `src/server.js`, `src/store.js`, `src/keyed-lock.js`, `src/price-cache.js`, `demo.js`. Same shape as scenario-c (async store, id pattern, callback-style memoizing helper) so false findings on look-alike code can be measured. `node demo.js` in scenario-e exited 0, all responses per contract. Added to both Node contracts: callbacks passed to the helper must not throw (behavior unspecified), so a throwing callback is not counted as a finding in either scenario.
7. Private key `private-evaluation-key-js.md` and self-test `fixture_selftest_js.mjs` written at the workspace root (outside every public directory). First self-test run: 18 tests, 17 pass, 1 fail. The failing check measured an unrelated GET during a slow id request with the server in the same process as the client; the client shares the blocked event loop, so the measurement could not show the stall (15.4 ms). Fix: that check now starts the server in a child process (`spawn(process.execPath, ['--input-type=module', '-e', ...])`). Reruns below.
8. Hint scan: case-insensitive search for `bug|defect|race|leak|todo|fixme|backtrack|redos|mismatch|stale` over scenario-c, scenario-d (excluding node_modules) and scenario-e: no matches except a substring inside an integrity hash in `scenario-d/package-lock.json:245`.

## Public paths

Give an evaluator one directory only.

| Scenario | Directory | Kind | Run |
| --- | --- | --- | --- |
| C | `C:/Users/Q/code/bugfinding-skill-evaluation/scenario-c/` | Node 22 `node:http` ledger service, no dependencies | `node demo.js` |
| D | `C:/Users/Q/code/bugfinding-skill-evaluation/scenario-d/` | React 19.3.1 SSR (`renderToString`) + `hydrateRoot`, node:test + jsdom 29.1.1 + RTL 16.3.3; `node_modules` installed | `npm test` |
| E | `C:/Users/Q/code/bugfinding-skill-evaluation/scenario-e/` | Node 22 `node:http` stock service, control (no planted defect) | `node demo.js` |

SHA256 (after calibration):

| File | SHA256 |
| --- | --- |
| scenario-c/package.json | 6242A09D2665B59E0638D16EBC7F06C63E9112967A3706F462C49102F6EE1D90 |
| scenario-c/contract.md | 3568ACCF7D1352E98DEB241083C17E8055C283C3CEDBE5F199B76457F8EDE083 |
| scenario-c/demo.js | 12E5901B3506334D759015E55504D2378DFE41BE8C6975A5939EAF7DE2DF2DE8 |
| scenario-c/src/server.js | 8C0E1576C56A55FDF645BC33DA023FAC666AA15B4C653CF89E2FF011E4E4B612 |
| scenario-c/src/store.js | 27C7B191A218CAF7FC1BDF536568E9D5616597EC942F463027A4679B1D44F776 |
| scenario-c/src/loader.js | F1EAEFBC3EB0D5D29CB483DFAD3E2A9FB2C5CE4C710671A3B1F75AE56AECA376 |
| scenario-d/package.json | 007FE24B1E56F19AA1E881B18EA664E806B57B60BC42D316CF8F2C8556A45DC5 |
| scenario-d/package-lock.json | 59C40A982ADF5C2B63C7848DD22B1B2918C92396E73862C61C14C19C35929DFA |
| scenario-d/contract.md | F5CC66A7A2CD09047A8307DC5D5F0423EDE5135D4B724CE49F774EB0FBF59171 |
| scenario-d/src/App.js | 54D9F087FA9C828BCC6F130FE4323A7A368236ADD810018A0DF6A4261C25F689 |
| scenario-d/src/tasks.js | D45B54DEE19D9EC02EAA1E25DFE740ED3F84126F856BA3459EF3B5021AF61B3E |
| scenario-d/src/server.js | F1EA3B0FC0C677854F77AA888C6BCB7511DE78C92552962F3D87B88198DDE827 |
| scenario-d/src/client.js | 95BBD05BA1E370A28F57C8B315A5D21A1D19B926168380B227442F0EBF78DF30 |
| scenario-d/test/setup-dom.js | 33D00004ACAACB81679E71156695E5ED32C72DF34A53C04F6E9761F9EC23376E |
| scenario-d/test/demo.test.js | CDA8AA0B56FFD8EED7031BF979EFACC5779AE6BACE648156777683B890077A8E |
| scenario-e/package.json | 62C4D8125072C2FF7D9CEA4C2251329722B717BD2CEA8CB13790C3C41F50408B |
| scenario-e/contract.md | 63B3F3401A32495883017C17F57863AE67281733963B1594D595654D758A9CED |
| scenario-e/demo.js | 9535C8976E62D658A7665361A51D90693ECFA5BC9351986F69154F8720667C30 |
| scenario-e/src/server.js | BB4C25C95E03C2E7C79F7A5C901F0488235AB479A9A96A60A4A84AC683A6EE46 |
| scenario-e/src/store.js | 6EAA06D42AF0977E6B8F259587A8D9FE8D8A61EFC257D720003F92840B294600 |
| scenario-e/src/keyed-lock.js | 42C576BBF2EEE974F9AF54F4AA9FF0419988CBDD55694830EFB80E72EC2325AB |
| scenario-e/src/price-cache.js | 94D76C0A0A2A79145F13E0200911EF26CB29999ED8BEE3FB502D27A171FC81B8 |

`scenario-d/node_modules/` (58 packages from the lockfile above) is not hashed file by file; the lockfile pins every resolved version and integrity.

## Private paths

Evaluators must not read these.

| File | SHA256 |
| --- | --- |
| `C:/Users/Q/code/bugfinding-skill-evaluation/private-evaluation-key-js.md` | 14BB2DBB96D5746FDE31BC255A1E4BD1055AC2F4210795B62C0D9E0CF5CBAE1F |
| `C:/Users/Q/code/bugfinding-skill-evaluation/fixture_selftest_js.mjs` | 8A933E5E31924E9C256B613209146B9CA54B98D5B8E8A48CEFA88B2090649C12 |

The key gives, per planted defect, location, trigger, observable and expected skill route, plus control evidence and known non-findings for E.

## Calibration output

Command (run from the workspace root): `node fixture_selftest_js.mjs`. Run 2 (after the fix): exit 0, wall 10406 ms, `# tests 19 / # pass 19 / # fail 0`, runner duration 9993 ms. Lines printed:

```text
C demo exit=0 ms=659
ok 1 - C healthy: public demo exits 0 with contract responses
ok 2 - C healthy: sequential HTTP deposits sum exactly
C(a) direct: responses 100, 200; final 200; contract requires 300
ok 3 - C defect (a): two concurrent deposits lose an update (direct API)
C(a) HTTP: 20 concurrent deposits of 1, all 200, final balance 1; contract requires 20
ok 4 - C defect (a): concurrent HTTP deposits lose updates
C(a) withdraw: fulfilled,fulfilled; final 0; 200 withdrawn from 100
C(a) create: fulfilled,fulfilled; contract allows exactly one
ok 5 - C defect (a) family: concurrent withdrawals and duplicate creates both succeed
C(b) n -> min ms of 3: 14:1.1(400) 16:1.3(400) 18:3.4(400) 20:10.8(400) 22:38.5(400)
C(b) valid 22-char id -> 404 in 14.2 ms
ok 6 - C defect (b): id pattern backtracking grows exponentially via request path
C(b) child server: unrelated GET alone 9.2 ms; during n=25 request 265.8 ms (n=25 request itself 298.7 ms, status 400)
ok 7 - C defect (b): one slow-path request stalls an unrelated client (server in a child process)
ok 8 - C healthy: loader shares fetches, caches, reports errors
C(c) outer=1 nestedSameKey=0 nestedOtherKey=1 fetches=2
D demo exit=0 ms=2888
ok 9 - C defect (c): load of the same key inside a load callback never calls back
ok 10 - D healthy: public demo test passes
ok 11 - D healthy: hydration with the same clock reports no error
D(a) server summary "3 open of 3 · as of 04:04 PM" client summary "3 open of 3 · as of 07:11 PM"
D(a) onRecoverableError calls: 1; first: Hydration failed because the server rendered text didn't match the client. As a result this tree will be regenerated on the client. This can happen if a SSR-ed Client Component used:
D(b) live window keydown listeners after each open/close: 1,2,3,4,5,6,7,8,9,10; after unmount: 11
D(c) after deleting "Charlie" under Open: Open shows ["Charlie"], All shows ["Alpha","Charlie"]; contract requires ["Alpha","Bravo"]
E demo exit=0 ms=398
ok 12 - D defect (a): hydration later in time reports a mismatch
ok 13 - D defect (b): each editor open/close leaves a window keydown listener
ok 14 - D healthy: delete under the All filter removes the named task
ok 15 - D defect (c): complete, filter Open, delete removes a different task
ok 16 - E control: public demo exits 0 with contract responses
E 50 concurrent reserves of 1 on 30: 30 x 200, 20 x 409, final 0
E mixed: +60 -20, final 40
ok 17 - E control: concurrent HTTP reserves and restocks keep exact counts
E sku size family n -> ms: 16:11.8(400) 64:1.7(400) 1024:0.7(400) 4096:0.8(400)
ok 18 - E control: long invalid sku paths are rejected quickly at every size
E nestedSameKey=1 nestedAfterError=1 fetches=3
ok 19 - E control: price cache nested, shared, cached and error paths
# tests 19
# pass 19
# fail 0
```

(Console lines from a test can print before that test's `ok` line; node:test buffers its TAP output.) Run 3, same command: exit 0, 19/19 pass; C(b) family 0.9, 1.3, 3.0, 9.9, 37.4 ms; unrelated GET 7.1 ms alone vs 266.8 ms during the n=25 request.

Other commands this task ran: `node demo.js` in scenario-c (exit 0), `npm install --no-audit --no-fund` in scenario-d (exit 0, 58 packages), `npm test` in scenario-d (exit 0, 3/3), `node demo.js` in scenario-e (exit 0), one inline node probe of the regex timing, and `npm view` lookups.

## Limits

- Calibration shows each planted defect is reachable and observable and the control meets its contract on the checks written. It does not show that any skill finds them, and it is not proof that E has no defect: E is "no planted defect", checked by 4 control tests, not verified bug-free.
- Timing checks (C(b), E size family) are wall-clock on this machine; the assertions use ratios and wide margins (t22 > 4 x t18 and > 15 ms; stall > 50 ms and > 5x baseline). Two passing runs, not a flakiness study.
- D(a) needs a clock or locale difference between render and hydrate; jsdom in one process shares the locale, so calibration uses a shifted `Date`. The public demo's hydration test can itself hit D(a) if server render and hydration straddle a minute boundary (a window of a few ms per minute).
- D runs in jsdom, not a browser; React's development build is used (NODE_ENV unset).
- C(a) also appears in `createAccount` (duplicate creates) and `withdraw`; the key scores them as one defect family. C(c) is a library-API defect, not reachable through the HTTP service.
- Per-evaluation CPU: demos under 3 s each; the full self-test about 10 s wall. A C(b) probe beyond n about 28 costs seconds per request because growth is about 2x per character; the contract's 64-character limit is checked after the pattern, so evaluators control that cost themselves.
- scenario-d pins jsdom 29.1.1, not the latest 31.0.0, because jsdom 30+ declares `node ^22.22.2` and the installed Node is 22.18.0.
- No network use except `npm view` and `npm install` for scenario-d. No commit or push. Scenarios a and b and their key were not read or modified.
