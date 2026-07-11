# Sample agent_resource_requests entry (rendered)

- agent_id: outreach-01
- request_type: model_upgrade
- justification: "Quality plateaued at 0.71 on local-small across weeks 4–6 while
  rejection reasons cluster on tone nuance; mid-tier local model projected to lift
  acceptance ≥10% at +$6/month."
- evidence: ledger rows weeks 4–6 (quality 0.70, 0.71, 0.71; rework 22%)
- expected_value: 180.00
- evaluator_recommendation: "Approve; projected value/cost ratio 4.2; revisit in 4 weeks."
- operator_decision: approved (2026-06-02)

The flow this encodes (paper §8.1): the agent requests, the evaluator recommends,
the operator approves, the runtime enforces. Agents never grant themselves resources.
