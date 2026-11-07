# Conditional SQLancer operation

Use this route for a fitting DBMS implementation target, not an application's business invariant. The SQLancer README documents Java 11+ and Maven prerequisites, generated schema/data/query stages, version-sensitive backends, logs and bounded execution ([README](https://raw.githubusercontent.com/sqlancer/sqlancer/main/README.md)). Verify the selected release, actual jar, embedded DBMS version, supported backend and local dependency/build policy before running it.

In an existing compatible integration, a finite command shape is:

```text
java -jar SQLANCER_JAR --num-threads 1 --timeout-seconds 120 sqlite3 --oracle QUERY_PARTITIONING
```

The values are illustrative allocations, not defaults. General options precede the backend; backend oracle options follow it ([README](https://raw.githubusercontent.com/sqlancer/sqlancer/main/README.md)). The inspected SQLite factory registers QUERY_PARTITIONING as a composite of WHERE, DISTINCT, GROUP_BY, HAVING and AGGREGATE ([factory](https://raw.githubusercontent.com/sqlancer/sqlancer/main/src/sqlancer/sqlite3/SQLite3OracleFactory.java)). Use actual selected-build help; this command was not executed while writing the skill.

Retain setup statements, related queries/results, selected oracle/configuration and actual errors/skips. Current-statement logs and reduced reproducer logs serve different purposes; reduction must continue to evaluate the related queries on their required state ([README](https://raw.githubusercontent.com/sqlancer/sqlancer/main/README.md)). Do not count elapsed search or generated queries as completed relation checks.

The actual TLP producer retains original and partition queries ([TLPWhereOracle](https://raw.githubusercontent.com/sqlancer/sqlancer/main/src/sqlancer/common/oracle/TLPWhereOracle.java)); inspect its actual output and ComparatorHelper before claiming full typed row/bag comparison ([ComparatorHelper](https://raw.githubusercontent.com/sqlancer/sqlancer/main/src/sqlancer/ComparatorHelper.java)). Expected-error handling and normalization can limit what was checked.

SQLancer's inspected license is MIT ([license text](https://raw.githubusercontent.com/sqlancer/sqlancer/main/LICENSE.md)). This reference does not install it, start a service, authorize target changes or imply permission to publish findings. Source/main and documentation were checked on 2026-11-07; repeat applicability checks for the selected version.
