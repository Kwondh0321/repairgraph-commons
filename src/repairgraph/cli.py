"""Command-line interface for RepairGraph Commons."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

from . import __version__
from .core import diagnose, load_graph, validate_graph


def positive_integer(value: str) -> int:
    parsed = int(value)
    if parsed < 1:
        raise argparse.ArgumentTypeError("1 이상의 정수를 입력하세요")
    return parsed


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="공개 수리 지식 그래프를 검증하고 검색합니다."
    )
    parser.add_argument(
        "--version", action="version", version=f"%(prog)s {__version__}"
    )
    subparsers = parser.add_subparsers(dest="command", required=True)
    validate = subparsers.add_parser("validate")
    validate.add_argument("graph", type=Path)
    query = subparsers.add_parser("query")
    query.add_argument("graph", type=Path)
    query.add_argument("symptom")
    query.add_argument("--limit", type=positive_integer, default=5)
    args = parser.parse_args(argv)
    try:
        graph = load_graph(args.graph)
        if args.command == "validate":
            errors = validate_graph(graph)
            print(
                json.dumps(
                    {"valid": not errors, "errors": errors},
                    ensure_ascii=False,
                    indent=2,
                )
            )
            return 1 if errors else 0
        results = diagnose(graph, args.symptom, args.limit)
        print(
            json.dumps(
                {"query": args.symptom, "results": results},
                ensure_ascii=False,
                indent=2,
            )
        )
        return 0 if results else 1
    except (OSError, TypeError, ValueError, json.JSONDecodeError) as error:
        print(f"repairgraph: {error}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
