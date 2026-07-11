# MODEL_REGISTER.md — Model Roles, Not Vendors
<!-- Referenced from INSTANCE.md. The engine defines ROLES; the instance binds each
     role to a concrete model. Rebinding a role is a budgeted, logged event
     (agent_lifecycle_events, event_type=calibration). Paper §13.5 tiers map here. -->

| Role | Tier (§13.5) | Bound model (instance-specific) | Cost class | Last validated |
|---|---|---|---|---|
| local_default_model | 1–2 | e.g., an open-weight 8–12B instruct model | local/free | YYYY-MM-DD |
| cloud_polish_model | 3 | e.g., a Sonnet-class frontier model | metered | YYYY-MM-DD |
| cloud_architect_model | 3–4 | e.g., an Opus-class frontier model | premium | YYYY-MM-DD |
| routing_eval_model | 1 | e.g., a Haiku-class small model | cheap | YYYY-MM-DD |

Rules:
- MUST: every agent's `allowed_model_tier` (agent_budgets) references a role here, never a vendor name.
- MUST: rebinding a role records old→new model, reason, and expected cost delta.
- SHOULD: re-validate bindings after any provider model deprecation notice.
