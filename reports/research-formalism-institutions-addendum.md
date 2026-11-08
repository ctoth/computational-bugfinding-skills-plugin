# Addendum: institutions papers not read in the first pass

Scope: retrieve (open access only) and read with `paper-reader` three papers missing from `reports/research-formalism-institutions.md`: Goguen & Roșu 2002 "Institution Morphisms"; Cerioli & Meseguer 1997 "May I Borrow Your Logic?"; Farmer, Guttman & Thayer 1992 "Little Theories".

## Retrieval log

Collection check: `C:/Users/Q/code/papers/index.md` grepped for "institution morphism", "borrow your logic", "little theories", Cerioli, Guttman: only hit is the Goguen & Burstall 1992 entry. No other `*/papers/` copy searched exhaustively (a recursive metadata.json grep over C:/Users/Q/code timed out after 20 s); the root collection had none.

paper-retriever `fetch_paper.py` (open-access waterfall: direct, Unpaywall) run on all three DOIs from `C:/Users/Q/code`: `fallback_needed: true` for each. Option 1 (sci-hub / institutional) skipped by instruction. Option 2 (open repositories by title) results below.

- Goguen & Roșu 2002:
  - https://fsl.cs.illinois.edu/publications/goguen-rosu-2002-fac.pdf, `...-2002-fac.html`, `...-2002-fac`, `...-2001-fac.pdf`: HTTP 404 (guessed URLs). https://fsl.cs.illinois.edu/publications/ : 404.
  - Unpaywall API for 10.1007/s001650200013: `is_oa: false`, no locations.
  - https://cseweb.ucsd.edu/~goguen/projs/inst.html (Goguen's UCSD institutions page) links "Institution Morphisms" to `../pps/rodfest.ps`. Downloaded https://cseweb.ucsd.edu/~goguen/pps/rodfest.ps : HTTP 200, application/postscript, 860549 bytes. Converted with Ghostscript (`-dSAFER`, pdfwrite) to `C:/Users/Q/code/papers/Goguen_2002_InstitutionMorphisms/paper.pdf`, 36 pages. Whether this is the FAC version or a preprint is checked at reading.
  - Not used: springerlink.bibliotecabuap.elogim.com (university proxy mirror, walled copy).
- Cerioli & Meseguer 1997:
  - Unpaywall: `is_oa: true`, single location https://www.sciencedirect.com/science/article/pii/S0304397596001600/pdf (publisher, Elsevier open archive). curl to it: no response within timeout (HTTP 000); the earlier pass saw a bot-check page there. Not bypassed.
  - https://person.dibris.unige.it/cerioli-maura/TCS96.html (author page): HTTPS connection refused (ECONNREFUSED 130.251.1.28:443); HTTP timed out.
  - Wayback availability API for the author page and the old ftp/disi .ps.gz paths: HTTP 429 Too Many Requests.
  - WebSearch for CiteSeerX / ps.gz / SRI report copies: none found.
- Farmer, Guttman & Thayer 1992:
  - https://imps.mcmaster.ca/doc/major-imps-papers.html (IMPS project site, McMaster) links `little-theories.pdf`. Downloaded https://imps.mcmaster.ca/doc/little-theories.pdf : 220103 bytes, PDF 1.2, 6 pages, to `C:/Users/Q/code/papers/Farmer_1992_LittleTheories/paper.pdf`. 6 pages versus the LNCS 15 (pp. 567-581): layout checked at reading.

## Papers read

- **[LT]** Farmer, Guttman & Thayer, "Little Theories", CADE-11, LNCS 607, pp. 567-581, 1992. Read every page (19 page images) with `paper-reader` from the authors' copy dated 15 October 1992 (IMPS site). Pages cited are that copy's printed pages 1-19, not the LNCS pages. Notes: `C:/Users/Q/code/papers/Farmer_1992_LittleTheories/notes.md`.
- **[GR]** Goguen & Roșu, "Institution Morphisms", Formal Aspects of Computing 13:274-307, 2002. Read every page (36 page images) with `paper-reader` from the authors' preprint marked "To appear in Formal Aspects of Computing" (Goguen's UCSD page). Pages cited are the preprint's printed pages 1-36, not the journal pages; the preprint cites [Mos03], so it is a late revision, but differences from the journal text are unknown. Notes: `C:/Users/Q/code/papers/Goguen_2002_InstitutionMorphisms/notes.md`.

## Findings

### [GR] Institution Morphisms

