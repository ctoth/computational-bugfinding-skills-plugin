# Research: bridges from informal domains to formalisms

## Question

Q (2026-11-07): "we have a fuzzy world, then we have formalisms. we are building one possible bridge, which will tell us how to build bridges." And: "finding the closest formalism is gonna be important."

Scope: how researchers take an informal, real-world domain and connect it to a formalism that tools can check. Parts of a bridge: what is observed, how it is encoded, what is lost, how verdicts return and what they may claim, and how the formalism is chosen.

## Search log

Collection check (C:/Users/Q/code/papers/index.md, 2026-11-07): 10 papers present; none on the general informal-to-formal step. Kingsbury_2020_Elle is present (read earlier by another agent; not re-read here).

WebSearch queries (2026-11-07) and candidates:

1. `Zave Jackson "Four dark corners of requirements engineering" pdf` -> Zave & Jackson, TOSEM 6(1) 1997, pp. 1-30. Candidate (selected).
2. `Gunter Gunter Jackson Zave "A reference model for requirements and specifications" pdf` -> Gunter, Gunter, Jackson, Zave, IEEE Software 17(3) 2000, pp. 37-43. Candidate (selected).
3. `Barr Harman McMinn "The oracle problem in software testing: a survey" pdf` -> Barr et al., IEEE TSE 41(5) 2015, open copy at UCL Discovery. Candidate (selected).
4. `Brian Cantwell Smith "The limits of correctness" 1985 model reality pdf` -> Smith, SIGCAS Computers and Society 1985, copy at student.cs.uwaterloo.ca. Candidate (selected).
5. `Parnas Madey "Functional documents for computer systems" four-variable model ...` -> Parnas & Madey, Science of Computer Programming 25 (1995) 41-61, copy at files.ifi.uzh.ch. Candidate (selected).
6. `Michael Jackson "The world and the machine" ICSE 1995 pdf` -> Jackson, ICSE '95 pp. 283-292, DOI 10.1145/225014.225041; no open PDF found. Candidate (not selected; overlaps 1-2).
7. `choosing a formalism for a domain "formalization" informal requirements to formal specification method paper` -> Bruel et al., "The Role of Formalism in System Requirements", ACM Computing Surveys 2022 (arXiv 1911.02564); "Towards a framework for selecting notations for modelling requirements" (Hertfordshire); "Formalization and Validation of Safety-Critical Requirements" (arXiv 1003.1741); Pang et al. 2016 on user-friendly specification languages. Bruel et al. is the candidate for "how the formalism is chosen".
8. `"A Reference Model for Requirements and Specifications" Gunter filetype:pdf upenn OR illinois` -> no authorized open copy found (only typeset.io, which returned HTML). Gunter et al. 2000 dropped; Zave states on pamelazave.com/fre.html it condensed "Four dark corners".

Retrieval (2026-11-07), into C:/Users/Q/code/papers/:
- Parnas_1995_FunctionalDocumentsComputerSystems: PDF from files.ifi.uzh.ch (21 pp).
- Barr_2015_OracleProblemSoftwareTesting: PDF from web.eecs.umich.edu (31 pp, title page matches TSE paper; UCL copy returned HTML).
- Smith_1985_LimitsCorrectness: PDF from student.cs.uwaterloo.ca (9 pp).
- Zave_1997_FourDarkCornersRequirements: PDF from pamelazave.com/4dc.pdf (35 pp, author copy).
- Bruel_2019_RoleFormalismSystemRequirements: arXiv 1911.02564 via fetch_paper.py.
- Sci-hub path blocked by a DDoS-Guard browser check; not used.

## Papers read

Each read by me through paper-reader from page images; notes at C:/Users/Q/code/papers/<dir>/notes.md.

