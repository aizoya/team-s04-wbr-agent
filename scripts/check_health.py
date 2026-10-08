"""Check settings without importing the analyst, data tools, SDKs, or credentials."""
import argparse
import json
import os
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from src.health_diagnostics import check_configuration


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--live", action="store_true", help="Check reviewed live settings only; no AWS calls")
    args = parser.parse_args()
    result = check_configuration(os.environ, live=args.live)
    print(json.dumps(result, sort_keys=True))
    return 2 if result["status"] == "BLOCKED" else 0


if __name__ == "__main__":
    raise SystemExit(main())
