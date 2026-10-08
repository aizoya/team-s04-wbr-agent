"""Replay a saved analyst response without invoking data tools or models."""
import argparse
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from src.analyst_adapter import run_analyst_week


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--response", required=True, help="Saved run_analyst(week) JSON response")
    parser.add_argument("--week", required=True, help="Requested comparison week")
    args = parser.parse_args()
    response = json.loads(Path(args.response).read_text())
    result = run_analyst_week(
        args.week, lambda week: response,
        expected_tool_names=("get_weekly_metric", "get_breakdown", "get_delivery_signals"),
        label="CAPTURED_UNVERIFIED",
    )
    print(json.dumps(result.renderer_input, indent=2, allow_nan=False))


if __name__ == "__main__":
    main()
