# INSTANCE.md — Deployment-Specific Configuration
<!-- Engine/instance separation: paper §14. Everything in this file is per-deployment.
     Everything NOT in this file is engine, identical across deployments. -->

## Operator
- operator_name:
- operator_role: CEO of this workforce
- timezone:
- notification_channel:        # e.g. telegram:@handle

## Business Context
- icp_definition:              # ideal customer profile
- content_pillars: []
- pricing_tiers: []
- brand_voice_ref: wiki/style/voice.md

## Models (roles, not vendors — see MODEL_REGISTER.md)
- local_default_model:         # e.g. an open-weight 9B-class model
- cloud_polish_model:          # Sonnet-class role
- cloud_architect_model:       # Opus-class role
- routing_eval_model:          # Haiku-class role

## Budgets
- monthly_cost_cap_usd:
- per_task_token_budget_default:
- reward_hack_threshold: 0.30  # Rule H10, calibrate per §11.3

## Data & Isolation (mandatory per §14)
- data_root:                   # unique per instance
- database_name:               # separate operational DB per instance
- backup_target:               # isolated per instance
- secrets_scope:               # scoped per instance

## Channels & Sources
- publishing_channels: []
- source_lists: []
- search_backends: []          # consumed by Search Router (Layer D)
