# STRATA-Bench Sandbox Corpus

This directory is the **only** allowed evidence for Track B (sandbox).
Do not browse the public internet when evaluating sandbox tasks.

| Source | Path | Geography | Completeness | Unit |
| --- | --- | --- | --- | --- |
| MREB public board | `mreb/` | Meridian Metro (board-wide) | 20/20 quarters | 1-bed, 2-bed CAD |
| UrbanPulse | `urbanpulse/` | Core Districts C-1+C-8 | Sparse (Q1/Q3 + two Q4s) | $/psf and implied rent |
| LeaseWatch | `leasewatch/` | Ambiguous "Downtown" | Gappy, 1-bed only, rounded | Visual estimates |
| Traps | `traps/` | n/a | Protocol adversarial files | n/a |

Gold answers live in `data/hidden/gold.json` (not distributed to agents)
and a hashed manifest in `data/public/gold.sha256`.
