# Research: Seligman information flow (channel theory) as a bridge formalism

## Question

Q's pointer (2026-11-07): "Seligman information environments, logical flow". Context: "we have a fuzzy world, then we have formalisms. we are building one possible bridge, which will tell us how to build bridges"; "finding the closest formalism is gonna be important".

What does Jerry Seligman's work (with Jon Barwise and others) say about information flow between systems: classifications, infomorphisms, channels, local logics? What does "information environments" refer to in Seligman's work? What primary work connects channel theory to Goguen's institutions?

## Search log

Collection check (2026-11-07): `C:/Users/Q/code/papers/` (15 papers) and every `C:/Users/Q/code/*/papers/` directory listing grepped for seligman, barwise, infomorph, channel, information flow, schorlemmer, kalfoglou, Kent: no channel-theory works present. Goguen & Burstall 1992 is present (read by the institutions report).

1. WebSearch `Seligman "information environments" channel theory` -> no source joins Seligman to the phrase. Hits: arXiv 2206.02283 (situation and channel theory for imperfect information, cites Seligman 2009); "information environments" hits are all from information-foraging / information-architecture writing (Pirolli, journalofia.org), not Seligman.
2. WebSearch `Barwise Seligman "Information Flow: The Logic of Distributed Systems" pdf` -> Cambridge Tracts in TCS 44, CUP 1997; Cambridge Core chapter pages (paywalled); PhilArchive record BARIFT (record only, to check). No authorized open PDF in results.
3. WebSearch `Goguen "information integration" institutions channel theory Barwise Seligman infomorphism` -> Goguen, "Information Integration in Institutions", for the Jon Barwise memorial volume (ed. L. Moss); listed on cseweb.ucsd.edu/~goguen/projs/inst.html and /projs/data.html. Kent arXiv 1810.02929 "System Consequence" (generalizes channel theory to institutions, its section 3); arXiv 1603.03475; arXiv 1810.08074.
4. WebSearch `"Jerry Seligman" "information environment"` -> nothing connecting Seligman to the phrase in 18 results.
5. WebSearch `Seligman "Channels: from logic to probability" pdf` -> chapter in Sommaruga (ed.), Formal Theories of Information, Springer LNCS 5363, 2009, pp. 193-233; Auckland ResearchSpace handle 2292/13632 marked restricted. A university-proxy Springer mirror appeared (springerlink.bibliotecabuap.elogim.com); not used (walled copy).
6. WebSearch `Kent "Information Flow Framework" IFF institutions channel theory arXiv` -> Kent arXiv 1603.03475 "Information Flow in Logical Environments" (2016); 1810.02929 "System Consequence"; 1810.08236 and 1109.0032 "Semantic Integration in the IFF"; 1108.4133 IFF metatheory. Note: Kent's title uses "logical environments", a near-match to Q's "information environments"; whether Q meant this is not known.

