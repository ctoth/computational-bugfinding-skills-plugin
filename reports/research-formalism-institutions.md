# Research: institutions, morphisms, and borrowing verification tools

## Question

Q (2026-11-07): "finding the closest formalism is gonna be important. goguen institutions morphisms blah blah blah". What does the literature on Goguen and Burstall's institutions, institution morphisms/comorphisms, heterogeneous specification (Hets/CASL), theory morphisms ("little theories") and borrowing proof tools across logics say about relating a domain to an existing formalism and reusing that formalism's verification tools?

## Search log

Collection check: `C:/Users/Q/code/papers/index.md` grepped for institution, goguen, burstall, comorphism, hets, casl, little theor, cerioli, meseguer, mossakowski, borrow, farmer: no hits. Nothing to dedupe.

1. WebSearch `Goguen Burstall "Institutions: abstract model theory for specification and programming" pdf` -> JACM 39(1):95-146, 1992, DOI 10.1145/147508.147524; PDF at courses.grainger.illinois.edu/cs522/sp2016/InstitutionsAbstractModelTheory.pdf; LFCS report ECS-LFCS-90-106.
2. WebSearch `Cerioli Meseguer "May I borrow your logic?"` -> TCS 173(2):311-347, 1997, DOI 10.1016/S0304-3975(96)00160-0; MFCS 1993 version LNCS 711.
3. WebSearch `Mossakowski Maeder Lüttich "The Heterogeneous Tool Set"` -> VERIFY 2007, CEUR Vol-259 paper11 (ceur-ws.org/Vol-259/paper11.pdf); TACAS 2007 version DOI 10.1007/978-3-540-71209-1_40.
4. WebSearch `Goguen Rosu "Institution morphisms" Formal Aspects of Computing 2002` -> FAC 13(3-5):274-307, DOI 10.1007/s001650200013.
5. WebSearch `Farmer Guttman Thayer "Little theories" CADE 1992` -> CADE-11 LNCS 607 pp. 567-581, DOI 10.1007/3-540-55602-8_192 (paywalled); related free: IMPS system description (imps.mcmaster.ca/doc/cade-11-sys-desc.pdf), IMPS JAR 1993.
6. WebSearch `Mossakowski "heterogeneous specification" Hets case study translation to Isabelle comorphism` -> candidates: HetCASL summary (uni-bremen), Alloy-in-Hets paper (core.ac.uk/download/55634086.pdf, translation of Alloy to second-order logic for LEO-II/Isabelle, medical-domain case study), Maude-in-Hets (DFKI 4796_main.pdf), Mossakowski habilitation 2005.

7. WebSearch `Alloy Hets institution comorphism second-order logic Isabelle LEO-II` -> Neves, Madeira, Martins, Barbosa 2014, "An institution for Alloy and its translation to second-order logic", DOI 10.1007/978-3-319-04717-1_3; repositorium.uminho.pt handle 1822/34744; repositorio.inesctec.pt item. Also Codescu et al. 2012 "logical frameworks + Hets" (cs.cornell.edu/~ks858/papers/logical_frameworks_hets.pdf).

Retrieval: Goguen & Burstall from the Illinois course copy (52 pp, title page checked at reading). Hets from CEUR (17 pp). paper-retriever fetch_paper.py returned fallback_needed for Goguen & Rosu, Cerioli & Meseguer, Little theories; fsl.cs.illinois.edu guess URL returned HTML, Cerioli's department page refused connection.

8. Sci-hub route for Goguen & Rosu: the browser call was DENIED by the permission classifier ("Walled Content from a Copy"). I did not work around it. ScienceDirect page for Cerioli & Meseguer showed a bot check ("Just a moment..."), which I did not bypass; author FTP path ftp.disi.unige.it/person/CerioliM/TCS96.ps.gz returned nothing. A university-proxy Springer mirror (springerlink.bibliotecabuap.elogim.com) showed up in searches; I did not use it (walled copy).
9. WebSearch `"Institution morphisms" Goguen Rosu preprint ... "comorphism"` -> found arXiv 2206.07180, Lopez Pombo & Martinez Suñé, "Integrating deduction and model finding in a language independent setting" (2022): satisfiability calculi (model finding) combined with proof calculi in the institutions/general-logics setting. Retrieved (30 pp). Relevant to bug finding (counterexamples vs proofs), so added.
10. Neves et al. 2014 retrieved from repositorium.uminho.pt bitstream (author repository).

