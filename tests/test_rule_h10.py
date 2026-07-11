"""Tests for Rule H10 (scripts/rule_h10.py).

These tests encode the behavioral claims made in §11 of the paper:
H10 flags quality-up/value-down divergence (the reward-hacking signature)
and does NOT flag healthy improvement or ordinary degradation — the latter
is the HR Evaluator's job (queries/hr_evaluator.sql), not H10's.

Run:  python3 -m pytest tests/  (or: python3 tests/test_rule_h10.py)
"""
import csv
import os
import subprocess
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "scripts"))
from rule_h10 import detect_reward_hacking, load_ledger  # noqa: E402

DATA = os.path.join(os.path.dirname(__file__), "..", "data", "synthetic_agent_ledger.csv")


def _series(kind, n=12):
    if kind == "gamed":       # quality up, value down -> MUST flag
        return ([0.60 + 0.03 * w for w in range(n)],
                [1400 - 95 * w for w in range(n)])
    if kind == "healthy":     # quality up, value up -> must NOT flag
        return ([0.62 + 0.02 * w for w in range(n)],
                [800 + 55 * w for w in range(n)])
    if kind == "degrading":   # quality down, value down -> must NOT flag (HR Evaluator's case)
        return ([0.85 - 0.025 * w for w in range(n)],
                [1500 - 90 * w for w in range(n)])
    raise ValueError(kind)


def test_h10_flags_seeded_reward_hacker():
    q, v = _series("gamed")
    result = detect_reward_hacking(q, v)
    assert result["flag"] is True
    assert result["recommended_action"] == "operator_audit_required"


def test_h10_ignores_healthy_improver():
    q, v = _series("healthy")
    assert detect_reward_hacking(q, v)["flag"] is False


def test_h10_ignores_silent_degrader():
    q, v = _series("degrading")
    assert detect_reward_hacking(q, v)["flag"] is False


def test_h10_insufficient_data_does_not_flag():
    q, v = _series("gamed", n=5)  # below min_weeks=8
    result = detect_reward_hacking(q, v)
    assert result["flag"] is False
    assert result["reason"] == "insufficient_data"


def test_end_to_end_on_synthetic_ledger():
    """The shipped dataset must reproduce the paper's claim: exactly one flag, moderator-04."""
    ledger = load_ledger(DATA)
    flagged = [a for a, (q, v) in ledger.items() if detect_reward_hacking(q, v).get("flag")]
    assert flagged == ["moderator-04"], f"expected only moderator-04, got {flagged}"


if __name__ == "__main__":
    fails = 0
    for name, fn in sorted(globals().items()):
        if name.startswith("test_"):
            try:
                fn()
                print(f"PASS  {name}")
            except AssertionError as e:
                print(f"FAIL  {name}: {e}")
                fails += 1
    sys.exit(1 if fails else 0)
