-- Lifecycle Events: state transitions with justification. Paper §8.1(5), Table 1.
-- States: probationary | standard | promoted | under_review | retired
CREATE TABLE agent_lifecycle_events (
    id SERIAL PRIMARY KEY,
    agent_id VARCHAR(64) NOT NULL,
    event_type VARCHAR(32) NOT NULL,  -- promotion / demotion / review_opened / review_closed / retirement / calibration
    from_state VARCHAR(32),
    to_state VARCHAR(32),
    justification TEXT,
    created_at TIMESTAMP DEFAULT NOW()
);