Selection (by relevance to "relate a domain to an existing formalism and reuse its tools"): (a) Goguen & Burstall 1992 (foundational definitions); (b) Goguen & Rosu 2002 (morphism vs comorphism); (c) Cerioli & Meseguer 1997 (borrowing a missing proof theory and its tools); (d) Mossakowski, Maeder & Lüttich 2007 (Hets, tool architecture over comorphisms); (e) Alloy-in-Hets (concrete application: connecting a domain language to existing provers); (f) Farmer, Guttman & Thayer 1992 Little theories, if retrievable.

## Papers read

All four were read through the research-papers `paper-reader` skill from page images, every page, one reader per paper. Each paper's notes are in its directory under `C:/Users/Q/code/papers/`. I checked two load-bearing passages myself against the page images: GB p.126 (Def 34, Prop 35) and LPMS p.27 (Def 20, Thm 1).

- **[GB]** Goguen & Burstall, "Institutions: Abstract Model Theory for Specification and Programming", JACM 39(1):95-146, 1992. `Goguen_1992_InstitutionsAbstractModelTheory/`. Pages cited are the printed ones.
- **[Hets]** Mossakowski, Maeder & Lüttich, "The Heterogeneous Tool Set", VERIFY 2007, CEUR-WS Vol-259, pp. 119-135. `Mossakowski_2007_HeterogeneousToolSetHets/`. Pages cited are the printed ones.
- **[Alloy]** Neves, Madeira, Martins & Barbosa, "An institution for Alloy and its translation to second-order logic", 2014, DOI 10.1007/978-3-319-04717-1_3. `Neves_2014_InstitutionForAlloySecondOrderLogic/`. Pages cited are PDF pages, because the images carry no printed numbers. The venue is not shown on the copy I read.
- **[LPMS]** Lopez Pombo & Martinez Suñé, "Integrating deduction and model finding in a language independent setting", arXiv 2206.07180, 2022. `Pombo_2022_IntegratingDeductionModelFinding/`. Pages cited are PDF pages, with page-000 counted as p.1.

## Findings

### Definitions

- **Institution [GB Def 1, pp.101-102].** An institution has a category Sign of signatures, a functor Sen: Sign -> Set, a functor Mod: Sign -> Cat^op, and a satisfaction relation ⊨_Σ for each signature. The **satisfaction condition** must hold for every signature morphism φ: Σ -> Σ': m' ⊨_Σ' Sen(φ)(e) iff Mod(φ)(m') ⊨_Σ e. [Hets p.121] phrases it as "truth is invariant under change of notation (or enlargement of context)". The same page says that structuring, modules, refinement and proof calculi can be built independently of the logic, because "all that is needed is captured by the satisfaction condition".
- **Institution morphism, GB direction [GB Def 32, p.125].** A morphism I -> I' has three parts:
  - Φ: Sign -> Sign', mapping signatures forward;
  - α: Φ;Sen' ⇒ Sen, mapping sentences backward from I' to I;
  - β: Mod ⇒ Φ^op;Mod', mapping models forward.

  It must satisfy m ⊨_Σ α_Σ(e') iff β_Σ(m) ⊨'_Φ(Σ) e'. On p.110, GB say the direction was kept "for essentially historical reasons". [GB] contains no comorphism notion.
- **Comorphism, as used in Hets [Hets p.122].** A comorphism (Φ, α, β): I -> J has three parts:
  - Φ maps signatures from I to J;
  - α_Σ maps Σ-sentences forward to Φ(Σ)-sentences;
  - β_Σ maps Φ(Σ)-models of J backward to Σ-models of I.

  It must satisfy M' ⊨_J α_Σ(φ) iff β_Σ(M') ⊨_I φ. This is the direction used for encoding a source logic into a target logic that has tools. The duality between morphism and comorphism is the subject of Goguen & Rosu 2002, which I did not read (see "Not read").

