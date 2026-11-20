"""Command-line interface for skill-path suggestions."""
from __future__ import annotations
import argparse
from .storage import load_sequences
from .core import train_model, build_report, save_report, evaluate_model, find_skill_gaps
from .llm import suggest_next_skills


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(description="Suggest next skills from employee skill sequences.")
    parser.add_argument("--skills", help="Comma-separated current skills, e.g. 'Python, SQL'")
    parser.add_argument("--role", default="", help="Current job role (informational context)")
    parser.add_argument("--top-n", type=int, default=5, help="Number of next-skill suggestions")
    parser.add_argument("--data", default=None, help="Path to employee sequence JSON")
    parser.add_argument("--report", action="store_true", help="Generate frequent patterns and skill-gap report")
    parser.add_argument("--evaluate", action="store_true", help="Evaluate next-skill prediction on held-out events")
    args = parser.parse_args(argv)
    records = load_sequences(args.data)
    if args.report:
        report = build_report(records)
        path = save_report(report)
        print(f"Report saved to {path}")
        print("\nFrequent transition patterns:")
        for rule in report["transition_rules"][:10]:
            print(f"  {rule['from']} -> {rule['to']}  confidence={rule['confidence']:.1%} support={rule['support']:.1%}")
        print("\nPotential team skill gaps (lowest coverage):")
        for item in find_skill_gaps(records):
            print(f"  {item['skill']}: {item['coverage']:.1%} of employees")
        return 0
    if args.evaluate:
        print(evaluate_model(records))
        return 0
    if args.skills:
        skills = [s.strip() for s in args.skills.split(",") if s.strip()]
    else:
        raw = input("Enter current skills separated by commas: ")
        skills = [s.strip() for s in raw.split(",") if s.strip()]
    if not skills:
        parser.error("At least one skill is required.")
    model = train_model(args.data)
    print(f"Current role: {args.role or 'Not specified'}")
    print("Current skills: " + ", ".join(skills))
    print("\nSuggested next skills:")
    for i, item in enumerate(suggest_next_skills(skills, model, args.top_n), 1):
        print(f"{i}. {item['skill']}  likelihood: {item['likelihood']:.1%}")
    print("\nSuggestions are exploratory training ideas, not employee assessments.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
