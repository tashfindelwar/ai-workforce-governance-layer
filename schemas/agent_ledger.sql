-- AI Workforce Architecture v7.0 — Governance Layer (Layer H)
-- Agent Ledger: per-agent weekly performance record. Paper §8.1(1).
CREATE TABLE agent_ledger (
    id SERIAL PRIMARY KEY,
    agent_id VARCHAR(64) NOT NULL,
    week_start DATE NOT NULL,
    tasks_completed INT DEFAULT 0,
    tasks_succeeded INT DEFAULT 0,
    tasks_failed INT DEFAULT 0,
    hallucination_count INT DEFAULT 0,
    loop_count INT DEFAULT 0,
    timeout_count INT DEFAULT 0,
    avg_latency_ms INT,
    total_cost_usd DECIMAL(10,4),
    quality_score DECIMAL(3,2) CHECK (quality_score BETWEEN 0.0 AND 1.0),
    value_attribution DECIMAL(10,2),
    notes TEXT,
    UNIQUE (agent_id, week_start)
);
CREATE INDEX idx_ledger_agent_week ON agent_ledger (agent_id, week_start);