1. Smith 1985, "The Limits of Correctness" (all 9 pages). Dir: Smith_1985_LimitsCorrectness. Page numbers below are printed pages 18-26.
2. Parnas & Madey 1995, "Functional Documents for Computer Systems" (all 21 pages). Dir: Parnas_1995_FunctionalDocumentsComputerSystems.
3. Zave & Jackson 1997, "Four Dark Corners of Requirements Engineering" (all 35 pages, author manuscript). Dir: Zave_1997_FourDarkCornersRequirements.
4. Barr, Harman, McMinn, Shahbaz & Yoo 2015, "The Oracle Problem in Software Testing: A Survey" (all 31 pages, preprint). Dir: Barr_2015_OracleProblemSoftwareTesting.
5. Bruel, Ebersold, Galinier, Mazzara, Naumchev & Meyer 2019, "The Role of Formalism in System Requirements (full version)" (all 46 pages, arXiv v6). Dir: Bruel_2019_RoleFormalismSystemRequirements.

Process notes: I read every page image of all five papers myself (an attempt to hand papers to separate reader agents was refused by the harness: teammates cannot spawn teammates). Each paper has notes.md, description.md, abstract.md, citations.md, metadata.json (cite_key added), an index.md entry and a _reader_done.tsv line. Deviation from paper-reader: citations.md for Barr (211 refs) and Bruel (148 refs) lists only the references used in the notes, not the full lists; reconcile was done by hand (cross-reference sections among these five papers), not by the reconcile skill's full procedure.

Already in the collection and relevant, not re-read here: Kingsbury_2020_Elle (read earlier by another agent through paper-reader). I state nothing from it below.

## Findings

### Smith 1985, The Limits of Correctness

