-- HR Evaluator (paper §8.1(4)) — deterministic trend metrics (Rule H12).
-- The decision WHETHER performance is up or down is SQL; LLM reasoning is used
-- only for the written recommendation text.

-- 4-week performance summary per agent
SELECT agent_id,
       SUM(tasks_completed)                                   AS tasks,
       ROUND(AVG(quality_score), 3)                           AS avg_quality,
       ROUND(SUM(total_cost_usd), 2)                          AS cost_usd,
       ROUND(SUM(value_attribution), 2)                       AS value_usd,
       ROUND(SUM(total_cost_usd) / NULLIF(SUM(tasks_succeeded), 0), 4) AS cost_per_output,
       ROUND(SUM(value_attribution) / NULLIF(SUM(total_cost_usd), 0), 2) AS value_per_cost
FROM agent_ledger
WHERE week_start >= CURRENT_DATE - INTERVAL '28 days'
GROUP BY agent_id
ORDER BY value_per_cost DESC NULLS LAST;

-- Trend: this 4 weeks vs previous 4 weeks (improving / stable / degrading)
WITH recent AS (
  SELECT agent_id, AVG(quality_score) q FROM agent_ledger
  WHERE week_start >= CURRENT_DATE - INTERVAL '28 days' GROUP BY agent_id),
prior AS (
  SELECT agent_id, AVG(quality_score) q FROM agent_ledger
  WHERE week_start >= CURRENT_DATE - INTERVAL '56 days'
    AND week_start <  CURRENT_DATE - INTERVAL '28 days' GROUP BY agent_id)
SELECT r.agent_id, ROUND(r.q - p.q, 3) AS quality_delta,
       CASE WHEN r.q - p.q >  0.05 THEN 'improving'
            WHEN r.q - p.q < -0.05 THEN 'degrading'
            ELSE 'stable' END AS trend
FROM recent r JOIN prior p USING (agent_id)
ORDER BY quality_delta;

-- Hallucination rate trending up (under_review trigger candidate)
SELECT agent_id, week_start,
       hallucination_count::float / NULLIF(tasks_completed, 0) AS hallucination_rate
FROM agent_ledger
WHERE week_start >= CURRENT_DATE - INTERVAL '28 days'
ORDER BY agent_id, week_start;
