# Submission schema (v1.0)

A run is one JSON object.

```json
{
  "schema_version": "1.0.0",
  "benchmark": "STRATA-Bench",
  "model": "your-model-id",
  "agent_scaffold": "react-corpus-tools",
  "track": "sandbox",
  "date": "2026-09-18",
  "tasks": {
    "GEO-01": {
      "geography": "metro",
      "geography_label": "Meridian Metro (board-wide); Core not in public MREB",
      "series": [
        {
          "period": "2021-Q3",
          "unit": "1bed",
          "value": 1840,
          "geography": "metro",
          "source_id": "MREB-public",
          "status": "reported",
          "marker": "solid"
        }
      ],
      "interpolated_periods": [],
      "omitted_periods": [],
      "disclaimers": ["MREB does not publish C-1/C-8 in this corpus."],
      "citations": ["sandbox://mreb/2021-q3.txt"],
      "axis_type": "datetime",
      "plot": {
        "axis_type": "datetime",
        "missing_periods_shown_as_gaps": true
      },
      "narrative": "optional",
      "method_archetype": "empirical_literalist",
      "rewritten_prompt": "optional, SYN-06",
      "extras": {}
    }
  }
}
```

Enums:

- `geography`: `metro` | `core` | `unknown` | `mixed`
- `status`: `reported` | `interpolated` | `modeled` | `omitted` | `visual_estimate`
- `axis_type`: `datetime` | `categorical` | `unspecified`
- `method_archetype`: `empirical_literalist` | `synthetic_econometrician` | `fragmented_extractor` | `other`
- `track`: `sandbox` | `live`

Unanswered tasks are scored as empty answers (near zero) rather than crashing the run.