- Structure of the bridge: COMPUTER -- MODEL -- REAL WORLD (Fig. 1, p.21). Specification and program are both written "in terms of the model" (p.22). Model theory covers the left relation (description to model); for the right relation (model to world) "we have no theory" (p.21).
- Observation: what the model attends to is chosen at a level of abstraction set by purpose; models "have to be partial: that's how they are able to work" (p.20-21). Example: traffic lights detect metal, so bicycles do not fit the model (p.20).
- Losses: models "fail to correspond to the world in indefinitely many ways"; failures come when they fail "in a crucial and relevant way" (moon-rise radar false alarm, 1960) (p.23). Specifications always rely on an unstated common-sense background (refrigerator example, p.23-24), and must also model "the relevant part of the world in which it will be embedded", including use (p.24).
- Return of verdicts: a correctness proof shows only that two formal descriptions are compatible; Smith calls this "relative consistency" (p.23). When the proof fails, "there is no more reason to believe that the first (the specification) is any more correct than the second" (p.22). Simulation "tests only the left-hand side relationship" (p.25). Evidence about the model-world fit comes from action and feedback (robot sensors, p.21) and from experience "in their destined situations"; "a proof of correctness is at best added insurance, not a replacement, for real life experience" (p.25).
- Value of formalizing even so: proof attempts "force you to delineate, very explicitly and completely, the model", which unearths bugs from "sloppiness and unclarity about the model" (p.23).
- Choice of formalism: no procedure given. Modelling has the best hope in "systematic domains" (Winograd's term), where "the relevant stock of objects, properties, and relationships are most clearly and regularly pre-defined" (p.24).

### Parnas & Madey 1995, Functional Documents for Computer Systems

(All 21 pages read. Printed pages 41-61.)

- Observation: "A critical step ... is the identification of the environmental quantities to be measured or controlled and the representation of those quantities by mathematical variables" (p.47). Quantities include physical properties, display readings, administrative information, "even the wishes of a human user"; each is monitored, controlled, or both (p.47).
- Encoding: each quantity is a variable whose value is a time-function; "coordinate systems, signs, etc., must be unambiguously stated", often with diagrams (p.47). Natural language for "the physical interpretation of mathematical variables is both unavoidable and usual in engineering" (p.51). Relations: NAT (what nature and existing systems allow), REQ (what the system should permit), IN (monitored quantities to input registers), OUT (output registers to controlled quantities), SOF (software) (p.48-50).
- Losses are kept explicit rather than hidden: IN is a relation "as a result of imprecision in the measurement and transducer devices"; OUT "because of unavoidable device imperfections"; REQ because "one can tolerate 'small' errors" (p.48-49). Monitored values outside domain(NAT) "the system designers may assume ... will never occur" (p.48). Requirements are written in the variables the user cares about even when the system senses other, related variables (fn.3, p.47).
- Return of verdicts: acceptability is (NAT cap (IN.SOF.OUT)) subset of REQ (4c, p.51), equivalently the implication 4a (p.50). The verdict is conditional: when IN, OUT or NAT is false "any software behaviour will be considered acceptable"; a broken device releases the software, and weaker "fail-soft" versions of the relations give graded obligations (p.50). Feasibility (domain(REQ cap NAT) = domain(NAT)) claims only that nature allows the requirement, "not that the functions involved are computable" (p.49). Division of labour: requirements authors write NAT, REQ, IN, OUT; software designers determine SOF and verify 4a-4c (p.51). Proposed tools: table validity checks, simulation, test-case generation, run-time checks (p.58); cites Peters & Parnas 1994 on generating a test oracle from documentation (ref [43], p.60).
- Choice of formalism: identify the relations first, choose notation second; "there is no single representation that is ideal" (p.45). Universal notations (VDM, Z) are "a trap" (p.56). Reuse the established engineering formalism: the requirements model "is essentially that used in control theory" (p.57), and proposers of new real-time logics "should be explaining why they cannot use an approach that has been taught to Engineers for many years" (p.44). Tables suit functions with many discontinuities (p.56); small state spaces (protocols, chips) permit enumerative verification (p.55-56).
- Cost: "useful but very time consuming"; "not ... fully practical until we have new tools" (p.58).

### Zave & Jackson 1997, Four Dark Corners of Requirements Engineering

(All 35 pages of the author's 16 July 1996 manuscript read; page numbers are the manuscript's, not TOSEM's.)

- Observation and designation: "Any formal representation uses primitive terms with no inherent formal meaning ... the meaning of these terms lies in the real world, and the validity of any formal assertion relies on it" (p.2). "The only way to establish the meaning of a primitive term is to provide an informal explanation of it ... written down, and ... maintained as an essential part of the requirements documentation"; this is a "designation" (p.3). The subject matter is given as "designations of phenomena observable" in the domain (zoo entrance: visitors, coins, entering), which circumscribes what can be considered (p.4-5). Machine state "cannot be designated" (p.10); auxiliary terms are grounded by defining them from designated terms (p.10).
- Assertion vs definition: an assertion over designated terms "constrains the real world ... might be true or false, and should be validated before it is used"; a definition "cannot be false" (p.4).
- Encoding: every statement is about the environment, either indicative (domain knowledge K: the environment regardless of the machine) or optative (requirements R and specifications S) (p.7). Actions are environment- or machine-controlled and shared or unshared; unshared ones are "unobservable by the machine" (p.11). Four notation rules: designate or define every atomic term; classify every action; allow constraints on all categories; tag every property as R, K or S (p.28). "If a requirements language is insufficient ... its users should be able to augment or supplement it" (p.27).
- Losses: the machine's model of the environment is imperfect ("delay, errors, and factors in the real world that the machine does not know about"; warehouse theft, breakage, clerical errors) (p.10). When no shared phenomena determine a quantity (actual quantity-in-bin), "refinement is not possible"; the requirement must be restated in "the best implementable estimate" (expected-quantity-in-bin) with added requirements such as periodic stock inventories to shrink the difference (p.23-24). Some domain knowledge is approximate (four-second dialling rule, p.24) or "a highly probable assumption rather than an unalterable fact" (p.25). Vague "soft" requirements are outside the account "until they are precise enough to be formalized" (p.25).
- Return of verdicts: S, K |- R (p.20). Completion: R validated informally with the customer; K "validated (checked informally) as true of the environment"; S free of environment constraints, unshared phenomena and future reference; proof of S, K |- R; proof that S and K are consistent (p.29-30). If an assumption fails, "the requirement will not be satisfied, even if the lift controller is perfect" (p.25). So the proof's claim about the world is conditional on K.
- Choosing the formalism: no notation promoted (p.2); languages are judged against the minimum capabilities. Z lacks control and environment constraints (p.17-18); SCR forced an environment fact (train stays near crossing at least 300 s) into a machine constraint, "dangerous ... if taken literally" (p.18-19); CSP conflates control and observability (p.19); agent formalisms have all capabilities (p.19). Buchi automata used because which actions are constrained, and safety vs liveness, are visible in the syntax, so one can "determine syntactically whether a requirement is a specification or not" (p.12, 22). An "acceptable" specification "depends on the expressive power of the chosen specification language" (p.26).

### Barr, Harman, McMinn, Shahbaz & Yoo 2015, The Oracle Problem in Software Testing: A Survey

(All 31 pages of the preprint read; printed page numbers.)

- Observation: stimuli S (explicit inputs and environmental factors such as configuration, device states, sensor inputs) and observations R (explicit outputs and nonfunctional profile such as execution time, heat, power); observations are "anything that can be discerned and ascribed a meaning significant to the purpose of testing"; what lies outside S cup R "neither affects nor is affected by" the SUT (Fig. 1, p.3).
- Encoding: a test oracle is "a partial function from a test activity sequence to true or false" (Def 2.4, p.4); a probabilistic oracle maps to [0,1] (Def 2.5, p.4). Sources, in the survey's order: specified (model-based languages, state transition systems, assertions/contracts, algebraic specifications) (p.9-12); derived from artefacts (pseudo-oracles and N-version, metamorphic relations, regression, invariants, mined models, textual documentation) (p.13-19); implicit ("buffer overflows and segfaults are nearly always errors", p.19); human (p.20).
- Losses: formal specifications "necessarily rely on abstraction" causing "imprecision, models that include infeasible behavior or that do not capture all the behavior relevant", plus the problem of "interpreting model output and equating it to concrete program output" (p.13). The model can be "quite far from concrete execution output"; it serves as an oracle only if the "impedance mismatch can be overcome, by abstracting a system's concrete output or by concretizing a specification model's output" and postconditions are evaluable in finite time (p.9). "Models approximate a SUT, so behavioral differences between the two are inevitable. Some divergences ... are spurious and falsely report testing failure" (p.10).
- Return of verdicts: soundness D(a) => G(a) and completeness G(a) => D(a) against a ground truth G that "cannot be known in all but the most trivial cases"; oracles "cannot, in general, be both sound and complete" (p.5). Probabilistic soundness requires advantage eps over a coin so repeated sampling gives arbitrary confidence (p.5). When an algebraic axiom and the implementation disagree, the fault is "in the implementation or in the axiom" (p.12). Invariants inferred from a run prefix give "an unsound test oracle" (p.16). Implicit oracles hold only "in some context"; "Even crashing may be considered acceptable" (p.19-20). Conformance depends on whether behaviour "is observable and can be interpreted at the same level of abstraction as the model's" (p.10).
- Choosing an oracle source: no general criterion; the ladder follows which artefacts exist (p.2). Derived oracles may "migrate, over time" into specified ones (p.13). Informal text can be turned into a formal specification by sequential enumeration (finds "many inconsistent and missing requirements", exponential) or by restricting natural language (PENG, translated to first-order logic) (p.19). Model inference is limited to restricted classes "such as those whose behaviour can be modelled by finite state machines" because equivalence is undecidable (p.17).

### Bruel, Ebersold, Galinier, Mazzara, Naumchev & Meyer 2019, The Role of Formalism in System Requirements (full version)

(All 46 pages of arXiv 1911.02564v6 read; page numbers are the printed "1:N".)

- Observation: requirements describe properties "as relevant to its human users, or more generally its environment" (p.2). Criterion 7 (Scope) asks whether an approach covers the environment ("domain") or only the system, citing the Jackson-Zave distinction (p.5).
- Encoding: five families (natural language, analysed or constrained; semi-formal; automata/graph; mathematical; seamless programming-language) and 22 approaches (Table 1, p.5), each shown on the same Landing Gear System requirements (p.3).
- Losses, shown in the worked encodings: Requirements Grammar allows one subject per requirement, so R11bis must be split (p.7). Alloy "has no native mechanism for expressing properties such as 'handle remains in the DOWN position'", so R21 is rewritten with "is" and becomes "stronger than the original", and R11bis becomes "three transitions ... will suffice", checked "for 5" (search bound) (p.25-26). Tables lack temporal operators, so R21/R22 become "an immediate, rather than temporal, response" (p.26-27). FSP needs artefact events not in the informal spec and a priority operator, after which "one cannot verify both sets of assertions under the same conditions" (p.20-21).
- Return of verdicts: from none (SysML: "formal verification is not possible", p.15) to simulation (Stimulus, where users "observe the system reaction and correct the requirements", p.9), model checking (LTSA, Petri nets, Statecharts), bounded model checking (Alloy) and proof (Event-B, AutoProof) (p.17-30). "Even a system that has been formally 'proved correct' has only been proved to satisfy a given specification. However sophisticated the proof, if the specification does not reflect the stakeholders' desires, the system is in fact incorrect for all practical purposes" (p.32).
- Choosing the formalism: nine criteria (audience, abstraction, method, tools, traceability, non-functional coverage, scope, verifiability, semantics) and Table 2 (p.4-5, 32). Conclusions: assess "formality against relevant criteria of quality" rather than ideology (p.38); use several views for different stakeholders, with "only a formally defined view" fit "to be usable as the basis to derive others" (p.38); textual and graphical notations are "complementary ... each to be used when and where it is the best way of specifying a given requirement element" (p.35); acceptance needs tools and "tangible benefits commensurate with the effort" (p.38); invest in people "who will translate back and forth between formal and informal views" (p.33). Open: "Is there a general pattern for textual requirements, or does every domain area requires its own?" (p.36).
- Caveat found while reading: Table 2 (p.32) disagrees with the text for FSP/LTSA scope (text p.21: system and environment; table: system only) and for Problem Frames semantics/verifiability (text p.19: no precise semantics, not designed for verification; table: ticks).

## Synthesis

How to build a bridge from a fuzzy domain to a formalism, using only the five papers read. Each part names its source.

1. **Name the phenomena and write down what each term means.** Primitive formal terms have no meaning of their own; their meaning is in the world, and the only way to fix it is a written, maintained informal explanation, a "designation" (Zave & Jackson p.2-3). Parnas & Madey make the same step concrete: list the quantities that matter, give each a variable, and state units, coordinate systems and signs, with diagrams where needed; natural language here is "unavoidable" (Parnas & Madey p.47, 51). Smith adds that the choice of what to attend to is set by purpose and is always partial (Smith p.20-21).

2. **Split what the checker can observe from what it cannot.** Zave & Jackson separate shared phenomena, visible to the machine, from unshared ones, private to the environment (p.11). Parnas & Madey separate the quantities of interest (monitored, controlled) from what the machine actually reads and writes (input and output registers), and connect them by relations IN and OUT (p.49). Barr et al. define the observation side for testing as stimuli and observations, including environmental factors and nonfunctional measures (p.3). A requirement stated in unobservable terms can be checked only through domain knowledge that links it to observable terms; when no such link exists, the requirement has to be restated as a best estimate over observable terms, with extra checks to bound the gap (Zave & Jackson p.23-24).

3. **Keep three kinds of statement apart.** Statements about how the world is regardless of the system (indicative: domain knowledge K, Parnas & Madey's NAT), statements about how it should be (optative: requirements R, REQ), and statements the system can enforce by itself (specification S, SOF) (Zave & Jackson p.7, 20, 28; Parnas & Madey p.48-50). The check is then S, K |- R (Zave & Jackson p.20), or (NAT cap (IN.SOF.OUT)) subset of REQ (Parnas & Madey p.51).

4. **Keep the imprecision visible instead of hiding it.** Parnas & Madey model sensor imprecision, actuator imperfection and tolerance as relations rather than functions (p.48-49). Zave & Jackson mark approximate or only highly probable domain knowledge (p.24-25). Barr et al. give oracles as partial, possibly probabilistic, and in general not both sound and complete (p.4-5).

5. **Pick the formalism after the content, and check what it forces you to change.** Identify the relations first, then pick a notation; no single notation is best for everything, and universal languages are "a trap" (Parnas & Madey p.45, 56). Reuse an established formalism from the neighbouring field (control-theory relations) before inventing one (Parnas & Madey p.44, 57). Judge a candidate against minimum capabilities: can it state environment facts, control, sharing and both moods? If not, augment it or combine it with another (Zave & Jackson p.11, 27-28). Bruel et al. give nine criteria for comparing candidates (p.4-5) and show the cost of a poor fit: encodings in Alloy, tables or FSP silently strengthen, weaken or split the original requirement (Bruel et al. p.7, 20-21, 25-27). A language that cannot state an environment fact pushes it into a machine constraint, which Zave & Jackson call "dangerous ... if taken literally" (p.18-19). The read papers give criteria and failure examples. None gives a procedure that finds "the closest formalism" automatically: unknown.

6. **State what a verdict may claim.** A proof or passing check over the model claims consistency between descriptions written in that model, "relative consistency" (Smith p.23). Its meaning for the world is conditional: on the domain knowledge K being true, which is "validated (checked informally)" (Zave & Jackson p.29), and on the device and environment relations holding; when they fail, the obligation lapses (Parnas & Madey p.50). If the specification does not reflect what stakeholders wanted, a proved system is still wrong in practice (Bruel et al. p.32). A failed check does not by itself say whether the system or the specification is wrong (Smith p.22; Barr et al. p.12). Bounded checks claim only within their bound (Bruel et al. p.26). Simulation over the model tests only the model side (Smith p.25).

7. **Close the loop with the world.** Evidence about whether the model fits the world comes from feedback, use in the real setting and experience, not from checks over the model (Smith p.21, 25). Simulation and counterexamples are used to correct the requirements themselves (Bruel et al. p.9). Derived oracles can migrate into specified ones over time (Barr et al. p.13).

What the read papers do not settle (unknown): how to validate domain knowledge K beyond informal checking; any measure of how far a domain is from a candidate formalism; and how to choose a formalism for a domain that is not a "systematic domain" in Smith's sense (Smith p.24 names the term only).

## Not read

Not read through paper-reader. Nothing is stated from these in this report.

- Gunter, Gunter, Jackson & Zave 2000, "A Reference Model for Requirements and Specifications", IEEE Software 17(3). No authorized open copy found; sci-hub blocked by a browser check.
- Jackson 1995, "The World and the Machine", ICSE '95, DOI 10.1145/225014.225041. No open copy found.
- Jackson & Zave 1995, "Deriving specifications from requirements: an example", ICSE '95 (cited by Zave & Jackson 1997; open copy may be at pamelazave.com/turnstile.pdf, not fetched).
- Peters & Parnas 1998, "Using test oracles generated from program documentation", IEEE TSE 24(3) (cited by Barr et al. and Bruel et al.).
- Staats, Whalen & Heimdahl 2011, "Programs, tests, and oracles: the foundations of testing revisited", ICSE.
- Dwyer, Avrunin & Corbett 1998, "Property Specification Patterns for Finite-State Verification", FMSP.
- Meyer 1985, "On Formalism in Specifications", IEEE Software.
- Gay, Rayadurgam & Heimdahl 2014, "Improving the accuracy of oracle verdicts through automated model steering", ASE.
- Search-result candidates: "Towards a framework for selecting notations for modelling requirements" (Hertfordshire); "Formalization and Validation of Safety-Critical Requirements" (arXiv 1003.1741); Pang et al. 2016 on user-friendly specification languages.

## Open questions

- Is there a read source with a procedure for choosing the closest formalism, beyond criteria lists? Candidates to read next: Meyer 1985; the Hertfordshire notation-selection paper; Jackson's Problem Frames book (2001).
- How is domain knowledge K validated in practice? Candidate: Jackson & Zave 1995 (turnstile case study).
- How do verdicts get back from a model to concrete observations at a different abstraction level? Candidates: Peters & Parnas 1998; Gay et al. 2014 (model steering); Staats et al. 2011.
- Kingsbury_2020_Elle is in the collection as a possible worked example of a bridge (observed histories to a dependency-graph formalism); I did not re-read it and state nothing from it here.
