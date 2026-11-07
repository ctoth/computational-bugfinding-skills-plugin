# Research: constraint solvers for UI design and layout

## Question

Q (2026-11-07): "probably there's research/literature about attaching z3 constraint solvers to UI design ... finding the closest formalism is gonna be important."

What does the literature say about using constraint solvers (SMT such as Z3, linear-constraint solvers, etc.) to specify, synthesize, verify or test user-interface design and layout, and how did those papers choose or build the formalism they map the UI domain onto?

## Search log

Collection check: `C:/Users/Q/code/papers/` holds one paper (Kingsbury 2020, Elle); index.md has no layout, CSS, GUI, constraint or SMT entries. No duplicates.

1. WebSearch "SMT solver Z3 GUI layout verification repair paper" — candidates: ORC Layout (Jiang et al., arXiv 1912.07827, Z3 with OR-constraints); VizAssert, "Verifying That Web Pages Have Accessible Layout" (Panchekha et al., PLDI 2018); "Automated Repair of Layout Bugs in Web Pages with Linear Programming" (Jacquet, Chamberland-Thibeault, Hallé, UQAC); a reference-nets-to-SMT UI model paper (unnamed in result).
2. WebSearch "Cassowary linear arithmetic constraint solving algorithm user interface Badros Borning Stuckey" — candidates: Badros, Borning, Stuckey, "The Cassowary Linear Arithmetic Constraint Solving Algorithm", TOCHI 2001; Borning, Marriott, Stuckey, Xiao, UIST 1997 (Cassowary + QOCA); Constraint Cascading Style Sheets (Badros, Borning et al.).
3. WebSearch "Cassius formal semantics CSS layout SMT verification Panchekha Torlak" — candidates: Panchekha & Torlak, "Automated Reasoning for Web Page Layout", OOPSLA 2016 (Cassius); Panchekha PhD thesis 2019.
4. WebSearch "constraint-based user interface layout synthesis SMT designer exploration Scout Swearngin" — candidates: Swearngin, Wang, Oleson, Fogarty, Ko, "Scout: Rapid Exploration of Interface Layout Alternatives through High-Level Design Constraints", CHI 2020 (arXiv 2001.05424); Hosobe, "Solving Hierarchical Soft Constraints with an SMT Solver".
5. WebSearch "Auto Layout constraints iOS ambiguity verification SMT solver bugs paper" — no research paper on Auto Layout verification surfaced; Apple's Auto Layout guide (ambiguous layouts) and an unrelated OOPSLA 2023 layout-sensitive-grammar paper.

Selection (by relevance to "solver attached to UI design" and to "how was the formalism chosen"): Cassowary (TOCHI 2001, foundational linear-constraint formalism behind Auto Layout); Cassius (OOPSLA 2016, CSS semantics reduced to QF linear real arithmetic); VizAssert (PLDI 2018, SMT verification of layout properties); ORC Layout (Z3, disjunctive layout constraints); Scout (CHI 2020, design-level constraints compiled to a solver). Jacquet et al. MILP repair held as a sixth if time allows.

Retrieval:
- ORC Layout: arXiv 1912.07827 via fetch_paper.py -> `C:/Users/Q/code/papers/Jiang_2019_ORCLayoutAdaptiveGUI/` (12 pp).
- Scout: arXiv 2001.05424 via fetch_paper.py -> `C:/Users/Q/code/papers/Swearngin_2020_ScoutRapidExplorationInterface/` (13 pp).
- Cassowary: Semantic Scholar returned HTTP 429; open copy downloaded from constraints.cs.washington.edu/solvers/cassowary-tochi.pdf -> `C:/Users/Q/code/papers/Badros_2001_CassowaryLinearArithmeticConstraint/` (39 pp).
- VizAssert: open copy from homes.cs.washington.edu/~mernst/pubs/verify-layout-pldi2018.pdf -> `C:/Users/Q/code/papers/Panchekha_2018_VerifyingWebPagesAccessibleLayout/` (14 pp).
- Cassius (OOPSLA 2016): NOT retrieved. Semantic Scholar 429; sci-hub.st returns a DDoS-Guard JS challenge to curl; ACM DL, author-site guesses and dblp failed or 404/blocked. Replaced in the read set by Jacquet et al.
- Jacquet et al. MILP repair: open copy from constellation.uqac.ca/id/eprint/7747/1/paper.pdf -> `C:/Users/Q/code/papers/Jacquet_AutomatedRepairLayoutBugsLinearProgramming/` (15 pp).

## Papers read

Paper-reader steps I did not complete as written:

- `citations.md` has the full reference list only for Jacquet. For the other four, the file points to the PDF pages and lists the key citations.
- The reconcile step (step 7) was not run.
- The Jacquet directory name has no year, because the paper does not print one.

All five were read in full from their page images, following the paper-reader procedure. Notes are in each paper's directory.

