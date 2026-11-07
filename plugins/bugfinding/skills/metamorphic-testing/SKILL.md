---
name: metamorphic-testing
description: Guides metamorphic bugfinding by deriving valid relations between transformed executions. Use when expected outputs are unavailable, extending round-trip checks, or testing transformations whose state, effects, numerical rules or result composition can invalidate an apparent equivalence.
---

# Metamorphic testing

Search related executions whose observations must satisfy a justified relation. A violated valid relation exposes an inconsistency; agreement cannot establish ground truth because both executions can share a defect ([Query Partitioning, §§3 and 6](https://www.manuelrigger.at/preprints/TLP.pdf)).

## Derive the relation from the actual contract

Read the real producer, enabled semantics and existing oracle. State the admissible original input/state, transformation, transformed execution conditions, required observation and composition rule. Explain what implementation behavior the transformation changes and why the relation still holds. Query partitioning illustrates why composition varies by feature rather than following one universal equality rule ([Query Partitioning, §3](https://www.manuelrigger.at/preprints/TLP.pdf)).

Check effects, evaluation multiplicity, exceptional behavior and nondeterminism before using an algebraic rewrite: SQLite's BETWEEN evaluates its left expression once, while its expanded comparisons can repeat it ([SQLite expressions, §§6–7](https://www.sqlite.org/lang_expr.html)). Numeric rearrangement also needs the target's overflow, rounding and empty/NULL rules; use `numerical-oracles` for a justified error contract rather than inventing epsilon ([SQLite aggregates](https://www.sqlite.org/lang_aggfunc.html)). Read [relation design](references/relation-design.md) when constructing or reviewing a relation.

## Generate follow-up cases that exercise the relation

Reuse the target's existing representation, formatter and transformations. Construct valid original state/programs, select applicable relations, and derive the dependent variants. SQLancer's actual TLP producer generates an original query and predicate, negated-predicate and NULL variants; its reproducer retains them together ([TLPWhereOracle](https://raw.githubusercontent.com/sqlancer/sqlancer/main/src/sqlancer/common/oracle/TLPWhereOracle.java)).

Count admitted originals, completed transformed executions and actual relation evaluations separately. Expected-error skips are not successful comparisons: the inspected SQLancer helper raises IgnoreMeException for unavailable/expected-error results ([ComparatorHelper](https://raw.githubusercontent.com/sqlancer/sqlancer/main/src/sqlancer/ComparatorHelper.java)). Use `harness-sensitivity` to verify that an existing healthy case and representative violation discriminate through this relation; examples of suitable controls are in [worked relations](references/worked-relations.md).

Match the observation to the guarantee. Preserve required columns, types, multiplicities and effects; compare ordering only where promised. SQLite distinguishes UNION ALL from duplicate-removing UNION and leaves unordered SELECT output unspecified ([SQLite SELECT, §§3–4](https://www.sqlite.org/lang_select.html)). Inspect the actual comparator: SQLancer's shown helper reads first-column strings and checks count plus sets, which is weaker than complete row-bag equality ([ComparatorHelper](https://raw.githubusercontent.com/sqlancer/sqlancer/main/src/sqlancer/ComparatorHelper.java)).

## Preserve the related experiment

Retain original setup/world, original and transformed programs, transformation parameters, enabled configuration, raw outcomes, admissibility evidence and selected violation. SQLancer's documented reduction requires the setup and continued disagreement of related queries ([SQLancer logs/reduction](https://raw.githubusercontent.com/sqlancer/sqlancer/main/README.md)).

After shrinking an original or setup, regenerate its variants and re-establish relation preconditions; shrinking only the final query can remove the required database state ([SQLancer reduction](https://raw.githubusercontent.com/sqlancer/sqlancer/main/README.md)). For world/program adaptations, retain dependent identities and observations through the target's real owners. Use `failure-reduction` for reduction mechanics, `semantic-program-generation` for valid program construction, and `evidence-based-triage` for attribution. These links define this pack's ownership.

Return the relation and its contract basis, tested domain, actual evaluation counts, paired replay artifacts, observed contradiction and unresolved assumptions. A mismatch under an invalid relation is not a demonstrated product violation; the TLP paper itself limits its model and distinguishes dialect-dependent behavior ([Query Partitioning, §§4 and 6](https://www.manuelrigger.at/preprints/TLP.pdf)).

For a fitting DBMS target, read [SQLancer operation](references/sqlancer-operation.md); for misleading shortcuts, read [common mistakes](references/common-mistakes.md). Select execution and budget through `bugfinding-campaign` and the project's existing authority.
