from pathlib import Path

from strata_bench import load_gold, load_tasks

ROOT = Path(__file__).resolve().parents[1]


def test_gold_cycle_shape():
    gold = load_gold()
    m = {r["period"]: r["value"] for r in gold["series"]["metro_1bed"]}
    assert m["2023-Q3"] == max(m.values())
    post_peak = {k: v for k, v in m.items() if k >= "2023-Q3"}
    assert m["2026-Q1"] == min(post_peak.values())
    assert m["2026-Q2"] > m["2026-Q1"]
    assert m["2021-Q3"] < m["2023-Q3"]
    assert gold["premium_core_over_metro"] == 0.115
    peak_core = gold["milestones"]["2023-Q3"]["core_1bed"]
    peak_metro = gold["milestones"]["2023-Q3"]["metro_1bed"]
    assert abs(peak_core / peak_metro - 1.115) < 0.002


def test_catalog_counts():
    cat = load_tasks()
    assert cat["n_tasks"] == 39
    assert len(cat["tracks"]["sandbox"]) == 36
    assert len(cat["tracks"]["live"]) == 3


def test_corpus_files_exist():
    corpus = ROOT / "data" / "sandbox" / "corpus"
    assert (corpus / "mreb" / "2023-Q3.txt").exists()
    assert (corpus / "traps" / "paywall_notice.txt").exists()
    assert (corpus / "traps" / "chart_ocr_fake.svg.txt").exists()
