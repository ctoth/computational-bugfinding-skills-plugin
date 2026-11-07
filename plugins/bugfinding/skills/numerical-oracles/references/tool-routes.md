# Tool routes and applicability

These are conditional routes for an existing suitable environment. They authorize no installation, target execution or rewrite.

## MPFR: explicit reference arithmetic

Use the versioned 4.2.2 manual's §2 header/library version probe before trusting a binding; its documented C link command is `cc -o version version.c -lmpfr -lgmp`. MPFR "is based on the GNU MP library" and links with `-lmpfr -lgmp`; this version is released under the "GNU Lesser General Public License, version 3 or any later version". Follow the semantic limitations in [contracts and references](contracts-and-references.md), including input conversion, subnormals and reference uncertainty ([MPFR §§1–2,4–5](https://www.mpfr.org/mpfr-4.2.2/mpfr.html)). No Go, JavaScript or Python binding was verified here; inspect a selected binding's actual conversions and flags before use.

## Herbie: candidate expressions and numerical regimes

The inspected source README requires Racket "(8.0 or later)" and Rust "(1.87.0 or later)" for a source build ([Herbie README, Installing from Source](https://raw.githubusercontent.com/herbie-fp/herbie/d493bef58667fcb62652fc3e6c2fd67527ff0f76/README.md)); Herbie uses the [MIT license](https://raw.githubusercontent.com/herbie-fp/herbie/d493bef58667fcb62652fc3e6c2fd67527ff0f76/LICENSE.md). These are source-build facts, not a check of the installed package or permission to install it.

The pinned input documentation provides FPCore `:pre`, `:precision` and optional `:spec`; match the selected platform's operations to the actual producer ([input format](https://raw.githubusercontent.com/herbie-fp/herbie/d493bef58667fcb62652fc3e6c2fd67527ff0f76/www/doc/2.4/input.html)). After checking an existing installation's subcommand help against the pinned options, a bounded report shape is:

```text
racket -l herbie report --seed 1 --timeout 60 in.fpcore out/
```

"Options must go before subcommand arguments" such as input and output paths; the timeout is "per-input, in seconds", and the seed "changes the randomly-selected points". Thus cap the input set too. Preserve reports, warnings, `--platform` and seed: two runs "with the same seed should produce identical results" ([Herbie options, General options](https://raw.githubusercontent.com/herbie-fp/herbie/d493bef58667fcb62652fc3e6c2fd67527ff0f76/www/doc/2.4/options.html)). The pin identifies the inspected source, not an assertion that it is a 2.4 release or compatible with the installed runtime.

Interpret the report's average "across many randomly-sampled valid inputs" as search evidence. It is not a worst-case, signed-zero or full exceptional-value guarantee; validate candidate rewrites independently against the product promise ([error metric](https://raw.githubusercontent.com/herbie-fp/herbie/d493bef58667fcb62652fc3e6c2fd67527ff0f76/www/doc/2.4/error.html)). Do not automatically replace a specified rounded graph with a more accurate real-arithmetic equivalent.

## FPGen: historical technique with artifact constraints

The inspected artifact is [BSD-3-Clause licensed](https://raw.githubusercontent.com/ucd-plse/FPGen/5e0102e587eab4c22d5ef4d0cee03d80a5875a72/LICENSE).

Use the paper for error-directed search ideas. Its artifact README targets an Ubuntu 14.04.5 LTS experimental setup and describes hardware-dependent reproduction: "Running the artifact on a different machine could possibly diverge the execution". No current generic Go/Windows integration was verified ([README](https://raw.githubusercontent.com/ucd-plse/FPGen/5e0102e587eab4c22d5ef4d0cee03d80a5875a72/README.md)). Porting it is separate work, not an assumed backend.

The comparison script hardcodes `rootpath=/home/fptesting/FPTesting` and mutates working-directory files (`rel-errors`, `test_input`, `best_input`, `out-*`, then `rm -f out-* test_input`) ([compute_error.sh lines 3, 16–39](https://raw.githubusercontent.com/ucd-plse/FPGen/5e0102e587eab4c22d5ef4d0cee03d80a5875a72/scripts/compute_error.sh)). Its printer clamps relative-error denominators with `FLT_MIN`, converts reported values to double and updates maxima through ordered comparisons ([print_error.c lines 64–80](https://raw.githubusercontent.com/ucd-plse/FPGen/5e0102e587eab4c22d5ef4d0cee03d80a5875a72/utils/print_error.c)). These are bounded limitations of the inspected artifact, not newly reproduced product findings. Do not adopt that printer unchanged as the final numerical oracle.