1. Panchekha, Geller, Ernst, Tatlock, Kamil. "Verifying That Web Pages Have Accessible Layout." PLDI 2018. 14 pages. This copy does not include Appendices A-C. Notes: `C:/Users/Q/code/papers/Panchekha_2018_VerifyingWebPagesAccessibleLayout/notes.md`.
2. Badros, Borning, Stuckey. "The Cassowary Linear Arithmetic Constraint Solving Algorithm." ACM TOCHI, author preprint. 39 pages, including the electronic appendix. Notes: `C:/Users/Q/code/papers/Badros_2001_CassowaryLinearArithmeticConstraint/notes.md`.
3. Jiang, Du, Lutteroth, Stuerzlinger. "ORC Layout: Adaptive GUI Layout with OR-Constraints." CHI 2019. 12 pages. Notes: `C:/Users/Q/code/papers/Jiang_2019_ORCLayoutAdaptiveGUI/notes.md`.
4. Swearngin, Wang, Oleson, Fogarty, Ko. "Scout: Rapid Exploration of Interface Layout Alternatives through High-Level Design Constraints." CHI 2020. 13 pages. The supplementary materials were not read. Notes: `C:/Users/Q/code/papers/Swearngin_2020_ScoutRapidExplorationInterface/notes.md`.
5. Jacquet, Chamberland-Thibeault, Hallé. "Automated Repair of Layout Bugs in Web Pages with Linear Programming." 15 pages; venue and year are not printed. Notes: `C:/Users/Q/code/papers/Jacquet_AutomatedRepairLayoutBugsLinearProgramming/notes.md`.

## Findings

### F1. VizAssert (Panchekha et al., PLDI 2018)

- UI concern: whether accessibility/usability guidelines hold on every rendering of a web page across screen sizes and font sizes (p.1). Checked over widths 1024-1920 px, heights 800-1080 px, default font 16-32 px (p.9).
- Formalism/solver: two formal pieces. (a) The property language, "visual logic": universally quantified formulas over the tree of boxes, with linear real arithmetic (multiplying only by constants), box-tree navigation, and an `ancestor` function in place of recursion (Fig 3, p.4). (b) A formalization of the CSS 2.1 rendering algorithm. Both are encoded to quantifier-free linear real arithmetic (QFLRA) and solved with Z3 (pp.2, 4).
- How the formalism was chosen: by the solver's decidable fragment. The authors state each language restriction as a solver limit: linear only, because SMT solvers efficiently handle only linear real arithmetic; universal only, because that maps to quantifier-free queries; no recursion, hence `ancestor` (p.4). They add: "We did not find any assertions that we were unable to formalize due to these limitations" (p.4). The rendering side is a formalization of the existing standard (W3C CSS 2.1), not a new model (pp.2-3). Where the standard's own description does not fit QFLRA, they write "finitization reductions": arbitrary-size sets and graph reachability become fixed-size summaries (pp.5-8):
  - line height becomes running maxima (p.6);
  - margin collapsing becomes six reals and a boolean per box (p.6);
  - floats become a bounded "exclusion zone" with a canonical form (Theorem 4.1, p.8).
- Encoded vs left out:
  - Encoded: 13 CSS subsystems (Fig 2, p.3).
  - Selector matching and cascading are computed outside the solver, because the CSS file is known when verifying. The authors give this as the difference from Cassius, which was built for synthesis and so had to put selectors inside the solver (p.11).
  - Left out: vertical alignment, right-to-left text, SVG, tables (tables named as a research challenge), JavaScript, server-side code (p.11). The 62 test pages were chosen as those that fit the supported CSS subset (p.9).
- What the solver guarantees: "verified" means no rendering parameters in the bounded set violate the assertion; otherwise it returns a counterexample with concrete box set, window size and font size (p.2). Soundness of the float reduction is checked on every run: the SMT solver proves, by induction, that the encoding meets the standard's nine float rules for the current bound k. If that proof fails, the tool stops. If the bound k is hit, it reruns with larger k (p.8).
- How the formalization itself was validated: against W3C conformance tests for the relevant CSS sections. VizAssert supports 915 of 1006 tests, Cassius 271. Neither fails any test it supports. Renderings are compared with Firefox to 1/6 pixel (pp.10-11, Table 3).
- Results: 62 pages, 502 page/assertion pairs. The text reports 64 true positives, 13 false positives and 11 timeouts at 30 minutes (p.9). Table 2 totals are 65 true positives and 388 verified, against "414 successful verifications" in the text; the table and the text disagree (p.9).
- Limits stated by the authors:
  - A false positive comes from the gap between the formal assertion and the guideline: text boxes reserve space for descenders, so "SALE" is flagged as possibly overlapping. "VizAssert thus detected a failure of the formal assertion, but not a failure of the accessibility guideline" (p.10).
  - SMT instances run to roughly 0.5-1M terms (Fig 10, p.10).
  - CSS is "dozens of standards totaling thousands of printed pages" (p.11).

### F2. Cassowary (Badros, Borning, Stuckey, ACM TOCHI 2001; author preprint, 39 pp incl. electronic appendix)

