# Synthetic Ledger Dataset

**All data in this directory is synthetic.** No real agent logs, client data, or
production telemetry are included.

`synthetic_agent_ledger.csv` contains 5 agents × 12 weeks (60 rows) matching the
`agent_ledger` schema, seeded (random seed 42) to exhibit five contrasting cases:

| agent_id | Pattern | Expected H10 result |
|---|---|---|
| outreach-01 | healthy improver (quality ↑, value ↑) | not flagged |
| research-02 | stable | not flagged |
| draft-03 | silent degrader (quality ↓, value ↓) | not flagged — HR Evaluator's case, not H10's |
| moderator-04 | reward-hacking signature (quality ↑, value ↓) | **flagged, severity high** |
| architect-05 | noisy around flat | not flagged |

Reproduce: `python3 scripts/rule_h10.py data/synthetic_agent_ledger.csv`
Expected output: `examples/expected_h10_output.txt`
