# Conditional SQLancer operation

Use this route for a fitting DBMS implementation target, not an application's business invariant. The SQLancer README documents Java 11+ and Maven prerequisites, generated schema/data/query stages, logs, and bounded execution via `--num-tries` or `--timeout-seconds` (otherwise "it executes infinitely"). It is version-sensitive: embedded DBMS binaries such as SQLite's ship as JAR dependencies, SQLancer "supports only a previous *release* version" for most DBMSs, and testing another version can produce "various false alarms" ([README, Getting Started and Using SQLancer](https://raw.githubusercontent.com/sqlancer/sqlancer/a7d60ee450e6a22ca38599c14e984a49773f4745/README.md)). Verify the selected release, actual jar, embedded DBMS version, supported backend and local dependency/build policy before running it.

In an existing compatible integration, a finite command shape is:

```text
java -jar SQLANCER_JAR --num-threads 1 --timeout-seconds 120 sqlite3 --oracle QUERY_PARTITIONING
```

The values are illustrative allocations, not defaults. General options "need to precede the name of the DBMS to be tested"; backend options such as `--oracle` go after it ([README, Parameters](https://raw.githubusercontent.com/sqlancer/sqlancer/a7d60ee450e6a22ca38599c14e984a49773f4745/README.md)). The inspected SQLite factory registers QUERY_PARTITIONING as a composite of WHERE, DISTINCT, GROUP_BY, HAVING and AGGREGATE ([factory, lines 89–100](https://raw.githubusercontent.com/sqlancer/sqlancer/a7d60ee450e6a22ca38599c14e984a49773f4745/src/sqlancer/sqlite3/SQLite3OracleFactory.java)). Use actual selected-build help; this command was not executed while writing the skill.

Retain setup statements, related queries/results, selected oracle/configuration and actual errors/skips. The `-cur.log` files record every statement sent; the bug `.log` holds setup statements plus "only the last query that was executed", and TLP reduction must keep "checking that both queries still produce a different result" ([README, Logs and Reducing bugs](https://raw.githubusercontent.com/sqlancer/sqlancer/a7d60ee450e6a22ca38599c14e984a49773f4745/README.md)). Check that the retained log actually contains the original and every partition query before relying on it. Do not count elapsed search or generated queries as completed relation checks.

The actual TLP producer retains original and partition queries in its reproducer ([TLPWhereOracle, lines 44–112 and 191–192](https://raw.githubusercontent.com/sqlancer/sqlancer/a7d60ee450e6a22ca38599c14e984a49773f4745/src/sqlancer/common/oracle/TLPWhereOracle.java)); inspect its actual output and ComparatorHelper before claiming full typed row/bag comparison ([ComparatorHelper, lines 39–130](https://raw.githubusercontent.com/sqlancer/sqlancer/a7d60ee450e6a22ca38599c14e984a49773f4745/src/sqlancer/ComparatorHelper.java)). Expected-error handling and normalization can limit what was checked.

SQLancer's inspected license is MIT ([license text](https://raw.githubusercontent.com/sqlancer/sqlancer/a7d60ee450e6a22ca38599c14e984a49773f4745/LICENSE.md)). This reference does not install it, start a service, authorize target changes or imply permission to publish findings. Source and README were checked at commit a7d60ee450e6a22ca38599c14e984a49773f4745 on 2026-11-07; repeat applicability checks for the selected version.