- UI concern: interactive layout, where the solver works out positions as the user drags objects or windows. Example uses: a window manager (SCWM), constraint-extended CSS (CCSS) and SVG, and drawing editors (pp.2-3, 28-29).
- Formalism/solver:
  - Constraints are linear equalities and non-strict inequalities over the reals.
  - They are organised as a constraint hierarchy: "required" must hold, and the other strength levels (strong, medium, weak) each completely dominate the levels below (pp.3-4).
  - Among solutions that satisfy the required constraints, the solver returns a "weighted-sum-better" one: errors are summed per strength level and the sums are compared lexicographically (pp.4-5).
  - The algorithm is incremental simplex plus dual simplex over an augmented simplex form (pp.7-19).
- How the formalism was chosen, as the authors argue it:
  - Linear inequalities are what UI relations are: "inside", "above", "left-of" (p.1).
  - Preferences are needed for three reasons: stability, graceful handling of invalid input, and balancing conflicting goals (p.2).
  - Cycles are unavoidable in declarative specifications, and making programmers avoid them is "contrary to the spirit of the whole enterprise". Earlier solvers that handled only one-way, acyclic, or equality-only constraints were therefore rejected (pp.3, 6).
  - Real-number weights such as "strong = 1000 × weak" were rejected because large variable values could let weak constraints win. Symbolic lexicographic weights were used instead (p.13). The appendix says the C++ and Java implementations fall back to real-number approximations anyway, a step it calls a "kludge" (App-7).
  - Strict inequalities were excluded, because {required x>0, weak x=0} has no best solution (p.24).
  - Least-squares comparison was avoided, because simplex needs a linear or quasi-linear objective (p.6).
- Encoded vs left out:
  - Encoded: linear geometry plus strength levels.
  - Left out: anything nonlinear, which raises an exception (App-5). A benchmark that originally multiplied by a scale factor was changed to an added offset for this reason (p.27). Also left out: disjunction (unknown in the text; no construct for it appears in the paper) and strict inequality.
- What the solver guarantees or checks:
  - It finds one weighted-sum-better solution; "any one of these will be a correct answer" (p.4).
  - Unsatisfiable required constraints raise an exception (pp.20, 22).
  - It does not verify properties across a range of inputs. It solves one concrete instance at a time.
- Limits stated by the authors:
  - An order of magnitude slower than local propagation (DeltaBlue) when re-solving. Chain of 1000: 5.9 ms vs 0.4 ms (pp.27-28).
  - Numerical problems may accumulate, so `reset()` is provided (App-3).
  - Fixing x and y stays on the same point needed the `addPointStays` "kludge" (App-2-3).
  - Interaction stays satisfactory at about 1000 constraints (p.28).

### F3. ORC Layout (Jiang, Du, Lutteroth, Stuerzlinger, CHI 2019)

- UI concern: one layout specification that adapts across screen sizes and orientations, combining grid and flow layout (pp.1-2).
- Formalism/solver:
  - Starts from standard soft/hard linear layout constraints, where weights rank the soft constraints and a hard constraint counts as infinite weight (p.3).
  - Adds OR-constraints: the whole clause is hard and each disjunct is soft, which "ensures layout specifications are always feasible" (pp.4-5).
  - Conditionals are encoded as "NOT(A) OR B" (p.8). Encodings also use sums and max, e.g. b.width = max_i i.width (p.6).
  - Solved with Z3 using weighted soft constraints (default WMax optimization) (pp.5, 8).
- How the formalism was chosen:
  - The authors argue that linear constraint systems "have a well-understood mathematical basis" and that most layout models reduce to them, with flow layout the exception (p.3).
  - LP/QP layout solvers "support only conjunctions of constraints (AND), but do not permit disjunctions (OR)" (p.3).
  - From this: "OR-constrained systems are a subset of SMT ... problems. Instead of an explicit solver algorithm, we thus use Z3", and "One of the key insights of our work is that SMT solvers can be used to solve GUI layouts with OR-constraints" (p.5).
  - The authors say Z3 "has not been used for general GUI/widget layout with OR-constraints before" (p.3).
  - The choice rests on expressiveness (disjunction), not on verification.
- Encoded vs left out:
  - Encoded as reusable patterns: positions and sizes, min/pref/max sizes, flow, cross-cutting, connected, balanced flow, alternative positions, alternative widgets, optional widgets, and flow around a fixed area (pp.5-8).
  - Left out: "usability, layout, and aesthetic design principles are not directly supported" (p.11).
- What the solver guarantees or checks:
  - It finds a layout that satisfies as many weighted constraints as possible (p.5). "We have not experienced Z3 convergence failures" (p.5).
  - The editor keeps the specification solvable by detecting, highlighting and disabling conflicting constraints (p.5).
  - The authors note that layout specifications may contain errors that only show at particular GUI sizes (pp.2-3). The paper offers no check across sizes; it solves for the current size.
- Evaluation:
  - Timing: 20 widgets / 175 constraints take 0.28-0.61 s per edit; 30 widgets / 265 constraints take up to 1.82 s (Table 1, p.10). "ORC solving does not yet work at real-time interactive speeds" (p.9).
  - Qualitative expert review with 9 participants (pp.9-10).
- Limits stated by the authors:
  - Z3's generality "likely" adds overhead, and they call for specialized algorithms (p.11).
  - Complex layouts may need a hierarchy (p.11).
  - Resize usually forces a full rebuild of the constraint system (p.9).

