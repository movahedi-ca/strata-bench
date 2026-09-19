# Package announcement — ready to send

**Where:** comp.lang.python.announce (moderated newsgroup for Python
release announcements) and/or the python-announce mailing list.
Check the current submission address at
https://www.python.org/community/lists/ before sending.

**Rules followed:** background info included, URL included, version
number given, license stated, signature with email, lines ≤ 78 chars,
2–3 line HTML snippet at the end for python.org's front page.

---

Subject: ANN: STRATA-Bench 1.1.0 — benchmark for AI agents on
 fragmented spatial-temporal market intelligence

I'm happy to announce STRATA-Bench 1.1.0, a benchmark for AI agents
that must compile longitudinal market intelligence from fragmented,
geographically nested, and temporally incomplete evidence.

Unlike factuality benchmarks that score single answers, STRATA-Bench
scores agent *conduct* across 36 sandbox tasks in six failure families:

- geographic masking (metro numbers relabeled as downtown)
- temporal attrition (inventing quarters the corpus never had)
- OCR laundering (scan artifacts reported as clean facts)
- silent interpolation (estimates plotted as observed data)
- non-uniform axes (plots that hide missingness)
- source blending (mixing asking and closed rents into fake trends)

Agents are scored on whether they disclose, tag, refuse, or model
uncertainty — refusal is a scored success, not a failure. The corpus
is fully synthetic and self-contained, the gold is held out, and three
reference agents ship in-tree so results are reproducible end to end.

Install:  pip install strata-bench
Docs:     https://movahedi-ca.github.io/strata-bench/
Repo:     https://github.com/movahedi-ca/strata-bench
PyPI:     https://pypi.org/project/strata-bench/
Conda (pending review): conda-forge/staged-recipes#34892

STRATA-Bench is a community benchmark: there is an open call for
agent submissions with automatic scoring on every pull request, plus
a public leaderboard and an interactive task explorer.

License: Apache-2.0. Requires Python 3.10+.

--
Mohammad Movahedi
m.h.movahedi97@gmail.com

<P><A HREF="https://movahedi-ca.github.io/strata-bench/">STRATA-Bench 1.1.0</A> - 36-task benchmark scoring whether AI agents disclose, tag, refuse, or model uncertainty on fragmented market intelligence. (19-Sep-26)
