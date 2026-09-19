# Community submissions

Run your agent on the sandbox track, save the result as
`<your-agent-name>.json` in this directory, and open a pull request.
The **Community leaderboard** workflow will score it against the frozen
v1.0 gold and post the scorecard as a comment on your PR.

Rules:

- The file must validate against [`../SCHEMA.md`](../SCHEMA.md):
  `strata-bench evaluate submissions/community/<your-agent-name>.json --format text`
- One file per agent/run. Name it after the agent and model, e.g.
  `myagent-gpt5.json`.
- Do not read `data/hidden/` when producing the run — the workflow scores
  with the in-tree gold, so the honor system applies (same as local eval).
- Set `model` and `agent_scaffold` fields so the board is informative.

Accepted runs are listed in the [community leaderboard](../README.md#community-leaderboard).