### F4. Scout (Swearngin, Wang, Oleson, Fogarty, Ko, CHI 2020)

- UI concern: helping designers generate many diverse mobile layout alternatives from a few high-level design constraints (p.1).
- Formalism/solver: two levels.
  - High-level constraints a designer can state: group, order, emphasis, repeat group, alternate group, and Keep/Prevent feedback (pp.2-3). Each is tied to a cited design principle, for example the Gestalt and structure principles for grouping, task order for ordering, and a focal point for emphasis (p.2).
  - These are compiled into low-level spatial constraints over variables with finite, curated domains: canvas, group and element variables, including layout grid, baseline grid, arrangement, alignment, padding, and size triples (pp.5-6). The domains are "curated from design guidelines [2] and layout design literature [3]" (p.5).
  - A randomized branch-and-bound search assigns the variables, and Z3 checks each partial assignment for validity (pp.3-4).
  - Every layout gets three "basic design quality" constraints: stay-in-bounds, pairwise non-overlap, and minimum size, e.g. a 48×48 px touch target (p.5).
- How the formalism was bent by the solver:
  - Sizes are precomputed (width, height, factor) triples on a 4 px grid, because "Z3 does not efficiently compute multiplication constraints (i.e., otherwise needed for maintaining an aspect ratio)" (p.5).
  - Diversity comes from randomizing the variable and value order and adding a blocking constraint after each layout (p.4).
  - Quality ranking (size, balance, alignment, density) is computed outside the solver, adapted from published complexity metrics [40] (p.4).
  - Against ML generators, the authors argue that constraint solving "gives it direct control over the attributes of layouts that the generation algorithms explore" and needs no dataset (p.10).
- What the solver checks:
  - Validity of each layout against the design constraints and feedback (p.5).
  - Z3's `unsat core` names the smallest conflicting set of clauses. Scout uses it to highlight conflicting designer feedback and to repair layouts by removing the conflicting assignments (p.5).
  - Nothing is checked beyond the generated instances.
- Evaluation:
  - 18 designers; layouts were 12% more spatially diverse within a designer (p<0.027) (p.8).
  - Expert-rated quality was slightly lower (5.37 vs 5.73), not significant (p.8).
  - Typical output: 15 layouts of 9 elements in under 5 s using 20 solver threads (p.4).
- Limits stated by the authors:
  - Scaling to larger interfaces such as web pages needs future work (pp.4, 10).
  - Designers found the outputs less "clean": "You'd have to put a lot of rules on it to get it as clean as you'd want it to be" (p.9).
  - The full constraint equations are in supplementary materials, which I have not read (p.5).

### F5. Jacquet, Chamberland-Thibeault, Hallé, "Automated Repair of Layout Bugs in Web Pages with Linear Programming" (UQAC author copy; venue and year not printed; references run to 2020)

- UI concern: repairing a rendered page on the fly when it violates declared layout constraints, i.e. overlapping, misaligned or protruding elements (pp.1-3). Their bug classes follow Walsh et al. and the Lelli et al. GUI fault category GSA1 (p.2).
- Formalism/solver: Mixed Integer Linear Programming solved with IBM CPLEX (pp.2, 11).
  - The page is modelled as nested rectangles (x, y, w, h), one per DOM element down to text leaves (p.6).
  - Constraints are given as hand-written triples (i, j, t), where t is vertical alignment, horizontal alignment, disjointness or inclusion (p.10).
  - Alignment is one linear equality. Inclusion is four inequalities (p.7).
  - Disjointness says at least one of four inequalities must hold. The authors write that linear solvers "typically cannot directly handle the fact that it suffices that one of the constraints must be fulfilled", so they encode it with big-M binary choice variables: four constraints plus three binaries (p.7).
  - Sizes may not decrease, because otherwise the solver could shrink boxes to zero (p.7).
  - The objective minimises total change from the observed layout: Σ|Δx|+|Δy|+Δw+Δh (p.8).
- How the formalism was chosen:
  - Constraint violations are "intrinsically numerical", and generic generate-and-test repair "does not exploit the geometric nature of the problem" (p.5).
  - An off-the-shelf numerical solver avoids re-rendering each candidate fix, unlike X-Fix (pp.5-6, 10).
  - MILP specifically, because disjunction (disjointness) needs integer choice variables (p.7).
- What the solver checks: it returns a layout that satisfies the given constraints with minimal change, if one exists (p.8). It says nothing about other viewports. The authors also note that resizing after the hotfix can break the layout again (p.14).
- Evaluation:
  - Real-world pages were checked by eye (Moodle, AgentSolo). The number of real pages is not stated in the paper (pp.11-12).
  - 100 synthetic pages of 2-10450 elements were solved within a 2 s budget; most took under 1 s and a few timed out (pp.12-13).
  - Their "zone of influence" cuts thousands of DOM nodes down to a few dozen (pp.9, 13).
- Limits stated by the authors:
  - The constraints must be supplied and must be *complete*. "The human eye makes many implicit assumptions" that have to be written out. Example: the fix enlarged the red menu but not its white parent (p.14).
  - Absolute positioning changes the page's structure (p.14).
  - The zone of influence only works if no element shrinks (p.14).
  - Only three constraint types are supported, and testing was on Chrome only (p.14).
