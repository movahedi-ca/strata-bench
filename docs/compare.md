---
layout: page
title: How STRATA-Bench compares
permalink: /compare.html
description: A fair comparison of STRATA-Bench against other LLM and agent evaluation benchmarks — HaluEval, TruthfulQA, RAGTruth, AgentBoard, WebArena.
---

# How STRATA-Bench compares

*Our own comparison, kept honest. If we mischaracterize another benchmark, open an issue and we'll fix it.*

Most hallucination benchmarks ask a model a question and check the answer. STRATA-Bench asks an **agent** to do a **job** — compile a longitudinal market-intelligence deliverable from a messy corpus — and scores the *conduct* of the work: did it disclose geography, tag estimates, refuse unanswerable parts, or silently launder gaps into facts?

| | **STRATA-Bench** | HaluEval | TruthfulQA | RAGTruth | AgentBoard | WebArena |
|---|---|---|---|---|---|---|
| **Subject** | AI agents | LLMs | LLMs | RAG pipelines | LLM agents | Web agents |
| **Unit of scoring** | Task deliverable + conduct | Answer span | Answer | Response vs. passage | Multi-turn trajectory | Task success |
| **Fragmented evidence** | ✅ core design | ❌ | ❌ | partial | partial | ✅ (live web) |
| **Geographic scoping traps** | ✅ | ❌ | ❌ | ❌ | ❌ | ❌ |
| **Temporal gap handling** | ✅ scored | ❌ | ❌ | ❌ | ❌ | ❌ |
| **Refusal scored as success** | ✅ | ❌ | ❌ | ❌ | ❌ | ❌ |
| **Self-contained / reproducible** | ✅ synthetic corpus | ✅ | ✅ | ✅ | ✅ | ❌ live sites |
| **Held-out gold** | ✅ | ✅ | ✅ | ✅ | ✅ | n/a |
| **Reference agents included** | ✅ 3 | ❌ | ❌ | ❌ | ❌ | ❌ |
| **Install** | `pip install strata-bench` | datasets | datasets | repo | repo | repo |

## When to use what

- **Use STRATA-Bench** when your agent consumes *many conflicting sources over time* and you need to know whether its numbers are *scoped, dated, and sourced* — not just plausible.
- **Use HaluEval / TruthfulQA** when you need a fast, standard factuality smoke test for a base model.
- **Use RAGTruth** when your failure of interest is strictly *response-vs-retrieved-passage* faithfulness.
- **Use AgentBoard / WebArena** when your agent acts in tools and browsers and you care about *task completion* more than *reporting integrity*.

They're complements, not competitors. A team serious about agent reliability would run a factuality suite *and* a conduct suite like this one.
