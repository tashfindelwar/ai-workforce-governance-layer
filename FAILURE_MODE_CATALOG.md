# Failure Mode Catalogue (public reference version)

The living catalogue described in §10 of the paper. Each entry maps an observed or
industry-documented failure mode to the architectural defense that addresses it.
Status: **Industry-doc.** = documented across the paper's cited industry/benchmark
sources; **Motivating** = the problem motivating v7.0's contribution (defense
specified, production evidence pending Phase A).

This is the sanitized public version. Deployment-specific entries (agent names,
workload details) are excluded by design; contribute new generic entries via
CONTRIBUTING.md using this format.

| ID | Status | Failure mode | Architectural defense |
|---|---|---|---|
| FM-001 | Industry-doc. | Hallucinated tool calls | Tool Registry validation (Layer G) |
| FM-002 | Industry-doc. | Hallucination cascades | Dispatch Relay separation (Principle 7) |
| FM-003 | Industry-doc. | Context overflow | Bounded passes with checkpoints (RULE B3.5) |
| FM-004 | Industry-doc. | Cost runaway from infinite loops | Per-task token budgets + state-hash loop detection |
| FM-005 | Industry-doc. | Schema drift after framework upgrade | Staging path + weekly schema validation |
| FM-006 | Industry-doc. | Stale data recycled | Freshness flags + stale-source gate |
| FM-007 | Motivating | Agent silent degradation | Agent Ledger + HR Evaluator (Layer H) |
| FM-008 | Motivating | Reward hacking | Value attribution tracking (Rule H10; paper §11) |
| FM-009 | Industry-doc. | Channel noise contamination | Output guard at Dispatch Relay |
| FM-010 | Industry-doc. | Wiki epistemic loop | Structured claims with required evidence |

New entries require: the failure's observable signature (trace/ledger), the defense,
and which principle it instantiates. See paper §10 for the governing rules
(entries are never deleted, only superseded; every entry cites its evidence).