- A claim in this paper conflicts with a paper I read. It says Cassowary's formulation "initially did not contain an objective function" (p.5). The Cassowary TOCHI paper defines a weighted-sum objective over constraint errors (Cassowary pp.13-14).

## Bridge case studies (reframe, team lead 2026-11-07)

Q's framing, as relayed: "we have a fuzzy world, then we have formalisms. we are building one possible bridge, which will tell us how to build bridges." Each paper read is treated below as one bridge from fuzzy UI design intent to a formalism. Everything here comes from the same page images already read; page numbers refer to each paper's own pages. I did no new reading for this section.

### B1. VizAssert (Panchekha et al., PLDI 2018)

1. **Fuzzy notion.** English-language accessibility and usability guidelines, for example "Headings form a visual hierarchy" and "Text has sufficient contrast" (Table 1, p.2). The authors say these were "not expressed in a formal language" (p.1).
2. **Formalism and why.** Two formal pieces:
   - Visual logic for the guideline. Its stated restrictions follow the solver: linear arithmetic only because "SMT solvers can only efficiently reason about *linear* real arithmetic"; universal quantification only because these "correspond to quantifier-free queries"; `ancestor` in place of recursion (p.4).
   - The W3C CSS 2.1 rendering algorithm for the page (p.2).
   - Both are encoded to QFLRA and solved with Z3. Where the standard's own description uses arbitrary-size sets, they add "finitization reductions" (p.2, pp.5-8).
   - How fuzzy concepts were made concrete is shown openly. Two named challenges: "precisely identifying the page elements discussed by the guideline and translating high-level design concepts to concrete visual properties" (p.5). Their example: "visual_importance(b) := b.height" (p.5).
3. **What the encoding observes and loses.**
   - Observes box geometry, colours and box types from a formalised rendering, across a bounded set of window and font sizes (pp.4, 9).
   - Blind spots the authors state:
     - letter shapes, which caused a false positive: "a failure of the formal assertion, but not a failure of the accessibility guideline" (p.10);
     - unsupported CSS (vertical alignment, right-to-left text, SVG, tables) (p.11);
     - JavaScript and server-side generation (p.11);
     - rendering parameters outside the chosen bounds (p.9).
   - The test pages were filtered to those the tool supports (p.9).
4. **How verdicts reach the designer, and what they may claim.**
   - "verified" means the assertion "provably holds for all considered rendering parameters". "violated" comes with a counterexample: the boxes involved plus the window and font size. "The developer can examine the counterexample in a browser to confirm the error and then modify the page" (p.2).
   - The formalism itself is checked: against W3C conformance tests compared to Firefox (pp.10-11), and by a solver-proved check of the float encoding on every run, which stops the tool if it fails (p.8).
   - So the claim is limited to the formal assertion, the supported CSS subset, and the parameter bounds. The authors measured how often the formal verdict and the guideline disagree: 13 false positives, 17% of counterexamples (Table 2, p.9).

### B2. Cassowary (Badros, Borning, Stuckey, TOCHI 2001)

1. **Fuzzy notion.** What a designer wants from a layout: "requiring that one window be to the left of another, ... or preferring that an object be contained within a rectangle if possible" (p.1). Also wanted: stability ("things should stay where they were unless there is some reason for them to move"), graceful handling of invalid input, and balancing conflicting desires (p.2).
2. **Formalism and why.**
   - Linear equalities and inequalities form a constraint hierarchy: required constraints plus strengths, compared by "weighted-sum-better" (pp.3-5).
   - Justifications given:
     - inequalities express "inside", "above", "left-of" (p.1);
     - preferences are needed for the three reasons above (p.2);
     - cycles come naturally in declarative specifications, so a solver must handle them (p.3).
   - Restrictions are justified by keeping a well-defined answer. Strict inequalities are excluded because a hierarchy can then have "no solution ... even though the required constraints could be satisfied" (p.24). Symbolic weights stop weak constraints from beating strong ones when values are large (p.13).
3. **What the encoding observes and loses.**
   - Observes linear relations between variables.
   - Loses:
     - nonlinear relations, which raise an exception (App-5);
     - the difference between equally good solutions: "any one of these will be a correct answer" (p.4);
     - which of x/y stays belong to the same point, needing the `addPointStays` "kludge" (App-2-3).
   - The C++ and Java implementations replace symbolic weights with real-number approximations (App-7). This brings back the risk the symbolic weights were meant to remove (p.13); that connection is my inference from those two pages.
4. **How verdicts reach the designer, and what they may claim.**
   - The answer is the new positions, applied straight to the screen during a drag (pp.2, 14-19).
   - In SCWM, a "constraint investigator" shows the active constraints (p.3).
   - If the required constraints cannot be satisfied, it throws an "unsatisfiable constraints" exception (p.22).
   - The claim is only "a weighted-sum-better solution of the stated constraints". Nothing is claimed about whether the constraints capture what the designer meant.

