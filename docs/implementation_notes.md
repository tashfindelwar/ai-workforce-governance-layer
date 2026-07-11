# Implementation Notes

## What is implemented in this repository vs proposed in the paper

| Component | Status here | Paper section |
|---|---|---|
| Governance Layer schemas (4 tables) | Implemented (SQL) | §8.1 |
| Rule H10 detection | Implemented + tested (stdlib Python) | §11 |
| HR Evaluator trend metrics | Implemented (SQL) | §8.1(4), Rule H12 |
| Templates (INSTANCE, TOOL_REGISTRY, AGENT_PROFILE) | Usable examples | §14, §7.7, §8.2 |
| Synthetic ledger dataset | Included | §11, Appendix B |
| Full workforce runtime (pods, dispatch relay, knowledge layer) | Proposed — specified in docs/v7.0-architecture-specification.md, not shipped here | §6–§8 |
| Real ledger data | Not included — Phase A output (paper §3.1) | §3 |

## Design decisions
- **Stdlib-only Python** for H10: zero install friction for reviewers; linear
  regression is 15 lines and auditable.
- **Plain PostgreSQL DDL**: portable; no ORM; comments carry the governance rules.
- **Thresholds and units (match paper §11.2–§11.3 exactly)**: both series are peak-normalized;
  slopes are per-week; the flag threshold is stated over the window (default 0.30) and divided
  by the window length at comparison time → 0.025/week. Feasible per-week divergence is ~[0, 0.25],
  so the per-week comparison is what makes the threshold reachable. Severity is high when per-week
  divergence exceeds 0.10. Worked example: moderator-04 → q_slope +0.033, v_slope −0.071,
  divergence 0.104/week → flagged, high. Calibrate per deployment; report calibration with Phase A.

## Known limitations
- H10 detects one divergence signature (quality↑/value↓); §11.5 of the paper lists
  what it deliberately does not do.
- Value attribution is operator-entered in v1; automated attribution is future work.
- Single-operator provenance: everything here reflects one deployment's design period.