(a) What a translation must preserve.
- Morphism (GB direction): Φ: Sign -> Sign′, β: Mod ⇒ Φ;Mod′ (models forward), α: Φ;Sen′ ⇒ Sen (sentences backward), with m ⊨_Σ α_Σ(f′) iff β_Σ(m) ⊨′_Φ(Σ) f′ [GR Def 4.1, p.11].
- Comorphism (Meseguer's "plain map", Tarlecki's "representation"): α: Sen ⇒ Φ;Sen′ (sentences forward), β: Φ;Mod′ ⇒ Mod (models backward), with β_Σ(m′) ⊨_Σ f iff m′ ⊨′_Φ(Σ) α_Σ(f) [GR Def 4.2, p.11]. This confirms the comorphism definition the main report took from [Hets p.122].
- Duality: INS ≅ Dgm(Trel) and coINS ≅ coDgm(Trel) [GR Thm 4.6, p.14]; if Φ has a left adjoint Φ′, morphisms ⟨Φ, μ⟩: I -> I′ are in natural bijection with comorphisms ⟨Φ′, μ′⟩: I′ -> I [GR Thm 4.11, p.15, after Arrais-Fiadeiro]. The bijection can fail even with adjoint signature functors (Ex 4.5 pair) [GR Ex 4.12, p.16].
- Other variants: theoroidal (signatures to theories; Meseguer's maps are theoroidal comorphisms) [GR Def 5.3, pp.16-17]; checking reduces to empty theories [GR Props 5.4-5.5, p.17]; simple theoroidal (signature to theory) [GR Def 5.7, p.18]; forward (syntax and semantics both forward; "a backward morphism is just a forward comorphism") [GR Def 6.1, p.20]; semi-natural (β only a family, not natural), useful because the free superextension "preserves information about why functions are undefined" [GR Def 7.1, Ex 7.2, pp.20-21].

(b) When a verdict legitimately transfers back.
- Borrowing theorem restated: "Given an institution morphism (Φ, β, α): I -> I′ such that β_Σ is surjective on objects for all Σ ... f′ ∈ F′• iff α_Σ(f′) ∈ α_Σ(F′)•" [GR Thm 4.4, p.12], = [GB] Prop 35, p.126. Purpose stated: "to support the re-use of a theorem prover for an institution I on a problem 'f′ ∈ F′•' in another institution I′ by translating it from I′ to I" [GR p.12].
- Conservativity for theory morphisms: φ is conservative "iff for any (Σ, F)-model m there is some (Σ′, F′)-model m′ such that m′↾φ = m" [GR Def 3.6, p.9]; then "F ⊨_Σ f iff φ(F) ⊨_Σ′ φ(f)", while without it only "F ⊨_Σ f implies φ(F) ⊨_Σ′ φ(f)" [GR Prop 3.7, p.9]. Same shape as the model-expansion condition in the main report (every source model is hit), here for theory morphisms inside one institution.
- For comorphisms, closure is preserved: α_Σ(F•) ⊆ α_Σ(F)• [GR Prop 5.8, p.19], i.e. source consequences map to target consequences.
- The paper credits Cerioli-Meseguer with "a borrowing theorem for comorphisms" and says "almost any notion of institution morphism will support some kind of borrowing theorem", but declares borrowing "not a major concern of the present paper" and lists "To what extent do the various morphisms support the borrowing of logics and theorem provers" as open [GR pp.12, 22]. So [GR] gives no comorphism borrowing condition of its own.
- Worked warning [GR Ex 5.9, p.19], FOLE -> FOL (to borrow a first-order prover for logic with equality):
  - The plain morphism treating "=" as a predicate "fails to capture the familiar trick of axiomatizing equality ... as is needed to borrow a first order theorem prover."
  - Adding equality axioms as a simple theoroidal morphism: "the satisfaction condition holds no matter what axioms we give, including none at all — unless some of them are wrong!"
  - As a comorphism with quotienting, "it is impossible to guarantee that '=' will be interpreted as identity."
  - A forgetful theoroidal morphism FOL^= -> FOLE works "by restricting the class of signatures to those where the borrowing makes sense", and "Theorem 4.4 now allows us to borrow a FOL theorem prover."
  - Moral: "morphisms may not encapsulate all the information we need ... we must be very careful in choosing morphisms, and of course also comorphisms."
  - So the satisfaction condition alone does not make a map useful for borrowing; which map is chosen decides whether the verdict can come back.

(c) Choosing or building the target. [GR] has no method for choosing a target logic. It argues for a style: "it is very often better to work with forgetful functors than with functors going the other way, even if they are adjoint" [GR p.11]; "In many cases, institution morphisms in the original sense [GB92] provide more natural formulations ... especially true when the institution morphism is forgetful" [GR p.22]; for borrowing, "it is nice to have the signature and sentence translations go in the same direction" (a comorphism property) [GR p.19]. Motive for many logics: "different logics are used for different aspects, including functional requirements, safety and liveness properties, concurrency control, real time response, data type design, and architectural structure" [GR p.21].

(d) The first step from an informal domain. Nothing in [GR] addresses it. The closest item is the hidden-algebra appendix, where a system is a "blackbox" observed only through experiments and two states are equivalent "iff they cannot be distinguished by any experiment" [GR pp.28-29]; that is a formal logic of observation, not a step from informal to formal.


### [LT] Little Theories

(a) What a translation must preserve.
- A theory interpretation is "a syntactic translation between the languages of two theories which preserves theorems"; to establish one, "one must show that the source theory *axioms* are translated to target theory theorems, together with some additional obligations that depend on the details of the logical context" [LT pp.2-3].
- In IMPS/LUTINS a translation is a pair (μ, ν) mapping sorts to sorts, sets or unary predicates and constants to expressions, extended homomorphically, with binders relativized when a sort becomes a predicate. "By the Interpretation Theorem for LUTINS [8], if each obligation of I is a theorem of T′, then I translates each theorem of T to a theorem of T′" [LT p.7, fn 4].
- Model side: "given an arbitrary model of T′, the interpretation tells us how to select a subdomain and distinguished values that furnish a model of T" [LT p.3]. Models go from target to source, as in a comorphism's β; [LT] does not use institution vocabulary, so that alignment is my reading.

(b) When a verdict transfers back.
- Direction stated: theorems go source -> target [LT pp.2, 7]. Second use: "To establish the consistency of the source theory relative to the target theory" [LT p.3]; "An interpretation I from T to T′ will allow us to assure ourselves that a theory T is consistent, if T′ is a well-established theory trusted to be consistent" [LT p.13].
- [LT] gives no condition under which a T′-theorem about translated sentences comes back as a T-theorem (no conservativity/expansion notion in this paper).
- Prover components transfer under checked presuppositions: a simplification/decision "processor" is "often sound for a range of theories, so long as they satisfy a number of presuppositions ... The simplifier for that theory can soundly call the processor if these presuppositions are theorems" [LT p.11].
- Context theory interpretations: a translation whose axiom images hold only under local assumptions {φ1..φn} is used "so long as our position in a proof licenses us to use the assumptions" [LT pp.12-13].

(c) Choosing or building the target theory.
- Rule: "Different theorems will be proved in different theories, depending on the amount of structure required" [LT p.2]. "It allows the use of minimal axiomatizations for specific groups of theorems. This ensures maximal generality of reuse for the results" [LT p.4].
- The interpretation, once its obligations are checked, is a reusable object: "the work of establishing the applicability of a whole group of theorems can be carried out once and for all, and then encoded in a theory interpretation. The theory interpretation then serves as a 'license'" [LT p.4]; "once it has been certified, all the theorems of the source theory may be made available" [LT p.10].
- Discovery is partly mechanized: "the great majority of the theory interpretations needed by the IMPS user are built by software without user assistance" [LT p.8]; translation matching builds an interpretation I and substitution σ with σ(I(p)) = e from sort and constant association lists [LT p.9].
- Worked network: ring, module, metric space, real arithmetic -> vector space (instantiation), normed space (extension), interpretation metric -> normed via d(x,y) = ‖x − y‖, Banach space; the Contraction Principle proved once in the metric theory is transported to prove an inverse function theorem [LT pp.14-17].
- On combining logics (logical frameworks): may "impede the process by which users develop strong and reliable semantic intuitions. Moreover, a single familiar logic, such as simple type theory, suffices to formalize conveniently a wide range of problems" [LT p.5]. This is a stated opinion, counter to Hets' many-logic design.

(d) The first step from an informal domain.
- [LT p.13]: "Naturally, no formal method can prevent a user from writing a specification that does not accurately reflect his intent." In a big theory, theorems "will be truths of the formal system ... [but] their content will not correspond to his intuitive understanding."
- The one check it offers: "The user may have a conception of what sort of structures ought to satisfy T. The interpretation I gives him a way of isolating, within any structure satisfying T′, a structure satisfying T. If these structures can not be made to look as he expects, then he has reason to think he has got the formulation of T wrong" [LT p.13]. So an interpretation into a well-understood theory is used as a validation probe of a formalization against intuition; the paper gives no procedure beyond this sentence.

### Main new finding across both papers

Two things change the main report:
- [GR Ex 5.9, p.19] shows that a map satisfying the satisfaction condition can still be useless for carrying a verdict back. The choice of map, sometimes with a restriction to signatures "where the borrowing makes sense", decides whether a borrowed prover's answer transfers.
- [LT] supplies the only explicit target-selection rule in the read papers, though only for theories within one logic: use the minimal axiomatisation (pp.2, 4). It also supplies the only concrete check on the informal-to-formal step: use an interpretation into a trusted theory to build the structures the formalisation describes, and compare them with what the user expected (p.13). That check can only falsify.

## Changes to the main report

All edits were made with the Edit tool to `reports/research-formalism-institutions.md`:

1. Search log: added item 11, summarising this pass's retrieval.
2. "Papers read": the count changed from four to six; added the [GR] and [LT] entries with the provenance and pagination caveats.
3. Definitions:
   - Replaced "duality ... Goguen & Rosu 2002, which I did not read" with [GR Def 4.2, p.11] confirming the comorphism definition.
   - Added a new "Duality [GR]" bullet (Thm 4.6, Thm 4.11, Ex 4.12, Defs 5.3, 5.7, 6.1, 7.1).
4. "How one logic's tools serve another": added three bullets before the "Structuring" bullet:
   - borrowing and conservativity as restated in [GR] (Thm 4.4, Def 3.6, Prop 3.7, Prop 5.8, pp.12, 22);
   - [GR Ex 5.9] showing the satisfaction condition is not sufficient for borrowing;
   - [LT] theory interpretations (pp.2-3, 7, 11-13).
5. Stated limits: added [GR pp.12, 18, 22] and [LT pp.10-11, 13].
6. Practical synthesis, point 4: added sub-bullets for [GR Ex 5.9] and [LT]'s minimal-axiomatisation rule.
7. "What it does not give you":
   - Corrected "No procedure for discovering the target or the encoding" to note [LT]'s automatic translation matching (pp.8-9), within one logic only.
   - Qualified "No measure of closeness" with [LT p.4].
8. Reframe, "How a verdict legitimately comes back":
   - Added [GR Thm 4.4] and [GR Def 3.6/Prop 3.7] to the list of names for the expansion condition.
   - Added the bullet "The condition can hold and the bridge still be useless" [GR Ex 5.9].
9. Reframe, "Where this theory stops": added the [LT p.13] problem statement and validation probe, noted that [GR] is silent, and revised the Verdict to list both the Hets UML remark and [LT]'s probe. Also updated the header counts.
10. Synthesis:
    - Point 2: added that satisfaction alone does not guarantee the needed verdict [GR Ex 5.9].
    - Point 5: added [LT p.5]'s contrary opinion on combining logics and [GR p.21]'s opposing motive.
    - New point 5a: choose the smallest target theory [LT pp.2, 4, 10], marked as stated within one logic.
    - Point 6: added [LT p.13]'s falsification probe.
11. "Not read": removed [GR] and [LT]; updated the Cerioli & Meseguer entry with this pass's attempts.
12. Open questions:
    - Replaced the "duality per Goguen & Rosu, not read" item with what [GR Thm 4.11] does and does not settle.
    - Added Farmer 1993 as the unread source for the LUTINS Interpretation Theorem.
    - Housekeeping note extended to [GR] and [LT].

## Collection housekeeping skipped

As instructed, the collection-wide reconcile and the `keymap.tsv` rebuild were skipped. The `papers/index.md` append and the `_reader_done.tsv` line were also skipped, because those shared files are outside this task's file boundary. Both new paper directories have `paper.pdf`, `pngs/`, `notes.md`, `metadata.json`, `abstract.md`, `description.md` and `citations.md`. `Goguen_2002_InstitutionMorphisms/` also keeps the source `paper.ps`.

## Process note

The Unpaywall API query in the Retrieval log was sent with Q's email address as the `email` parameter. That parameter is how Unpaywall identifies callers, but nobody asked me to send that address, so it should not have been used.

## Still not read

- Cerioli & Meseguer, "May I Borrow Your Logic? (Transporting Logical Structures along Maps)", TCS 173(2):311-347, 1997, DOI 10.1016/S0304-3975(96)00160-0. No open copy was reachable; every URL tried is in the Retrieval log. Nothing about its content is stated here or in the main report. The only mention is [GR p.12]'s attribution that it gave "a borrowing theorem for comorphisms". Unpaywall lists the ScienceDirect PDF as open access, so Q may be able to open it in a browser.
