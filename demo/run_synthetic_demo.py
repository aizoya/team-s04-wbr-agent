from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from src.wbr_contract import mean_review, pct_change
from src.wbr_runner import run_wbr


EXPECTED_TOOLS = (
    "weekly_revenue",
    "weekly_orders",
    "weekly_review_score",
    "category_breakdown",
    "state_breakdown",
)


def envelope(name, data, *, status="ok", refs=None, warnings=None, error=None):
    return {
        "tool_name": name,
        "request_id": f"synthetic-{name}",
        "status": status,
        "generated_at": "2026-10-05T00:00:00+00:00",
        "parameters": {"dataset": "SYNTHETIC"},
        "data": data,
        "evidence_refs": [f"synthetic:{name}"] if refs is None and status != "error" else (refs or []),
        "warnings": warnings or [],
        "error": error,
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--scenario", choices=("complete", "partial"), default="complete")
    args = parser.parse_args()

    fixture_path = ROOT / "fixtures" / "synthetic_weekly_fixture.json"
    fixture = json.loads(fixture_path.read_text())
    prior = fixture["prior_week"]
    current = fixture["current_week"]

    review_status = "ok" if args.scenario == "complete" else "error"
    review_error = None if args.scenario == "complete" else "synthetic review tool failure"
    review_refs = None if args.scenario == "complete" else []

    payloads = {
        "weekly_revenue": envelope(
            "weekly_revenue",
            {
                "prior": prior["revenue"],
                "current": current["revenue"],
                "pct_change": pct_change(prior["revenue"], current["revenue"]),
            },
        ),
        "weekly_orders": envelope(
            "weekly_orders",
            {
                "prior": prior["orders"],
                "current": current["orders"],
                "pct_change": pct_change(prior["orders"], current["orders"]),
            },
        ),
        "weekly_review_score": envelope(
            "weekly_review_score",
            {
                "prior": mean_review(prior["review_scores"]),
                "current": mean_review(current["review_scores"]) if review_status == "ok" else None,
            },
            status=review_status,
            refs=review_refs,
            error=review_error,
        ),
        "category_breakdown": envelope(
            "category_breakdown",
            {"note": "synthetic placeholder; final payload owned by data workstream"},
        ),
        "state_breakdown": envelope(
            "state_breakdown",
            {"note": "synthetic placeholder; final payload owned by data workstream"},
        ),
    }

    calls = [
        (
            name,
            lambda _params, payload=payloads[name]: payload,
            {"dataset": "SYNTHETIC"},
        )
        for name in EXPECTED_TOOLS
    ]

    def analyst(_results):
        return [
            {
                "claim_id": "synthetic-revenue",
                "question_id": "q1",
                "statement": "Synthetic revenue declined by 20 percent week over week.",
                "claim_type": "fact",
                "confidence": None,
                "supporting_evidence": ["synthetic:weekly_revenue"],
                "causal_language_allowed": False,
                "requires_human_review": False,
            }
        ]

    result = run_wbr(
        calls,
        analyst,
        expected_tool_names=EXPECTED_TOOLS,
        label="SYNTHETIC",
    )
    print(json.dumps(result.renderer_input, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