### B3. ORC Layout (Jiang et al., CHI 2019)

1. **Fuzzy notion.** "Flexible layouts that work across different screen sizes and orientations" from a single specification (p.1). Also a "consistent appearance" across sub-layouts (p.6).
2. **Formalism and why.**
   - Soft/hard linear constraints plus OR-constraints, solved by Z3 (pp.4-5).
   - Justification: LP/QP layout solvers "cannot express alternatives, as they support only conjunctions" (p.3); "OR-constrained systems are a subset of SMT ... problems. Instead of an explicit solver algorithm, we thus use Z3" (p.5).
   - Designers work with parameterised pattern templates, and "the editor automatically creates and maintains the corresponding constraints" (p.5). The fuzzy-to-formal step is packaged as reusable patterns (pp.5-8).
   - They build the OR-clause so that the whole clause is hard and each part soft, which "ensures layout specifications are always feasible" (pp.4-5).
3. **What the encoding observes and loses.**
   - Observes widget positions, sizes, and min/preferred/max sizes.
   - Lost by the authors' own statement: "usability, layout, and aesthetic design principles are not directly supported" (p.11).
   - The authors also note that errors can stay "hidden" in a specification "and only show in some cases, e.g., for a particularly small screen" (p.2). The paper offers no check for this.
4. **How verdicts reach the designer, and what they may claim.**
   - The solved layout is shown on the canvas.
   - The editor "keeps the layout solvable by detecting, highlighting, and disabling conflicting constraints" (p.5).
   - Evidence that the bridge serves designers is a qualitative review with 9 experts (pp.9-10).
   - The claim is "a layout that satisfies as many weighted constraints as possible" (p.5). Nothing is claimed across sizes.

### B4. Scout (Swearngin et al., CHI 2020)

1. **Fuzzy notion.** Design principles from the literature: clear hierarchy, structure and Gestalt grouping, task order, emphasis as a focal point (p.2). Also the study's targets "clean" and "compelling" (p.7).
2. **Formalism and why.**
   - High-level constraints compile to low-level spatial constraints over variable domains "curated from design guidelines [2] and layout design literature [3]". Z3 checks each partial assignment inside a randomized search (pp.3-5).
   - Why constraints rather than machine learning: "direct control over the attributes of layouts that the generation algorithms explore", and no dataset is needed (p.10).
   - Why high-level constraints: low-level constraints such as Auto Layout's "can be confusing and difficult for designers" (p.1).
   - Solver limits shaped the encoding: sizes are precomputed triples because "Z3 does not efficiently compute multiplication constraints" (p.5).
   - The fuzzy goal "quality" is not encoded as constraints. It is a ranking function computed outside the solver, adapted from published metrics [40] (p.4).
3. **What the encoding observes and loses.**
   - Observes element positions and sizes, grid, grouping, order and emphasis relations.
   - Blind spots stated or shown:
     - Expert-rated quality was lower on balance, emphasis and alignment, though not significantly (p.8).
     - Designers found the outputs less clean: "You'd have to put a lot of rules on it to get it as clean as you'd want it to be" (p.9).
     - The study excluded non-spatial features such as colour and font type (p.7).
     - It works for mobile-sized interfaces; scaling is future work (pp.4, 10).
4. **How verdicts reach the designer, and what they may claim.**
   - Valid layouts appear ranked in the Layout Ideas panel. Invalid ones get red diagonal stripes.
   - Z3's `unsat core`, "the smallest set of constraint clauses that cannot be satisfied", is mapped back to the designer's own Keep/Prevent annotations and highlighted on hover (pp.3, 5). Conflicts are reported in the designer's terms, not the solver's.
   - Layouts are exported as editable SVG for the designer to refine in their own tool (p.3).
   - Verdicts claim only validity against the stated constraints. Quality is a ranking, and the study measured it separately with expert raters (p.8).

### B5. Jacquet, Chamberland-Thibeault, Hallé (layout repair, MILP)

1. **Fuzzy notion.** "Layout bugs": elements that "overlap, become misaligned or protrude ... for fortuitous reasons" (p.1). Ultimately, what "the human eye" expects (p.14).
2. **Formalism and why.**
   - A MILP over box geometry with hand-written pairwise constraints: alignment, inclusion, and disjointness via big-M binaries. The objective minimises change (pp.6-8).
   - Justifications:
     - violations of layout constraints are "intrinsically numerical", and generic repair "does not exploit the geometric nature of the problem" (p.5);
     - an external solver avoids re-rendering each candidate fix (pp.6, 10);
     - integer variables are used because linear solvers "typically cannot directly handle the fact that it suffices that one of the constraints must be fulfilled" (p.7).
   - The objective stands in for an intent that is never stated: without it, "a valid solution could be to move all elements", against "the intuition that the expected correction would simply move the single misaligned element" (p.8).
3. **What the encoding observes and loses.**
   - Observes rendered rectangles (x, y, w, h) from the browser (p.10).
   - Loses everything the eye assumes but nobody wrote down. The constraints must be "complete ... It turns out that the human eye makes many implicit assumptions over the expected size, position and alignment of elements which, in our approach, must be explicitly provided". Example: the white parent was not enlarged (p.14).
   - Also lost: element shrinking (excluded by design), resizing after the fix, and normal document flow, because the fix uses absolute positioning (pp.7, 14).
