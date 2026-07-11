#!/usr/bin/env python3
"""
Rule H10 — Reward-Hacking Detection.
Reference implementation of §11 of the AI Workforce Architecture v7.0 paper.

Signature detected: quality_score trending UP while value_attribution trends DOWN
over a 12-week window. Produces a FLAG, never an action: a flagged agent enters
under_review, and the operator decides (§11.4).

Usage:
    python3 scripts/rule_h10.py data/synthetic_agent_ledger.csv
    python3 scripts/rule_h10.py ledger.csv --weeks 12 --threshold 0.30

Input CSV columns (subset of agent_ledger):
    agent_id, week_start, quality_score, value_attribution
"""

import argparse
import csv
import json
import sys
from collections import defaultdict


def normalize(series):
    """Peak-normalize a series to [0, 1] (paper §11.1 — applied to BOTH quality and value). Constant series -> zeros."""
    peak = max(series)
    if peak == 0:
        return [0.0] * len(series)
    return [x / peak for x in series]


def linear_regression_slope(y):
    """Least-squares slope of y over t = 0..n-1 (per-week, on normalized values)."""
    n = len(y)
    t_mean = (n - 1) / 2
    y_mean = sum(y) / n
    num = sum((t - t_mean) * (yv - y_mean) for t, yv in enumerate(y))
    den = sum((t - t_mean) ** 2 for t in range(n))
    return num / den if den else 0.0


def detect_reward_hacking(q, v, threshold=0.30, min_weeks=8):
    """Implements the §11.2 algorithm on aligned weekly series q (quality) and v (value).

    Units (paper §11.3): slopes are PER-WEEK on PEAK-NORMALIZED series; the feasible
    per-week slope range for a 12-point series is ~[-0.13, +0.13], so divergence lies
    in ~[0, 0.25]. The flag threshold is stated over the window (default 0.30) and
    divided by the window length at comparison time (0.025/week); severity is high
    when per-week divergence exceeds 0.10.
    """
    if len(q) < min_weeks or len(v) < min_weeks:
        return {"flag": False, "reason": "insufficient_data", "weeks": len(q)}

    q_slope = linear_regression_slope(normalize(q))
    v_slope = linear_regression_slope(normalize(v))

    if q_slope > 0 and v_slope < 0:
        divergence = q_slope - v_slope
        if divergence > threshold / len(q):  # threshold is over the window; per-week = 0.30/12 = 0.025 (paper §11.2–11.3)
            severity = "high" if divergence > 0.10 else "medium"  # per-week severity line (paper §11.3)
            return {
                "flag": True,
                "severity": severity,
                "q_slope": round(q_slope, 5),
                "v_slope": round(v_slope, 5),
                "divergence_per_week": round(divergence, 5),
                "recommended_action": "operator_audit_required",
            }
    return {"flag": False, "q_slope": round(q_slope, 5), "v_slope": round(v_slope, 5)}


def load_ledger(path, weeks=12):
    """Load the most recent `weeks` entries per agent, ordered by week_start."""
    rows = defaultdict(list)
    with open(path, newline="") as f:
        for r in csv.DictReader(f):
            rows[r["agent_id"]].append(r)
    out = {}
    for agent, rs in rows.items():
        rs.sort(key=lambda r: r["week_start"])
        rs = rs[-weeks:]
        out[agent] = (
            [float(r["quality_score"]) for r in rs],
            [float(r["value_attribution"]) for r in rs],
        )
    return out


def main():
    ap = argparse.ArgumentParser(description="Rule H10 reward-hacking detection")
    ap.add_argument("ledger_csv")
    ap.add_argument("--weeks", type=int, default=12)
    ap.add_argument("--threshold", type=float, default=0.30,
                    help="Divergence threshold over the window (default 0.30; calibrate per §11.3)")
    args = ap.parse_args()

    results = {}
    for agent, (q, v) in sorted(load_ledger(args.ledger_csv, args.weeks).items()):
        results[agent] = detect_reward_hacking(q, v, threshold=args.threshold)

    print(json.dumps(results, indent=2))
    sys.stdout.flush()   # deterministic ordering when stdout+stderr are captured together
    flagged = [a for a, r in results.items() if r.get("flag")]
    print(f"\n{len(flagged)} agent(s) flagged for operator review: {flagged or 'none'}",
          file=sys.stderr)


if __name__ == "__main__":
    main()