7. WebSearch `Seligman "environments" information flow logic paper situation theory "Seligman, J."` (extended) -> no Seligman work with "environments" in its title; closest named match again Kent 1603.03475.
8. Seligman's CV (logic.pku.edu.cn/ann_attachments/seligman-cv.pdf, 3 pp, publications to 2010, text searched): no item titled or described with "information environment(s)". Items found: Barwise & Seligman 1997 book; "Imperfect Information Flow" (LICS 1993); "The Rights and Wrongs of Natural Regularity" (Phil. Perspectives 8, 1994); Moss & Seligman "Classification Domains and Information Links" (1994); "Physical Situations and Information Flow" (1991); Seligman, Mares & Restall "Situation Theory II: Constraints and Channels" (Handbook of Logic and Language 2nd ed.); "Channels: from Logic to Probability" (2009).
9. WebSearch for book PDFs / "Imperfect information flow" PDF -> LICS 1993 DOI 10.1109/LICS.1993.287582 (IEEE, paywalled); no open copy. A copy of book front matter at mimuw.edu.pl/~skowron/WM/Logika/ksiazka/part1.pdf (a course page, not author or publisher); not used.
10. WebSearch `Mares Seligman Restall "Situations, Constraints and Channels" pdf consequently.org` -> author copy at consequently.org/papers/sitconchan.pdf (Restall's page; chapter in Handbook of Logic and Language, 2nd ed., Elsevier 2011, pp. 329-344).

## Retrieval log

- Goguen, "Information Integration in Institutions": author page cseweb.ucsd.edu/~goguen/pps/ifi04.pdf -> 48-page PDF, saved `C:/Users/Q/code/papers/Goguen_2006_InformationIntegrationInstitutions/paper.pdf`.
- Kent, "Information Flow in Logical Environments", arXiv 1603.03475: `fetch_paper.py` failed (arXiv API HTTP 429); direct arxiv.org/pdf/1603.03475 -> 16-page PDF, saved `C:/Users/Q/code/papers/Kent_2016_InformationFlowLogicalEnvironments/paper.pdf`.
- Barwise & Seligman 1997 book, DOI 10.1017/CBO9780511895968: `fetch_paper.py` -> Semantic Scholar 404, "Could not resolve metadata". Unpaywall API refused the plugin's placeholder email (HTTP 422, "Please use your own email address"); I did not send Q's email. Cambridge Core chapters are paywalled; PhilArchive record BARIFT returned HTTP 403. No author or publisher open copy found. Not retrieved.
- Mares, Seligman & Restall, "Situations, Constraints and Channels": consequently.org/papers/sitconchan.pdf -> 8-page PDF, saved `C:/Users/Q/code/papers/Mares_2011_SituationsConstraintsChannels/paper.pdf`.
- Seligman 2009 "Channels: from Logic to Probability": Auckland ResearchSpace 2292/13632 marked restricted; only other copy seen is a university-proxy Springer mirror, not used. Not retrieved.

## Papers read

- **[MSR]** Mares, Seligman & Restall, "Situations, Constraints and Channels (Update of Chapter 4)", Handbook of Logic and Language 2nd ed., Elsevier 2011, ch. 5, pp. 329-344, DOI 10.1016/B978-0-444-53726-3.00005-0. Author copy. `C:/Users/Q/code/papers/Mares_2011_SituationsConstraintsChannels/`. Read from page images through paper-reader, all 16 pages. Printed pages cited.
- **[Kent]** Robert E. Kent, "Information Flow in Logical Environments", arXiv 1603.03475v1, 2016 (arXiv notes it was completed in 2008). `C:/Users/Q/code/papers/Kent_2016_InformationFlowLogicalEnvironments/`. All 16 pages read from page images. Printed pages cited.
- **[Goguen]** Joseph Goguen, "Information Integration in Institutions", draft for the Jon Barwise Memorial Volume (ed. L. Moss), author copy cseweb.ucsd.edu/~goguen/pps/ifi04.pdf, dated 2006 in [MSR]'s and [Kent]'s reference lists. `C:/Users/Q/code/papers/Goguen_2006_InformationIntegrationInstitutions/`. All 48 pages read from page images. Printed pages cited.

Paper-reader deviations: notes, metadata, description, abstract and citations files were written for each work. I did not append to `C:/Users/Q/code/papers/index.md` or `_reader_done.tsv`, and did not run reconcile or the keymap rebuild, because these are shared collection files outside my allowed paths. The Goguen citations.md lists 29 of the 75 references.

## Findings

### [MSR] Mares, Seligman & Restall 2011

Definitions (modern channel theory, attributed to Barwise & Seligman 1997):
- **Classification**: "simply a binary relation ⊨_A between a set tok(A) of tokens and a set typ(A) of types" (p.337).
- **Theory**: types with a relation ⊢ between subsets; Γ ⊢_T Δ is "a prohibition on classifying tokens to have all the types in Γ and none of the types in Δ" (p.337).
- **Local logic**: a classification plus a theory plus a set N_L of *normal* tokens, such that if Γ ⊢_L Δ "there is no normal token of all the types in Γ and none of the types in Δ" (p.337). The constraints bind only the normal tokens.
- **Infomorphism** f: A -> B: "a pair of contra-variant functions f^: typ(A) -> typ(B) and f˅: tok(B) -> tok(A)" with f˅(b) ⊨_A α iff b ⊨_B f^(α) (p.339). Types go forward, tokens go backward.
- **Logic-infomorphism**: also preserves the theory and the normal tokens. For logics built from a theory and its models, it is "an interpretation of theory T1 in theory T2 together with a transformation of models in M2 into models in M1 that preserves the satisfaction relation" (p.339).
- **Channel**: a *core* classification C with two infomorphisms, s_C: C -> A (source) and r_C: C -> B (receiver). "a token c of C [is] the specific connection within the channel that relates source token s˅(c) to receiver token r˅(c)" (p.339). Generalised channel: any set of infomorphisms out of one core; information "flows in both directions" (pp.340-341).
- **Refinement**: an infomorphism between cores that commutes with the source and receiver maps, "ensuring that any information that flows in one channel also flows in the refined channel" (p.340). Serial composition C1;C2 and parallel composition C1•C2 are the least refined channels agreeing with their parts (p.340).

What must hold for information to flow, and how a conclusion carries:
- Early version: a channel c "supports the constraint A -> B if and only if for each signal-target pair s and t where s ↦c t, if s ⊨ A then t ⊨ B" (p.331). The conclusion t ⊨ B is licensed only for a target the channel actually links to the observed signal.
- Modern version: local logics move between classifications along infomorphisms, by image fL (the least logic on B making f a logic-infomorphism) and inverse image f⁻¹L′ (the greatest on A), and combine by meets and joins in a complete lattice. "In this way information distributed around a network of channels may be moved from one classification to another" (p.340, fn 9).
- "it is logical structure—entailment, contradiction, etc.—that is transformed by infomorphisms, not propositional content" (p.340, fn 10).
- A statement φ "infomorphically entails" ψ if φ implies ψ along every infomorphism. Per van Benthem 2000 (cited, not read), this holds iff there is a "flow formula" α with φ ⊢ α ⊢ ψ. Flow formulas are built from a ⊨ t, its negation, &, ∨, existential quantification over tokens and universal over types, and "are all preserved over infomorphisms" (p.342). So the statements that are guaranteed to carry across any infomorphism are exactly those of this syntactic shape.

Fallible flow:
- Fallibility is a stated desideratum: the student who sees an 'A' "is reading a forgery" in an indistinguishable situation (p.331). Channels are "objective 'links' ... These links may be present or absent, distinguishing veridical information flow from cases of misinformation" (p.331).
- **Pseudo signal**: a thermometer that was never near a patient; "the channel does not connect any patient situation with the thermometer situation" (p.332). The channel "does not link *all* tea drinking situations with matching better feeling ones. It merely links 'appropriate' ones" (p.332). The regularity stays true; the error is applying it to an unlinked token.
- **Abnormal tokens**: in a local logic, a token that violates the constraints is "classified but flagged as strange, and we model it as a token that lies outside the set of normal tokens" (p.337). In a probabilistic version, "Aberrant behaviour of the system, perhaps due to outside influences or initial conditions can be marked as non-normal" (p.338, fn 7; needs Seligman 2009, not read).
- Smoke and fire: whether smoke indicates fire "depends a great deal on the circumstances"; the background condition can be modelled as the type of channel mediating the flow (p.336).

Modelling a real, informal system as a classification:
- Schemes of individuation: "Different languages ... give us different ways of grouping objects together", and "we adapt our conceptual repertoire according to context, employing only those distinctions that are salient and/or useful" (p.336). Seligman 1990 calls the typing relations *perspectives* and allows several (p.336).
- The local logic of a formal theory and its models is "atypical in having a token that is a counterexample to every inference not licensed by T. Local logics used to model classification by humans or other finite agents are unlikely to have this property" (p.337).
- Children classifying leaves: constraints are "either explicitly or implicitly, some self-imposed, some deriving from language". An inference may be invalid without a counterexample in hand: "Even if there are red pointy leaves in the token set and they all have three points, this may be a regularity of the sample, not one that is part of the child's classificatory method" (pp.337-338, Fig 5.1).
- An observed dynamic system: tokens are observed instances, which "may not include tokens of all possible states but only the ones that have been observed. Our observations are rarely capable of discriminating individual states, so observation types correspond to a limited selection of subsets of the state space" (p.338).
- The chapter cites Goguen (2006) as showing the categories of classifications and local logics "to be special cases of a much broader class of categories, which have been extensively studied in computer science" (p.339, fn 8).
- "Information environments": the phrase does not occur in this chapter (all 16 pages read).

### [Kent] Kent 2016, Information Flow in Logical Environments

- **Logical environment**: "a more semantic version of an institution" (p.6). It has a category of structures (the world) indexed by languages, sentences, and satisfaction, with "truth preserved under change of notation" (p.6). Kent states the satisfaction condition and calls it the "infomorphism condition": the structures, sentences and satisfaction relation of each language form a classification, and each language morphism gives an infomorphism, so the whole is a functor cls: Lang -> Cls into classifications and infomorphisms (p.3).
- **The two views** (p.1): IF is one institution (types as unary predicates, a subenvironment of FOL, p.8). Conversely the IF classification relation "can be regarded as an abstraction of the INS satisfaction relation", so Kent argues "IF as an abstraction and extension of INS" (p.1; conclusion p.16).
- **Distributed system and channel**: a distributed system is a diagram of structures; an information channel is a family of structure morphisms g_i: A_i -> C into a common *core*; a covering channel is a cocone; the minimal cover is the colimit (p.10). Kent names two concerns: "(1) given a distributed system and some viewpoint (scientific, technological, social, etc.), how should the whole system be modeled; and (2) how does the natural logic of one component part of a system affect another component part" (p.10). The first "can have several solutions" (p.11).
- **When information carries**: A_i satisfying a_i "carries the information that A_j satisfies sentence a_j, relative to the channel C, if the translation sen(γ_i)(a_i) entails the translation sen(γ_j)(a_j) in the theory max(C)" (p.11). The conclusion is relative to a chosen channel.
- **Transfer rules along a morphism f: M1 -> M2** (pp.11-12, paraphrasing B&S part I):
  - f-Intro (translate forward) preserves validity but not nonvalidity.
  - f-Elim (translate back) preserves nonvalidity but not validity. It is sound only when M1 is isomorphic to the reduct of M2: "the f-Elim rule preserves validity along structure-isomorphic structure morphisms" (p.12).
  - In system terms: a component's constraint becomes a constraint of the whole; a constraint of the whole comes back only to "those parts that really are (up to isomorphism) a component of the system structure" (p.12).
  - Proximal to distal across a binary channel P -> C <- D: p-Intro gives a theory at C that "may be sound ... but not necessarily complete ... there may be constraints of C that are missed". Then "following p-Intro by d-Elim means that we lose our guarantee that the resulting distal theory is either sound or complete. A sentence about the distal structure obtained from a sentence about the proximal structure in this way is guaranteed to apply when the distal structure is connected (up to isomorphism) to the proximal structure in the channel" (p.12).
- **Local logics, soundness, completeness** (pp.13-14): a logic is ⟨Σ, M, T⟩. It is *sound* when M satisfies T, and *complete* when T entails every sentence M satisfies. "In general, logics may be neither sound nor (logically) complete"; "The only sound and complete logics are those equivalent to the natural logic log(M)" (p.14). Kent's logics have no separate normal-token set; normal instances appear only in the IFS environment, which "allows the definition of a normal subset of instances" (p.9).
- **Flow over a channel**: "a two-step process: direct image flow along the component structure morphisms of the channel, followed by the meet operation in the lattice of logics over the core" (p.15). Direct image preserves soundness (Prop 1, p.15). Inverse image preserves completeness (Prop 2, p.16).
- **Channel Principle** (p.13): "The regularities of a given distributed system are relative to its analysis in terms of information channels." Quoting B&S Lecture 12: components "will typically be describe[d] in quite different ways with different languages", and "it is natural to think of each of the components as having its own logic" (p.13).
- **Integration** (pp.9-10, 14-15): an "unpopulated" ontology (theory only) is integrated by a colimit of theories; a "populated" one (with structures) by a colimit of logics. Alignment constraints are morphisms in a diagram; e.g. two equivalent types are aligned through one mediating type with two maps back (p.9).
- "Logical environment" is Kent's term for a semantic institution. It is not Seligman's, and Kent does not use the phrase "information environment" (all 16 pages read).

### [Goguen] Goguen 2006, Information Integration in Institutions

Correspondences between channel theory and institutions:
- A B&S classification is a set of tokens, a set of types, and a relation between them; "tokens carry information, and types represent the information that is carried". Classifications "can be considered a primitive kind of ontology" (p.15).
- "the condition on f˅ and f^ is just the institutional Satisfaction Condition" (p.15).
- **Proposition 2** (p.15): "A classification is a 1-institution where Mod(•) is the set of tokens and Sen(•) is the set of types. Moreover, infomorphisms are comorphisms of these institutions." A 1-institution has a single signature, so it is just a triad (p.14).
- **Channel** (Def 12, p.21): "a corelation f_i: A_i -> C for i ∈ I, in the category IFC; C is called the core". B&S's "cover" is a cocone, and their "minimal covers" are colimits in IFC, "although [3] uses the term 'limit' for this concept" (p.21).
- **Local logics** (pp.24-25): a "local classification" is a classification with a subset N of normal tokens (Def 13). B&S local logics are pairs (T, M), with T a regular theory and M a local classification satisfying T on N. They come out as a Grothendieck construction over the theories of the institution IFS (p.25).
- Theorems 3, 6 and 7: the categories of classifications, local classifications and local logics have all limits and colimits (pp.15, 24, 25). "every IF-distributed system has a channel that best describes its flow of information" (p.22). The Xerox principle (transitivity of flow) is a special case (p.23).
- Conclusion: "over any of these institutions, channels are corelations (or cocones), distributed systems are diagrams, and behaviors are colimits" (p.38).
- Why institutions are more general: they allow "information integration over arbitrary logics" and treat cases "in which part of a situation is fixed while another part is allowed to vary, e.g., non-logical symbols can vary, while the logical symbols and rules of deduction are fixed" (p.2).
- B&S "says '... any suggestion that tokens must have something like "syntax" is quite unwelcome'". Goguen disagrees: "such structuring is precisely what is needed for many applications" (p.16, fn 15).

Conclusions carrying across, and where they stop:
- Translations between logics (morphisms and comorphisms) are "truth preserving" (p.11). Integration over a shared part is a colimit, which combines theories "in a way that takes proper account of shared substructures" (p.9, fn 8).
- Optimality is not guaranteed in practice: "in some practical situations, it is not realistic to expect this kind of optimality, because there are multiple feasible solutions, among which trade-offs must be negotiated; in such cases, one should consider pragmatic optimality criteria" (p.22).
- Blends "are *not* determined uniquely up to isomorphism" (houseboat vs boathouse). "it does not seem ... that any single set of optimality criteria can be appropriate for all situations" (p.34). His implemented blending algorithm uses "purely formal" criteria "(since they could not otherwise be implemented)" that measure how far the injections preserve structure (p.35).

Fallible and imperfect information:
- Normal tokens appear only through local classifications and local logics (pp.24-25). The paper says nothing beyond this about pseudo signals or imperfect channels.
- "real data is often too dirty for this to work well, which suggests that new ideas are needed to deal with the complex uncertainties of real world data" (p.19).
- "it seems necessary for theory and tools to cope with the multiple forms of uncertainty inherent in the real world ... Further development of 3/2-categories seems promising in this respect, and perhaps some ideas from fuzzy logic could help" (p.38).

Modelling real, informal systems:
- Stance: "mathematical models are just models, useful to varying extents for various applications" (p.3). Footnote 2 (p.1): the formal entities are not claimed to be "identical with, or ... even fully adequate representations of, information or concepts as actually experienced and used by humans".
- Goguen rejects "the implicit philosophical realism of [3]" (Barwise & Seligman) as taking "too little account of the social and cognitive aspects of information". He also rejects "an implicit Aristotelean view that concepts are given as conjunctions of attribute", which he says is inconsistent with Rosch's results (p.39).
- **Triads and symbol grounding** (p.33): Unified Concept Theory "uses triads to combine a symbolic space (or theory), a geometrical space (or model), and a relation of satisfaction between them for the given context ... Triads give a solution to the symbol grounding problem, because symbols in conceptual spaces can refer to entities in geometrical spaces, which in turn can be identified with real world entities. This way of combining formal models with concrete interpretations works over any concrete institution".
- **Skin-tone colour terms** (Example 6, pp.33-34): skin-tone words mean something different than they do for fabrics. Gärdenfors embeds skin-tone space in the colour manifold, where the standard colour regions are "the closest fits". Goguen treats the colour terms as a theory and their meaning as a triad between that theory and a colour model; the embedding and projection give triad morphisms (pp.33-34). Triad morphisms "are more general" than context morphisms, "as is shown by the skin color example". With only unary predicates and one context, "triad morphisms degenerate to the infomorphisms of [3]" (pp.44-45).
- **Ontology alignment** (Example 7, pp.35-36): English river/stream and French fleuve/rivière classifications of six rivers. "This information is not enough to recover the informal relations between concepts ... but if we can align the objects, a surprising amount of insight can be obtained". The alignment rests on a supplied assumption that corresponding rows have the same properties. "triad pushouts compute the limit (pullback) of models and the colimit of theories with their signatures" (p.36). The concept lattice of the merged triad gives "a canonical formal vocabulary for classifying the given models" (p.36). Mapping tools build correspondences; "this process can be non-trivial", with "partial automation" suggested (p.37).
- "information environment(s)" does not occur in this paper (all 48 pages read).

## Synthesis

Limited to what the three read works support. Where a line combines statements from them, it is marked "(my combination)".

1. **The bridge is a channel, not a single map.** The fuzzy domain and the formalism are each modelled as a classification: tokens (real instances, observed runs, models) and types (what can be said of them). Neither is mapped straight onto the other. Both map out of a third classification, the core, whose tokens are "the specific connection within the channel" relating a token on one side to a token on the other ([MSR] p.339; [Kent] p.10; [Goguen] Def 12, p.21). Building the bridge therefore means choosing what counts as a connection, for example a pairing of an observed run with a model state, and not only choosing an encoding (my combination).
2. **The basic contract is the institutions' satisfaction condition.** Types go forward, tokens go backward, and "f˅(b) ⊨ α iff b ⊨ f^(α)" ([MSR] p.339). This is the institutional satisfaction condition ([Goguen] p.15; [Kent] p.3).
3. **Which conclusions carry, and in which direction** ([Kent] p.12, paraphrasing B&S part I):
   - A constraint that holds of a component carries into the core (validity is preserved).
   - A constraint of the core carries back only to parts that "really are (up to isomorphism)" components.
   - Going from one side through the core to the other side loses the guarantee of both soundness and completeness. The result applies only to tokens that the channel actually connects.
   - [MSR] gives the same thing as a picture: a channel supports A -> B only over the signal-target pairs it links ([MSR] p.331). A token it does not link is a "pseudo signal" (p.332).
   - In terms of logics: direct image preserves soundness and inverse image preserves completeness ([Kent] Props 1-2, pp.15-16).
   - The statements guaranteed to carry across every infomorphism are those of "flow formula" shape ([MSR] p.342, citing van Benthem 2000, not read).
4. **Fallibility is represented, not ignored.** It appears in three ways:
   - The channel may be absent for a given token (pseudo signal; [MSR] pp.331-332).
   - A token may lie outside the normal tokens, so the constraints do not bind it ([MSR] p.337; [Goguen] Def 13, p.24).
   - A logic may be unsound or incomplete relative to its structure ([Kent] p.14).

   For a bug-finding bridge, this gives three distinct reasons a transferred verdict can fail to hold: the run was not connected, the run was abnormal, or the logic was unsound or incomplete (my combination).
5. **A model of a real, informal system is a local logic with a sample-limited token set.**
   - A local logic for a human classifier, or for an observed dynamic system, generally lacks a counterexample token for every unlicensed inference. A regularity seen in the observed tokens "may be a regularity of the sample, not one that is part of the ... classificatory method" ([MSR] pp.337-338).
   - Observation types are "a limited selection of subsets of the state space" ([MSR] p.338).
   - So a formalism inferred from observed runs should keep, apart from each other: constraints the domain imposes; regularities only observed in the sample; and tokens flagged abnormal (my combination of [MSR] pp.337-338).
6. **Choosing the closest formalism**:
   - The read works give a structural criterion: a better channel is a refinement, through which "any information that flows in one channel also flows in the refined channel" ([MSR] p.340). For a given distributed system the colimit is the best channel, unique up to isomorphism ([Kent] p.10; [Goguen] p.22).
   - [Goguen] says this optimality is often unrealistic. When several solutions are feasible, "pragmatic optimality criteria" are needed (p.22), and no single set of criteria fits all situations (p.34).
   - In the colour example, the "closest fits" are regions in a geometric model, not choices of logic (pp.33-34).
   - A measure of closeness between a fuzzy domain and a candidate formalism beyond these points: unknown.
7. **The step from the informal world**: [Goguen] gives the most direct statement in the read works. Triads tie symbols to geometric or concrete models, which "in turn can be identified with real world entities", over any concrete institution (p.33). He also says models are "just models" (p.3), real data is "often too dirty" (p.19), and uncertainty is unsolved (p.38). How a real system's tokens should be chosen and validated: unknown from the read works, except that [MSR] treats choosing a scheme of individuation as context-dependent, "employing only those distinctions that are salient and/or useful" (p.336).

## Relation to the institutions report

- **Agree, same condition.** The institutions report says "The satisfaction condition is the whole contract". Channel theory's infomorphism condition is that same condition: [Goguen] Prop 2 (p.15), [Kent] p.3. A classification is a 1-institution, meaning a single signature with models as tokens and sentences as types ([Goguen] p.15).
- **Agree, same direction.** Infomorphisms are institution *comorphisms* ([Goguen] Prop 2, p.15). This is the direction Hets uses for encoding a source logic into a tool logic (institutions report, Hets p.122). Types/sentences go forward and tokens/models go backward in both.
- **Agree, refutation versus confirmation.** The institutions report found that any comorphism carries refutations back, and confirmation needs model expansion (LPMS; Hets; GB's surjective β). [Kent] states the parallel for structure morphisms: f-Intro preserves validity and f-Elim preserves nonvalidity, and each preserves both only "along structure-isomorphic structure morphisms" (p.12). Whether Kent's isomorphism condition is formally the same as model expansion: unknown. The read works do not relate them.
- **Differ, what is related.** An institution comorphism relates two *logics*. A channel relates particular *systems or instances* through a core whose tokens are connections ([MSR] p.339; [Kent] p.10). The institutions report noted that "Institutions relate formal to formal" and that the first step from the informal domain is outside the theory. Channel theory still needs a formal classification on each side, but its unit is a particular system and its instances. It also has explicit apparatus for imperfect links: pseudo signals, normal tokens, unsound or incomplete logics ([MSR] pp.332, 337; [Kent] p.14). The read institution papers have no such apparatus (my combination of this report and the institutions report).
- **Differ, uniqueness.** Hets routes a goal along a chosen comorphism path, and "the shortest path need not always be the best one" (institutions report). Channel theory has a canonical best channel, the colimit ([Kent] p.10; [Goguen] p.22). [Goguen] then cautions that this optimality is often not realistic (p.22).
- **Connect, generalisation.** [Goguen] and [Kent] both generalise channel theory to any institution. Channels become corelations/cocones, distributed systems become diagrams, behaviours become colimits ([Goguen] p.38). Information flow becomes direct image followed by meet ([Kent] p.15). [Kent] cites Goguen & Burstall for Theorem 1 (p.15). [Goguen] notes that Hets is "based in part on the approach to heterogeneity described in Appendix B", the Grothendieck construction (pp.5-6).
- **Connect, a candidate for the informal node.** The institutions report's only structural idea for the informal step was Hets' "formalism without semantics" node for UML. [Goguen]'s triads offer a different structure: a theory, a concrete or geometric model, and a satisfaction relation "for the given context", with triad morphisms more general than signature morphisms (pp.33, 44-45). Whether triads serve as the bridge from a fuzzy domain in practice: unknown. Goguen's own examples (colour terms, river ontologies) start from already-classified data (pp.33-36).

## Not read

Nothing is stated from these.

- Barwise & Seligman, *Information Flow: The Logic of Distributed Systems*, CUP 1997, Cambridge Tracts in TCS 44, DOI 10.1017/CBO9780511895968. No open copy found. URLs tried:
  - Cambridge Core chapter pages: paywalled.
  - philarchive.org/rec/BARIFT: HTTP 403.
  - Semantic Scholar via `fetch_paper.py`: 404.
  - Unpaywall: refused the placeholder email. I did not send Q's email.
  - Copy at mimuw.edu.pl/~skowron/WM/Logika/ksiazka/part1.pdf: a course page, not an author or publisher copy. Not used.
- Barwise & Seligman, "Imperfect Information Flow", LICS 1993, DOI 10.1109/LICS.1993.287582. Only IEEE and LICS archive pages found, no open PDF.
- Seligman, "Channels: from Logic to Probability", in Sommaruga (ed.), *Formal Theories of Information*, LNCS 5363, 2009, pp. 193-233. Auckland ResearchSpace 2292/13632 is restricted. A university-proxy Springer mirror was seen and not used.
- Barwise & Seligman, "The Rights and Wrongs of Natural Regularity", Phil. Perspectives 8, 1994. No open copy found.
- Barwise 1993, "Constraints, channels and the flow of information"; Moss & Seligman 1994, "Classification Domains and Information Links"; Seligman 1990, "Perspectives in Situation Theory"; Seligman & Moss 2010, "Situation Theory" (Handbook). Not searched for copies.
- Kent, "System Consequence", arXiv 1810.02929; Kent, "Semantic Integration in the IFF", arXiv 1810.08236 / 1109.0032; IFF metatheory arXiv 1108.4133. Open on arXiv, not read (limit of 4 works; Kent 2016 chosen as the most direct).
- Goguen, "Data, schema, ontology and logic integration", Logic J. IGPL 13, 2005.
- Kalfoglou & Schorlemmer 2002, "Information-flow-based ontology mapping".
- Schorlemmer & Kalfoglou 2004, "A channel-theoretic foundation for ontology coordination".
- van Benthem 2000, "Information transfer across Chu spaces" (source of the flow-formula result quoted in [MSR]).
- Restall 2005, "Logics, situations and channels" (consequently.org/writing/channels/).
- arXiv 2206.02283, "Situation Theory and Channel theory as a Unified Framework for Imperfect Information Management". Search hit, not read.

## Open questions

- **What "information environments" refers to: not found.** I searched for `Seligman "information environments" channel theory`, `"Jerry Seligman" "information environment"`, and an extended search for Seligman titles containing "environments". I also checked Seligman's CV (publications to 2010). None joins Seligman to the phrase, and it does not occur in the three works read. The phrase in search results belongs to information-foraging and information-architecture writing (Pirolli), unrelated to Seligman. The nearest named framework is Kent's "logical environments" (a semantic institution carrying Barwise-Seligman information flow, [Kent] p.6). I do not know whether Q meant that, a Seligman talk or paper after 2010 not on the CV, or something else. Q is the one who can say.
- Whether Kent's "structure-isomorphic" condition for f-Elim ([Kent] p.12) coincides with the model-expansion condition in the institutions report: unknown.
- The B&S book's own treatment of imperfect flow, and of modelling real systems (its applications chapters): unknown, not read.
- Seligman 2009's probabilistic local logics, referred to by [MSR] p.338 fn 7: unknown, not read.
- Whether any of the applied channel-theory work (Kalfoglou & Schorlemmer) gives a procedure for building the core from real data: unknown, not read.
