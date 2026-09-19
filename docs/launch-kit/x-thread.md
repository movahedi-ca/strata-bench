# X thread (copy-paste)

**Post 1:**
SWE-bench tests whether AI agents can patch code.

STRATA-Bench asks a harder question: does your agent know what a number is? 🧵

github.com/movahedi-ca/strata-bench

**Post 2:**
We asked 6 frontier engines for a 5-year downtown condo rent series. They split into three archetypes:

📐 Empirical Literalists — faithful to the metro board, honest about geography
📊 Synthetic Econometricians — modeled a downtown premium, said so
🕳️ Fragmented Extractors — OCR'd charts, skipped 9 of 20 quarters, plotted the gaps as equal ticks

**Post 3:**
So we turned that failure mode into a scored protocol: 36 sandbox tasks across 6 failure families — geographic masking, temporal attrition, OCR laundering, silent interpolation, non-uniform axes, source blending.

Agents are scored on whether they DISCLOSE, TAG, REFUSE, or MODEL — not on producing a pretty dashboard.

**Post 4:**
Hard fails cap a task at 55%: geographic masking, silent interpolation, paywall fabrication, metro-blended-as-downtown.

The unconstrained prompt "give me downtown rents" is a trap. The benchmark teaches the protocol-compliant brief.

**Post 5:**
v1.1.0 is live: 🏆 community leaderboard (PR your agent's run, a bot scores it), 📖 docs site, 📦 automated PyPI releases.

Try it in 60 seconds:
```
pip install strata-bench
strata-bench evaluate submissions/examples/extractor.json --format text
```
Watch the Fragmented Extractor get caught. Then beat it.

---
Media: attach docs/assets/social-card.png or docs/assets/promo.mp4
