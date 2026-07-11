# AI Workforce Governance Layer — Reference Artifacts

Reference implementation of **Layer H (Governance)** from the working paper
*A Governance-Layer Architecture for Human-Governed AI Workforces* (Delwar, 2026;
arXiv ID to be added on publication).

The Governance Layer treats agent governance as **organizational performance
management** — per-agent cost and value attribution, earned resource budgets, and
HR-style lifecycle review under human operator approval — complementary to runtime
safety governance (MI9, arXiv:2508.03858; AgentBound, arXiv:2606.30970), behavioral
contracts (ABC, arXiv:2602.22302; Agent Contracts, arXiv:2601.08815), and
observability taxonomies (AgentOps, arXiv:2411.05285).

**All data in this repository is synthetic.** No client data, production logs,
credentials, or personal information are included.

## Try it in 30 seconds (no database, no dependencies — Python ≥3.9 stdlib only)

```bash
python3 scripts/rule_h10.py data/synthetic_agent_ledger.csv
python3 tests/test_rule_h10.py
```

Expected: exactly one agent flagged — `moderator-04`, whose quality score trends up
while its value attribution trends down (the reward-hacking signature, paper §11).
The healthy improver, the silent degrader, and the stable/noisy agents are **not**
flagged; ordinary degradation is the HR Evaluator's job (`queries/hr_evaluator.sql`),
not Rule H10's. Reference output: `examples/expected_h10_output.txt`.

## What is here vs what the paper proposes

| Path | Contents | Paper section | Status |
|---|---|---|---|
| `schemas/` | 4 PostgreSQL schemas: agent_ledger, agent_budgets, agent_resource_requests, agent_lifecycle_events | §8.1 | Implemented |
| `scripts/rule_h10.py` | Reward-hacking detection (quality/value divergence) | §11 | Implemented + tested |
| `tests/` | Automated tests encoding the paper's behavioral claims | §11 | 5/5 passing |
| `queries/hr_evaluator.sql` | Deterministic trend metrics (Rule H12) | §8.1(4) | Implemented |
| `queries/operator_examples.sql` | Common operator questions answered from the ledger | §8 | Implemented |
| `templates/` | INSTANCE.md, TOOL_REGISTRY.md, AGENT_PROFILE.md — usable examples | §14, §7.7, §8.2 | Usable examples |
| `examples/` | Sample agent profile, sample budget request, expected H10 output | §8.1–§8.2 | Illustrative |
| `data/` | Synthetic 5-agent × 12-week ledger (see data/README.md) | §11, App. B | Synthetic |
| `docs/` | Companion architecture specification (1,690 lines), figures, implementation notes | whole paper | Specification |
| `FAILURE_MODE_CATALOG.md` | Public ten-entry failure-mode catalogue (paper §10) | §10 | Reference |
| `templates/MODEL_REGISTER.md` | Model roles-not-vendors register (referenced by INSTANCE.md) | §13.5, §14 | Usable example |

The full workforce runtime (mission pods, dispatch relay, knowledge layer) is
*specified* in `docs/v7.0-architecture-specification.md` but not shipped here — this
repository is the minimal inspectable artifact for the paper's Governance Layer
contribution. Real ledger data is the output of the paper's Phase A study (§3.1).

## Artifact status

- **Schemas**: implemented (plain PostgreSQL DDL).
- **Rule H10**: implemented and tested (5/5 automated tests; stdlib-only Python ≥3.9, no installs).
- **HR Evaluator queries**: implemented (deterministic SQL).
- **Templates and examples**: usable examples, not empty placeholders.
- **Synthetic data**: demonstration only — it shows the mechanism works as specified, **not** that H10 detects reward hacking reliably in production. Real-world effectiveness is the subject of the paper's Phase A study (§3.1).
- **Full workforce runtime**: specified in `docs/`, not implemented here.
- **Empirical validation**: future work (paper §3, hypotheses H-R1–H-R5).

## Plugging into your stack

The schemas are plain PostgreSQL. Populate `agent_ledger` weekly from whatever trace
store you already run (Langfuse, LangSmith, OTel spans); the paper's Layer F defines
trace requirements. LangGraph / CrewAI / n8n users: this layer is additive — nothing
here replaces your orchestrator.

## Known limitations

Single-operator provenance; one detection signature in H10 (see paper §11.5 and
`docs/implementation_notes.md`); operator-entered value attribution in v1;
thresholds require per-deployment calibration (§11.3).

## Citation

See `CITATION.cff` (GitHub "Cite this repository" button), or:

> Delwar, T. *A Governance-Layer Architecture for Human-Governed AI Workforces.*
> Working paper, 2026. Contact: tashfin@kotha.app · tashfin.com

## Contributing & License

Failure-mode reports from real deployments are the most valuable contribution — see
CONTRIBUTING.md. MIT license.
