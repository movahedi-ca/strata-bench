---
layout: page
title: Task Explorer
description: Browse all 36 STRATA-Bench sandbox tasks by failure family.
---

<style>
.fam-filters { margin: 1em 0; }
.fam-filters button {
  margin: 0 6px 8px 0; padding: 6px 14px; border-radius: 999px;
  border: 1px solid #6fbf9a; background: transparent; color: inherit; cursor: pointer;
}
.fam-filters button.active { background: #6fbf9a; color: #0e1210; font-weight: bold; }
.task-card { border: 1px solid #2a3530; border-radius: 10px; padding: 16px 18px; margin: 14px 0; }
.task-card h3 { margin: 0 0 6px; }
.task-meta { font-size: 0.85em; opacity: 0.75; margin-bottom: 8px; }
.task-meta .fam { font-weight: bold; color: #e8b05c; }
.task-card .lbl { font-weight: bold; }
.task-card details { margin-top: 8px; }
.task-card summary { cursor: pointer; color: #6fbf9a; }
#task-count { font-size: 0.9em; opacity: 0.7; }
</style>

<div class="fam-filters" id="filters"></div>
<p id="task-count"></p>
<div id="task-list"><p>Loading tasks…</p></div>

<script>
fetch("assets/tasks.json").then(r => r.json()).then(data => {
  const fams = data.families;
  const filters = document.getElementById("filters");
  const list = document.getElementById("task-list");
  const count = document.getElementById("task-count");
  let active = "ALL";

  const btn = (key, label) => {
    const b = document.createElement("button");
    b.textContent = label;
    b.dataset.fam = key;
    if (key === "ALL") b.classList.add("active");
    b.onclick = () => {
      active = key;
      filters.querySelectorAll("button").forEach(x => x.classList.toggle("active", x === b));
      render();
    };
    filters.appendChild(b);
  };
  btn("ALL", "All 36");
  Object.keys(fams).forEach(k => { if (k !== "LIVE") btn(k, k + " · " + fams[k].split(" ")[0]); });

  function esc(s){ return s.replace(/&/g,"&amp;").replace(/</g,"&lt;"); }

  function render() {
    const tasks = data.tasks.filter(t => active === "ALL" || t.family === active);
    count.textContent = tasks.length + " task" + (tasks.length === 1 ? "" : "s") +
      (active === "ALL" ? "" : " in family " + active);
    list.innerHTML = tasks.map(t => `
      <div class="task-card">
        <h3>${esc(t.id)} — ${esc(t.title)}</h3>
        <div class="task-meta"><span class="fam">${t.family}</span> · ${esc(t.primary_dimension)} · weight ${t.weight}</div>
        <p><span class="lbl">Prompt:</span> ${esc(t.prompt)}</p>
        <details><summary>Success criteria</summary><p>${esc(t.success)}</p></details>
        <details><summary>Hard fail</summary><p>${esc(t.hard_fail)}</p></details>
      </div>`).join("");
  }
  render();
}).catch(() => {
  document.getElementById("task-list").innerHTML = "<p>Could not load task data.</p>";
});
</script>
