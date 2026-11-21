from __future__ import annotations

import argparse
from pathlib import Path

from app.core import generate_default_report, milestone_1, milestone_2, milestone_4, milestone_5
from app.storage import Store


def _parse_skills(raw_items: list[str]) -> list[str]:
    parsed: list[str] = []
    for entry in raw_items:
        for part in entry.split(","):
            cleaned = part.strip()
            if cleaned:
                parsed.append(cleaned)
    return parsed


def main(argv: list[str] | None = None) -> None:
    parser = argparse.ArgumentParser(
        prog="skill-path-triage-assistant",
        description="HR managers analyze employee skill acquisition sequences to suggest relevant next courses or identify common skill gaps for team training.",
    )
    sub = parser.add_subparsers(dest="command", required=True)
    sub.add_parser("hello", help="check that everything is wired up")

    suggest_p = sub.add_parser("suggest", help="suggest next skills or roles from current skills/roles")
    suggest_p.add_argument("items", nargs="+", help="current skill(s) or role(s)")
    suggest_p.add_argument("--top-n", type=int, default=3, help="number of suggestions to return")
    suggest_p.add_argument("--save", action="store_true", help="save suggestion result to the local store")

    eval_p = sub.add_parser("evaluate", help="evaluate next-step LM and write report")
    eval_p.add_argument("--top-n", type=int, default=3, help="top-N accuracy window")
    eval_p.add_argument("--write-report", action="store_true", help="write report to reports/evaluation_report.md")

    args = parser.parse_args(argv)
    if args.command == "hello":
        print("Skill Path Triage Assistant is ready. Open README.md for your milestones.")
    elif args.command == "suggest":
        items = _parse_skills(args.items)
        suggestions = milestone_5(items, top_n=args.top_n)
        print(f"Current profile: {', '.join(items)}")
        for rank, (nxt, score) in enumerate(suggestions, start=1):
            print(f"  {rank}. {nxt} (confidence: {score:.1%})")
        if args.save:
            Store().put("last_suggestion", {"inputs": items, "suggestions": suggestions})
    elif args.command == "evaluate":
        seqs = milestone_1()
        patterns = milestone_2(seqs, min_support=0.2, min_confidence=0.4)
        metrics = milestone_4(seqs, top_n=args.top_n, seed=42)
        print(
            f"Evaluated {metrics['test_count']} sequences | "
            f"Baseline Top-1: {float(metrics['baseline_top1_acc']):.1%} | "
            f"LM Top-1: {float(metrics['lm_top1_acc']):.1%} | "
            f"LM Top-{args.top_n}: {float(metrics['lm_top_n_acc']):.1%}"
        )
        print(f"Discovered {len(patterns)} frequent transition patterns.")
        if args.write_report:
            report_path = generate_default_report(Path("reports/evaluation_report.md"))
            print(f"Saved report to {report_path}")


if __name__ == "__main__":
    main()
