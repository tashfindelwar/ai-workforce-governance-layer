-- Resource Budgets: per-agent allowances. Paper §8.1(2).
-- Rule: agents request, evaluators recommend, operators approve, runtime executes.
CREATE TABLE agent_budgets (
    agent_id VARCHAR(64) PRIMARY KEY,
    max_tokens_per_task INT,
    max_thinking_time_seconds INT,
    allowed_model_tier VARCHAR(32),
    parallel_instance_count INT DEFAULT 1,
    skill_access JSONB,               -- list of registered tool ids (see TOOL_REGISTRY.md)
    monthly_cost_cap_usd DECIMAL(10,2),
    status VARCHAR(32) NOT NULL CHECK (status IN ('active','suspended','retired')),
    last_review_date DATE
);
