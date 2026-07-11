# Contributing

The most valuable contribution is a **failure-mode report** from your own
deployment: what failed, its signature in traces or the ledger, and what
mitigated it. Open an issue using the format of the paper's Failure Mode
Catalogue (ID, status, failure mode, architectural defense).

Also welcome: Rule H10 threshold-calibration data (§11.3), schema extensions
with rationale, and adapters that populate `agent_ledger` from specific trace
stores (Langfuse, LangSmith, OTel).

Please do not submit real ledger data containing PII or client-identifiable
information; sanitize per Layer F rules first.
