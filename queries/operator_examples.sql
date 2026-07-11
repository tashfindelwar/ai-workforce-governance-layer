-- Common operator questions, answered from the ledger.

-- "Which agents earn their keep?"
SELECT agent_id, SUM(value_attribution) - SUM(total_cost_usd) AS net_value_usd
FROM agent_ledger GROUP BY agent_id ORDER BY net_value_usd DESC;

-- "Who is over budget this month?"
SELECT l.agent_id, SUM(l.total_cost_usd) AS spend, b.monthly_cost_cap_usd
FROM agent_ledger l JOIN agent_budgets b USING (agent_id)
WHERE date_trunc('month', l.week_start) = date_trunc('month', CURRENT_DATE)
GROUP BY l.agent_id, b.monthly_cost_cap_usd
HAVING SUM(l.total_cost_usd) > b.monthly_cost_cap_usd;

-- "What resource requests are waiting on me?"
SELECT id, agent_id, request_type, expected_value, created_at
FROM agent_resource_requests WHERE operator_decision IS NULL
ORDER BY created_at;

-- "Show every lifecycle change for an agent"
SELECT created_at, event_type, from_state, to_state, justification
FROM agent_lifecycle_events WHERE agent_id = :agent ORDER BY created_at;