### How one logic's tools serve another, and when conclusions transfer

- **GB's soundness condition for borrowing a prover [GB Def 34 and Prop 35, p.126; checked by me].** A morphism is *sound* iff each β_Σ is surjective on objects. When it is, a sentence e' follows from E' in I' iff α_Σ(e') follows from α_Σ(E') in I. So entailment is both preserved and reflected. GB's example: the sound morphism FOEQ -> EQ means "a theorem prover for first-order logic with equality can be used for equational theories".
- **Hets' condition for borrowing [Hets pp.131-132].** If the comorphisms are *model-expansive*, then (Σ,Γ) ⊨_I φ iff (Φ(Σ), α(Γ)) ⊨_J α_Σ(φ), and "borrowing of entailment systems along the composite comorphism ... is sound and complete". Hets **assumes** every comorphism is model-expansive (p.131). Proving the comorphisms correct, for example in Twelf, is listed as future work (p.133). The exact definition of model-expansive is not in this paper; it cites refs [7, 27].
- **Hets mechanics.**
  - Each logic is an instance of a Haskell `Logic` type class, which provides parsers, static analysis, sentence translation and provers (pp.123-124).
  - The logic graph is flattened into a Grothendieck institution (pp.122, 128).
  - Development graphs reduce proof obligations to local goals (p.128).
  - On "Prove", the theory and goals go to a prover's logic along the shortest comorphism path, but "the shortest path need not always be the best one", so the user can choose the path (p.131).
  - Only three logics have their own provers: Propositional (zChaff), SoftFOL (SPASS, Vampire, MathServ) and Isabelle. Every other logic gets proof support only through translations (p.125).
  - Case study: in checking the RCC8 composition table, SPASS proved the 95 first-order goals and Isabelle proved the 4 higher-order bridge lemmas (pp.129, 132).
- **Counterexamples transfer one way; proofs need more [LPMS].**
  - For any comorphism, consequence is preserved (Prop 3, pp.25-26). A model found in the target logic for the translated Γ ∪ {¬α} therefore shows that α has no proof from Γ in the source logic (Coro 6, p.26).
  - The paper states that failing to find a counterexample "does not provide any solid information" about whether a proof exists (p.27; checked by me).
  - Consequence is reflected back only under the **ρ-expansion property** (Def 20, p.27): every source model is the β-image of some target model. Theorem 1 (p.27, citing [44]) gives Γ ⊨ φ iff ρ(Γ) ⊨' ρ(φ). With that property, an effective model finder for the target becomes a semantics-based decision procedure for the source (p.27).
  - Worked case, first-order logic to propositional logic (pp.28-32): existentials are encoded as n-way disjunctions over fresh constants. This is a theoroidal comorphism for every bound n (Prop 9), which gives bounded counterexample search. Per the reader's notes, the paper does not say whether models larger than n expand, so reflection is not claimed for this case.
- **Concrete domain-to-prover application [Alloy].**
  - Alloy is cast as an institution (pp.7-11). Signatures carry kinds and their "extends" parents, typed relations and variables. Theorem 1 proves the satisfaction condition.
  - The comorphism goes to second-order logic presentations (pp.12-14). Six axiom schemes encode Alloy's implicit rules about kinds. Transitive closure is encoded as a least closed relation. Theorem 2 is the satisfaction condition, proved in Appendix A.3-A.5 (pp.24-30). Theorem 3 gives conservativity, which the paper defines as model expansion (p.5).
  - The paper says conservativity is what lets one "borrow" proof support soundly (p.6).
  - The case study uses only the earlier translation to CASL, which is first-order (pp.18-20). SPASS proves a DCR-graph property. A false property in a medical workflow is out of the Alloy Analyzer's reach below scope 15, but Vampire refutes it in seconds. The new second-order route is proved but not run on any prover in the paper.
  - The paper calls the second-order embedding "more natural" and keeps CASL because it reaches first-order provers (p.2). The CASL translation handles transitive closure only of atomic relations (pp.14-16).
- **Structuring transfers under extra conditions [GB].** Theories can be combined whenever their signatures can (Thm 11, p.108). If a morphism is "cordial" (Φ has a cocontinuous left inverse), the induced theory map preserves structuring (Thm 39, p.127). Entailment is preserved along signature morphisms but not reflected in general (Closure Lemma, p.105).

