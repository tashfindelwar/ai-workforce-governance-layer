-- Request Queue: structured agent requests for more resources. Paper §8.1(3).
CREATE TABLE agent_resource_requests (
    id SERIAL PRIMARY KEY,
    agent_id VARCHAR(64) NOT NULL,
    request_type VARCHAR(32) NOT NULL CHECK (request_type IN
        ('budget_increase','new_skill','model_upgrade','parallelize')),
    justification TEXT,
    evidence JSONB,                   -- links to agent_ledger rows demonstrating need
    expected_value DECIMAL(10,2),
    evaluator_recommendation TEXT,
    operator_decision VARCHAR(32),    -- approved / denied / deferred
    created_at TIMESTAMP DEFAULT NOW(),
    decided_at TIMESTAMP
);
