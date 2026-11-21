"""Command-line entry point: `python -m app.cli --help`."""
import argparse


def main(argv: list[str] | None = None) -> None:
    parser = argparse.ArgumentParser(prog="skill-path-triage-assistant", description="HR managers analyze employee skill acquisition sequences to suggest relevant next courses or identify common skill gaps for team training.")
    sub = parser.add_subparsers(dest="command", required=True)
    sub.add_parser("hello", help="check that everything is wired up")
    # TODO: add your own commands here as you work through the milestones.
    args = parser.parse_args(argv)
    if args.command == "hello":
        print("Skill Path Triage Assistant is ready. Open README.md for your milestones.")


if __name__ == "__main__":
    main()