### Stated limits

- [GB pp.102, 119, 132]: the paper "has said little about proofs"; checking the satisfaction condition is "tedious"; data constraints have no complete deduction rules.
- [Hets p.131, p.133]: soundness and completeness of borrowing rest on an unproved assumption that the comorphisms are model-expansive.
- [Alloy pp.16, 19, 21]: models that use transitive closure heavily needed an interactive prover, and "more experimental work" is needed. Whether its second-order logic uses standard or Henkin semantics is not addressed.
- [LPMS p.27]: model finding through a comorphism without the expansion property can refute but never confirm.

### Practical synthesis: picking and justifying "the closest formalism"

How the read papers support doing it:

1. Write the domain as an institution: what a signature is, what a sentence or property is, what a model or behaviour is, and when a model satisfies a sentence. Prove the satisfaction condition. This is what [Alloy] does for Alloy (pp.7-11).
2. For each candidate target logic that has tools, write a comorphism into it and prove its satisfaction condition ([Hets p.122]; [Alloy] Thm 2).
3. Classify what each translation licenses:
   - Any comorphism: a target counterexample refutes the source claim [LPMS Coro 6, p.26].
   - Model expansion, called model-expansive in [Hets], ρ-expansion in [LPMS] and conservativity in [Alloy]: in addition, a target proof establishes the source claim, so the target's tools become a sound and complete stand-in ([Hets pp.131-132]; [LPMS Thm 1, p.27]; [GB Prop 35, p.126], in GB's own direction).
4. Under this reading, "closest" means the target tool reaches through a translation with the strongest transfer guarantee that is still proved. Among targets with equal guarantees, the tradeoff is between a natural encoding and tool strength: [Alloy] keeps a less natural first-order target because it has better provers (p.2), and [Hets] lets the user override the shortest path (p.131). That ranking is my synthesis from these papers; none of them states it as a method.
5. For bug finding in particular, [LPMS] says counterexample search alone needs only a comorphism. Claims of absence of bugs need the expansion property.

What it does not give you:

- No procedure for discovering the target or the encoding. Every paper starts from a translation someone has already designed.
- No measure of "closeness" beyond whether these properties hold or fail.
- Proofs are by hand and "tedious" [GB p.119]. Hets runs on assumed, unproved model-expansiveness [Hets p.131].
- Nothing on performance or decidability of the translated problem, except that [Alloy] reports some prover outcomes and [LPMS] says its effective subcalculi ensure decidability (p.18).
- Nothing on domains that have no logic-like presentation, such as raw program behaviour, unless someone first builds that institution. Unknown from the read papers.

## Reframe (team-lead, relaying Q, 2026-11-07)

Institutions are an example, not the scope. Q's question: "we have a fuzzy world, then we have formalisms. we are building one possible bridge, which will tell us how to build bridges." Below I re-read the four papers as a theory of bridges. Every passage cited in this section was checked by me against the page image unless marked "(reader notes)":
- GB pp.96, 126
- Hets p.120
- Alloy PDF pp.18, 20
- LPMS PDF pp.5, 27, 28

### What must be preserved for a conclusion to cross

- **The satisfaction condition is the whole contract.** A bridge maps three things: vocabularies (Φ), statements (α) and models (β). For every statement and model, "model satisfies translated statement" must hold exactly when "translated model satisfies statement" does [Hets p.122; GB Def 32, p.125 (reader notes)]. Nothing else is required of the two sides: Hets p.121 says that structuring and proof calculi need only "what is captured by the satisfaction condition" (reader notes).
- **Why anyone builds the bridge [GB p.96, checked].** GB give the motive as tool reuse: "because of the proliferation of logics ... plus the great expense of implementing tools like theorem provers and compilers, it is useful to know when sentences in one logic can be translated into sentences in another logic in such a way that soundness is preserved". The stated payoff is "using a theorem prover for one logic on (translations of) sentences from another logic".

### What a translation is allowed to lose