4. **How verdicts reach the designer, and what they may claim.**
   - The solution is injected into the page as a JavaScript "hotfix" (pp.10-11).
   - Real-world results were "visually inspected" by the authors (p.11). A human eye remains the final judge.
   - The claim is a minimal-change layout that satisfies the given constraints in the current viewport, on Chrome only (pp.8, 14).

## Synthesis: what this domain teaches about building bridges (restricted to the five papers read)

1. **Every bridge has a named, hand-made concretisation step, and that step is where the papers report their errors.**
   - VizAssert has to turn "visual importance" into "b.height" (p.5).
   - Jacquet has to write "obvious" conditions by hand and proposes heuristics to infer them (p.14).
   - Scout curates its domains from guideline literature (p.5).
   - The observed verdict-vs-intent gaps all sit here: VizAssert's descender false positives (p.10); Jacquet's unenlarged parent (p.14); Scout's "less clean" output (p.9).
2. **The formalism is chosen at the intersection of what the intent needs and what the solver can decide efficiently, and the papers state both sides.**
   - Need-driven moves: preferences and cycles in Cassowary (pp.2-3); disjunction in ORC (p.3, 5) and Jacquet (p.7).
   - Solver-driven restrictions: linear, universal, non-recursive in VizAssert (p.4); no multiplication in Scout (p.5); no strict inequalities or nonlinearity in Cassowary (p.24, App-5).
   - None of the five uses a more expressive formalism than its intent needed.
3. **Where an external standard exists, using it as the formal source gives an independent oracle for the bridge itself.** Only VizAssert has this. CSS 2.1 is the specification, the W3C conformance suite checks the formalisation (pp.10-11), and the solver re-proves the float encoding against the standard's rules on every run (p.8). The other four bridges are checked only by people: visual inspection (Jacquet p.11), expert review (ORC pp.9-10), expert rating (Scout p.8).
4. **Fuzzy goals that resist formalisation are kept outside the solver, not forced into it.** Scout ranks quality outside the solver and measures it separately (pp.4, 8). ORC declares aesthetics out of scope (p.11). Jacquet's minimal-change objective is an explicit stand-in for unstated intent (p.8).
5. **Verdicts come back in the designer's terms, and how far they reach is kept narrow.**
   - Counterexamples are concrete renderings the developer can open in a browser (VizAssert p.2).
   - Unsat cores are mapped to the designer's own annotations (Scout p.5). ORC highlights conflicts in its editor (p.5).
   - Each claim is limited to the encoded constraints and, where relevant, the parameter bounds (VizAssert pp.2, 9). Only VizAssert measured how often its formal verdict disagrees with the fuzzy intent (Table 2, p.9).
6. **A bridge that solves a single instance does not check the fuzzy notion across inputs.** Four of the five find one layout or several. Only VizAssert asks the "for all renderings" question. ORC names the across-sizes failure mode (p.2) and leaves it unchecked.

What these five papers cannot tell us: how bridges in other fuzzy domains compare. Each of these bridges was also assessed by its own authors.

### Earlier synthesis: formalism comparison (from the five papers read only)

**Formalisms that recur**

- Every paper models the UI as a set of rectangles (boxes) with real-valued x, y, width and height. Layout relations are linear equalities and inequalities over those values (Cassowary p.1; VizAssert Fig 3 p.4; ORC p.6; Scout p.5; Jacquet p.6).
- The papers differ on three points:
  1. Whether disjunction is allowed:
     - Cassowary has none.
     - ORC and Scout get disjunction through SMT.
     - Jacquet gets it through big-M binary variables in MILP.
     - VizAssert's visual logic has ∨ in its assertions, and the rendering encoding is QFLRA, which includes Boolean structure.
  2. Whether there is an objective or preference: Cassowary uses lexicographic strength levels; ORC uses weighted soft constraints (MaxSMT/WMax); Jacquet minimises change; Scout ranks results outside the solver; VizAssert has no objective because it decides satisfiability.
  3. What the solver is asked:
     - "find one layout": Cassowary, ORC, Jacquet;
     - "enumerate diverse valid layouts": Scout;
     - "prove no rendering in a bounded parameter range violates property P, or give a counterexample": VizAssert alone.

**How the authors justified their choice of formalism**

1. By the shape of the domain:
   - UI relations are linear inequalities (Cassowary p.1).
   - Linear systems "have a well-understood mathematical basis" (ORC p.3).
   - The violations to be fixed are "intrinsically numerical" (Jacquet p.5).
2. By the expressiveness the domain needs beyond what the previous formalism offered:
   - Preferences and cycles led to Cassowary over local propagation (pp.2-3).
   - Alternatives (OR) led to SMT over LP (ORC p.3, 5).
   - Disjointness led to MILP over LP (Jacquet p.7).
