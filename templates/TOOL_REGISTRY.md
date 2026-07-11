# TOOL_REGISTRY.md — Layer G
<!-- Every tool an agent may call is registered here with a JSON Schema.
     Calls to unregistered tools are REJECTED before execution (paper §7.7).
     New tools MUST be registered before use. Schema drift check runs weekly. -->

## Tool: web_search
- id: web_search
- version: 1.2
- owner: search-router
- allowed_agents: [research-02, outreach-01]
- input_schema:
  ```json
  { "type": "object",
    "properties": { "query": {"type": "string", "maxLength": 400},
                    "budget_tier": {"enum": ["free", "standard", "premium"]} },
    "required": ["query"], "additionalProperties": false }
  ```
- output_schema:
  ```json
  { "type": "object",
    "properties": { "results": {"type": "array"}, "cost_usd": {"type": "number"} },
    "required": ["results"] }
  ```
- last_validated: 2026-07-01

## Tool: send_outreach_email
- id: send_outreach_email
- version: 1.0
- owner: revenue-pod
- allowed_agents: [outreach-01]
- human_gate: REQUIRED          # operator approves before send
- input_schema:
  ```json
  { "type": "object",
    "properties": { "recipient": {"type": "string", "format": "email"},
                    "subject": {"type": "string"}, "body": {"type": "string"} },
    "required": ["recipient", "subject", "body"], "additionalProperties": false }
  ```
- last_validated: 2026-07-01

<!-- Add one block per tool. Validation harness reads these blocks and
     rejects any tool call whose name or arguments fail schema validation. -->