- **Expressivity, under conditions [LPMS p.28, checked].** The authors call it "misleading" to think the source of a comorphism must be less expressive than the target. Comorphisms are "encodings" that "might loose expressivity / representation capability" while still satisfying the satisfaction condition. Their bounded FOL -> propositional translation is an example (Prop 9, pp.28-32, reader notes). The conditions under which such lossy comorphisms exist are "left for further investigation" (p.28).
- **Model coverage, at the price of one-way verdicts.** A bridge can satisfy the satisfaction condition while some source models have no counterpart in the target. In that case only refutations come back, not confirmations [LPMS p.27, checked; Prop 3 and Coro 6, pp.25-26 (reader notes)].
- **Naturalness, traded for tool strength.** [Alloy] proves a "more natural" second-order translation but keeps the first-order CASL route because it reaches first-order provers (p.2, reader notes). Its case study runs only the CASL route (pp.18-20, reader notes).
- **Distinctions the source does not make must not be collapsed.** [Hets p.120, checked] keeps both theory morphisms and logic comorphisms as "first-class citizens". So Hets "can also distinguish conjunction in Isabelle/HOL from conjunction in PVS (these actually have two different semantics!)" and relate the two logics with a comorphism.

### How a verdict legitimately comes back

- **Counterexample in the target means the claim is false in the source**, for any comorphism, because consequence is preserved [LPMS Coro 6, p.26 (reader notes)].
- **Proof in the target means the claim holds in the source** only when every source model is the image of some target model. This condition is called model-expansive in [Hets pp.131-132], ρ-expansion in [LPMS Def 20 and Thm 1, p.27, checked], "sound morphism" (β surjective) in [GB Def 34 and Prop 35, p.126, checked], and conservativity in [Alloy Thm 3, p.5 and p.13 (reader notes)].
- **No counterexample found means nothing.** "not being able to do so does not provide any solid information about its existence" [LPMS p.27, checked]. [Alloy PDF p.18, checked] gives the domain version: Alloy "may give a false sense of security as the scope set for a simulation session may not be wide enough to produce a counter example". A property that holds under small scopes is refuted by Vampire through the bridge (pp.18-20, reader notes).
- **The condition is often assumed rather than proved.** Hets assumes every comorphism is model-expansive (p.131, reader notes).

### Where this theory stops: the first step from the informal domain

Institutions relate formal to formal. Here is what the four read papers say about getting from an informal domain to the first formalism:

- [GB p.96, checked] lists "natural language" among the problems that exotic logics "have been proposed to handle". That is a statement about logics, not about the step from informal to formal. Nothing else in my checks or in the reader notes of [GB] addresses that step.
- [Hets p.120, checked] is the only passage that touches it structurally. UML "deliberately has no formal semantics, and hence is not a formal method or logic". It "could be integrated ... as a formalism without semantics, while the different formal semantics that have been developed for UML would be represented as logic translations". So an informal or semi-formal language could sit in the graph as a node, and *each candidate meaning* of it becomes a separate translation into a logic. The paper does not develop this further.
- [Alloy PDF p.20, checked] describes its contribution as "the first steps toward establishing a rigorous methodology for modelling and validating software designs by connecting Alloy to a network of logics". It starts from Alloy models, not from the domain.
  - The medical workflow is taken already formalised as a DCR graph "as introduced in [16]" (PDF p.18, checked).
  - Properties are given in English beside the Alloy text ("In English it reads: ...", p.18). The paper does not check the English against the Alloy; the two simply sit side by side.
  - The same page notes the cost to people: the institutional framework is "a notational burden the working software engineer may find hard to bear", paid "once and for all".
- [LPMS PDF p.5, checked] frames the choice between lightweight methods (Alloy, which "cannot usually be entirely trusted when dealing with models of mission critical systems") and heavyweight provers (which "require a high level of expertise"). It is about choosing the formal tool, not about how to formalise.
- **Verdict.** In the read papers, the first step from informal to formal is outside the theory. No read paper gives a criterion for when a formalisation is faithful to an informal domain. The closest they come is the Hets UML remark: keep the informal artefact as a semantics-free node and represent each candidate formal meaning as an explicit translation.

## Synthesis: what this teaches about building bridges