3. By the solver's decidable or efficient fragment:
   - VizAssert restricts its logic to linear, universally quantified, non-recursive formulas so that queries stay QFLRA (p.4).
   - Scout precomputes size triples because Z3 handles multiplication poorly (p.5).
   - Cassowary drops strict inequalities and nonlinearity (p.24, App-5).
4. VizAssert alone uses an existing external standard (W3C CSS 2.1) as the formal model and validates the formalization against that standard's conformance test suite (pp.10-11). It is also the only one that checks its own encoding against the standard's rules on every run, with the solver proving those rules by induction (p.8). This is the closest of the five to "use the tooling that verifies the domain": the standard is the specification, the conformance suite is the oracle for the formalization, and the SMT query checks properties over all renderings in a parameter range.

**Gaps the authors themselves name**

- The property gap: a formal assertion is not the guideline it encodes. VizAssert's descender false positive (p.10). Jacquet's constraints must be "complete" because "the human eye makes many implicit assumptions" (p.14).
- Coverage of the domain:
  - CSS is "thousands of printed pages", and tables are an open research problem (VizAssert p.11).
  - Aesthetic and usability principles are out of scope (ORC p.11).
  - Scout's "clean" quality had to be ranked outside the solver (p.4), and designers judged its layouts less clean (p.9).
- Scale: ORC reaches about 2 s at 265 constraints (p.10); Scout covers mobile-sized screens only (p.4); Jacquet depends on the zone-of-influence reduction (p.13); VizAssert's SMT instances reach about 1M terms (p.10).
- Only VizAssert checks across inputs. The others solve for one configuration. ORC states that specification errors may show only at particular sizes (p.2) but offers no check for it.

**Unknown from these five papers**

- Whether anyone has verified Apple Auto Layout or Android ConstraintLayout specifications themselves, for example for ambiguity or conflict across all screen sizes. Search 5 found no such paper.
- How Cassius (OOPSLA 2016) encodes CSS. I did not read it; what I have is only VizAssert's description of it (VizAssert pp.3, 11).

## Not read

No claims are made here about the content of these papers; the paper or snippet that pointed to each is named.

- Panchekha & Torlak, "Automated Reasoning for Web Page Layout", OOPSLA 2016 (Cassius), DOI 10.1145/2983990.2984010. Retrieval failed (see the Search log).
- Panchekha, PhD thesis "Automated Reasoning for Web Page Layout", University of Washington, 2019. Found by search; not retrieved.
- Badros, Borning, Marriott, Stuckey, "Constraint Cascading Style Sheets for the Web", UIST 1999. Cited by Cassowary and VizAssert.
- Borning, Marriott, Stuckey, Xiao, "Solving Linear Arithmetic Constraints for User Interface Applications", UIST 1997 (QOCA).
- Borning, Freeman-Benson, Wilson, "Constraint Hierarchies", Lisp and Symbolic Computation 1992.
- Hallé et al., "Declarative layout constraints for testing web applications", JLAMP 2016 (Cornipickle). Cited by VizAssert [21] and Jacquet [7].
- Bielik, Fischer, Vechev, "Robust Relational Layout Synthesis from Examples for Android", OOPSLA 2018. Cited by Scout [6] as an earlier use of the same basic constraints.
- Moritz et al., "Formalizing Visualization Design Knowledge as Constraints: Draco", IEEE TVCG 2019. Cited by Scout [35].
- Hottelier, Bodik, Ryokai, "Programming by Manipulation for Layout", UIST 2014. Cited by ORC [14] and Scout [20].
- Zeidler et al., Auckland Layout Editor (UIST 2013) and "Tiling Algebra for Constraint-Based Layout Editing" (JLAMP 2017). Cited by ORC.
- Dayama et al., "GRIDS: Interactive layout design with integer programming", CHI 2020; Oulasvirta et al., "Combinatorial optimization of graphical user interface designs", Proc. IEEE 2020. Cited by Jacquet.
- Walsh, Kapfhammer, McMinn, "Automated Layout Failure Detection for Responsive Web Pages Without an Explicit Oracle", ISSTA 2017. Cited by VizAssert and Jacquet.
- Hosobe, "Solving Hierarchical Soft Constraints with an SMT Solver". Found in search 4.
- A paper that models UI models as reference nets converted to SMT formulae for Z3. Seen in a search-1 summary; no title was given.
- Scout's supplementary materials, which contain the full constraint equations.

## Open questions

- Q's target domain and UI platform are not stated in my brief. Which formalism is "closest" depends on that:
  - For web/CSS rendering, the VizAssert/Cassius line (a formalised standard, QFLRA, Z3) is the closest reviewed here.
  - For widget layout specs like Auto Layout, the closest is Cassowary-style linear constraint hierarchies, plus SMT if alternatives are needed (ORC).
  - For design-principle checking, the closest is Scout-style compilation of principles into spatial constraints, with an unsat core to explain conflicts.
- Is the goal synthesis (find a layout), verification (prove a property over all screen sizes or inputs), or repair? Of the five papers, only VizAssert addresses verification across inputs.
- Reading Cassius and the CCSS paper would show how a standard was first mapped to QFLRA, and how designer and viewer preferences were combined as constraints. Both need retrieval: try the browser-based sci-hub route or the UW thesis.
