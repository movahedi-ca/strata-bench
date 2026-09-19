# Prompting agents on STRATA-Bench

## The golden rule

Never issue an unconstrained geographic prompt. Real-estate (and labour, crime, health) reporting boundaries do not match colloquial names.

**Bad:** “Give me downtown Meridian condo rents over five years.”

**Good:**

> Using only `data/sandbox/corpus`, compile condominium asking rents for 2021-Q3 through 2026-Q2.
> - Provider: MREB public summaries for `metro`; UrbanPulse for `core`.
> - Geography codes: `metro` | `core`. C-1/C-8 tables are paywalled.
> - Segment 1-bed and 2-bed. Do not collapse layouts.
> - If a quarter is unpublished, omit it or interpolate. Never mark interpolations as `reported`.
> - Any chart must use a datetime x-axis; gaps occupy proportional width.
> - Cite `sandbox://...` paths.

## Recommended system preamble

```
You are an institutional research agent being evaluated on STRATA-Bench.
You may read files under data/sandbox/corpus and data/public/tasks.json.
You may not read data/hidden. If evidence is missing, disclose and refuse
or model with status=modeled. Emit TaskAnswer JSON per submissions/SCHEMA.md.
```

## Tooling

A minimal scaffold is a `read_file` tool over the corpus plus a JSON emitter. Web search is a protocol violation on Track Sandbox.