Restricted to what the read papers support. Where a line is my combination of their statements, it is marked as such.

1. **A bridge maps three things: vocabulary, statements and models.** It is correct when satisfaction agrees on both sides of the map [Hets p.122; GB p.125]. A bridge that translates only statements, such as a syntactic encoding into a solver's input, has no correctness criterion in this theory until a model map β is also stated.
2. **Decide in advance which verdicts the bridge must carry back.**
   - Refutation (a counterexample or bug) needs only the satisfaction condition [LPMS p.26].
   - Confirmation (a proof or "no bug") needs every source model to be reached by a target model [LPMS p.27; Hets pp.131-132; GB p.126].
   - "Searched and found nothing" carries nothing back unless the search is complete for the translated problem [LPMS p.27; Alloy p.18].
3. **A bridge may lose expressivity and naturalness and stay sound for the verdicts it claims** [LPMS p.28; Alloy p.2]. Losing model coverage downgrades it to a refutation-only bridge (my combination of LPMS pp.27-28).
4. **The bridge itself carries proof obligations.** The satisfaction-condition proofs are "tedious" [GB p.119, reader notes] and run to appendix length [Alloy Appendix A, pp.24-30, reader notes]. In the one working tool, the expansion property is assumed rather than proved [Hets p.131].
5. **Keep several bridges and keep them distinct.** Hets keeps theory morphisms and comorphisms as first-class objects. It routes each goal along a chosen path rather than a fixed hub logic, and criticises single-hub integration such as PROSPER, where "the user is forced to use this central logic" [Hets p.120]. The shortest path "need not always be the best one" [Hets p.131].
6. **The first bridge, from the fuzzy world to a formalism, is not covered.** The only structural suggestion in the read papers is to represent the informal artefact as a node without semantics, with its candidate meanings as separate translations [Hets p.120]. Whether that idea extends to a fuzzy domain rather than a semi-formal notation like UML is unknown from the read papers.

## Not read

No claims are made from these.

- Goguen & Rosu, "Institution Morphisms", Formal Aspects of Computing 13:274-307, 2002, DOI 10.1007/s001650200013. Not retrieved: open-access fetch failed, and the sci-hub browser call was denied by the permission classifier.
- Cerioli & Meseguer, "May I Borrow Your Logic? (Transporting Logical Structures Along Maps)", TCS 173(2):311-347, 1997, DOI 10.1016/S0304-3975(96)00160-0. Not retrieved: ScienceDirect showed a bot check and the author's FTP path was dead. Q may be able to fetch it, since TCS is in Elsevier's open archive (unverified).
- Farmer, Guttman & Thayer, "Little Theories", CADE-11, LNCS 607, pp. 567-581, 1992, DOI 10.1007/3-540-55602-8_192. Paywalled; not retrieved.
- Meseguer, "General Logics", 1989. Not searched further.
- Tarlecki on heterogeneous specification. Cited by LPMS as the source of Prop 3; not retrieved.
- Mossakowski's 2005 habilitation thesis, cited by Hets for the development-graph calculus and model-expansiveness.
- Codescu et al. 2012, logical frameworks plus Hets (cs.cornell.edu/~ks858/papers/logical_frameworks_hets.pdf).
- IMPS papers (imps.mcmaster.ca).
- Maude-in-Hets (DFKI 4796_main.pdf).
- HetCASL summary.

## Open questions

- Exact definition of model-expansive and the proof that it gives sound and complete borrowing: Hets refs [7, 27], not read.
- Which Hets comorphisms are actually model-expansive: not stated in [Hets] (p.131 assumes all are).
- How the GB-direction "sound morphism" (surjective β, p.126) relates formally to the comorphism-direction expansion property: duality per Goguen & Rosu 2002, not read.
- Whether the read papers' notion of "closest" can be applied when the domain is program behaviour rather than a specification language: unknown.
- The informal-to-formal step: none of the four read papers covers it. The literature on that step (requirements formalisation, validation of formal models against domains) was not searched in this pass, so its content is unknown here.
- Papers dir housekeeping not done: reconcile and `keymap.tsv` rebuild were skipped for all four papers to avoid concurrent edits to shared collection files.
