# Power / MDE calculation — Phase B (attach to the OSF pre-registration)

*Computed 2026-07-16, before any Phase A/B data collection. Stdlib-only script:
`scripts` snapshot at the end of this file; rerunnable with `python3 mde_calc.py`.*

## Committed sample size

- **N = 240 tasks per condition** × 4 conditions (A, B, C, D) = **960 tasks total**.
- At the deployment's observed throughput (≈4 eligible tasks/day per condition stream) this fits a
  ~60 collection-day window inside the 90-day study period, with slack for holidays/outages.
- **No optional stopping.** Collection ends when each arm reaches 240 accepted-or-rejected tasks
  (not 240 accepted — acceptance is an outcome).
- **B-2 pattern sub-experiment:** N = 120 tasks per pattern (swarm / generate-validate-repair /
  human-gated), run after B-1 on the same stream; labeled secondary.

## Test framework

- α = 0.05 two-sided, power = 0.80.
- **4 pre-specified primary contrasts** (Bonferroni-adjusted α = 0.0125):
  1. **B − A** — observability effect,
  2. **C − B** — governance + tool-registry effect,
  3. **D − B** — Governance-Layer effect in isolation,
  4. **C − D** — Tool-Registry increment.
- Serial correlation: tasks arrive in daily blocks (m ≈ 4/day). Assuming within-day ICC = 0.10, the
  **design effect = 1 + (m−1)·ICC = 1.30**, i.e. effective n ≈ 185/arm. (The analysis itself uses a
  block bootstrap over days / mixed model with day random effects, per §8; DEFF here is only for
  planning.)
- Cost/token outcomes are right-skewed → analyzed on the **log scale**; MDEs below are stated both as
  Cohen's d and as the detectable **geometric-mean ratio**, assuming SD(log tokens-per-accepted-output)
  ≈ 0.8 (to be replaced by the Phase-A estimate in the results paper; the commitment is the N, not σ).

## Minimum detectable effects at N = 240/arm

| Scenario | MDE (Cohen's d) | Detectable geo-mean ratio (σ_log = 0.8) |
|---|---|---|
| iid, unadjusted α = .05 | 0.256 | 1.23 (~23%) |
| iid, Bonferroni α = .0125 | 0.305 | 1.28 (~28%) |
| **Headline: DEFF 1.30 + Bonferroni** | **0.348** | **1.32 (~32%)** |

**Operator approval rate** (primary DV #3), Bonferroni + DEFF, detectable absolute difference:

| Baseline approval | Detectable difference |
|---|---|
| 60% | ≈ 17.0 pp |
| 70% | ≈ 15.9 pp |
| 80% | ≈ 13.9 pp |

## Interpretation committed in advance

The study is powered to detect **≳ 32% differences in geometric-mean tokens/cost per accepted output**
and **≳ 14–17 pp differences in approval rate** between any primary pair of conditions under the most
conservative assumptions. The working paper's economic thesis predicts differences well above this
threshold (deterministic-first vs agent-led orchestration); effects smaller than the MDE will be
reported as **not distinguishable at this study size**, not as nulls. H-R4/H-R5 remain exploratory and
are excluded from the primary-contrast correction.

## Reproducible script

```python
from statistics import NormalDist
import math
nd = NormalDist(); z = nd.inv_cdf
ALPHA, POWER = 0.05, 0.80
Z_BETA = z(POWER)
def mde_d(n, alpha, deff=1.0):
    za = z(1 - alpha/2); return (za + Z_BETA) * math.sqrt(2 / (n/deff))
def mde_prop(n, p0, alpha, deff=1.0):
    za = z(1 - alpha/2); return (za + Z_BETA) * math.sqrt(2*p0*(1-p0) / (n/deff))
N, K = 240, 4
DEFF = 1 + (4.0 - 1) * 0.10           # m=4 tasks/day, ICC=0.10
d = mde_d(N, ALPHA/K, DEFF)           # 0.348
ratio = math.exp(d * 0.8)             # 1.32
pp70 = mde_prop(N, 0.7, ALPHA/K, DEFF)  # 0.159
```
