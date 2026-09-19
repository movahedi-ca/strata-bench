"""Command-line interface: `strata-bench evaluate submissions/run.json`."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

from . import __version__
from .evaluate import evaluate_submission, load_gold, load_tasks
from .report import render_markdown, render_text


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        prog="strata-bench",
        description="STRATA-Bench evaluation harness for AI-agent submissions.",
    )
    parser.add_argument("--version", action="version", version=f"STRATA-Bench {__version__}")
    sub = parser.add_subparsers(dest="cmd", required=True)

    p_eval = sub.add_parser("evaluate", help="Score a submission JSON file.")
    p_eval.add_argument("submission", type=Path)
    p_eval.add_argument("--gold", type=Path, default=None)
    p_eval.add_argument("--tasks", type=Path, default=None)
    p_eval.add_argument("--track", choices=["sandbox", "live"], default=None)
    p_eval.add_argument("--format", choices=["json", "text", "markdown"], default="text")
    p_eval.add_argument("-o", "--output", type=Path, default=None)

    p_list = sub.add_parser("list-tasks", help="Print the public task catalog.")
    p_list.add_argument("--family", default=None)
    p_list.add_argument("--format", choices=["text", "json"], default="text")

    args = parser.parse_args(argv)

    if args.cmd == "list-tasks":
        catalog = load_tasks()
        tasks = catalog["tasks"]
        if args.family:
            tasks = [t for t in tasks if t["family"] == args.family.upper()]
        if args.format == "json":
            json.dump(tasks, sys.stdout, indent=2)
            sys.stdout.write("\n")
        else:
            print(f"STRATA-Bench v{catalog['version']}  —  {len(tasks)} tasks\n")
            for t in tasks:
                print(f"  {t['id']:<9} {t['title']}")
        return 0

    gold = load_gold(args.gold) if args.gold else load_gold()
    catalog = load_tasks(args.tasks) if args.tasks else load_tasks()
    result = evaluate_submission(
        args.submission, gold=gold, catalog=catalog, track=args.track
    )
    if args.format == "json":
        payload = json.dumps(result, indent=2) + "\n"
    elif args.format == "markdown":
        payload = render_markdown(result)
    else:
        payload = render_text(result)

    if args.output:
        args.output.write_text(payload, encoding="utf-8")
    else:
        sys.stdout.write(payload)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
