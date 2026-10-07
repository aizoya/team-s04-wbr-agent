from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from src.wbr_runner import run_wbr


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Run deterministic acceptance against real-Olist tool envelopes and a trusted planted-scenario answer key."
    )
    parser.add_argument("--fixture", required=True, help="JSON fixture containing tool_results, claims, and answer_key")
    args = parser.parse_args()

    fixture = json.loads(Path(args.fixture).read_text())
    label = fixture.get("label")
    if label not in {"PLANTED_REAL_OLIST", "REAL_OLIST_INCOMPLETE"}:
        raise SystemExit("fixture label must be PLANTED_REAL_OLIST or REAL_OLIST_INCOMPLETE")

    expected_tools = tuple(fixture["expected_tool_names"])
    tool_results = fixture["tool_results"]
    claims = fixture["claims"]
    answer_key = fixture["answer_key"]

    by_name = {item["tool_name"]: item for item in tool_results}
    calls = [
        (
            name,
            lambda _params, payload=by_name[name]: payload,
            dict(by_name[name].get("parameters", {})),
        )
        for name in expected_tools
        if name in by_name
    ]

    def analyst(_results):
        return claims

    def verifier(claim, evidence_by_ref):
        expected = answer_key.get(claim["claim_id"])
        if expected is None:
            return {
                "claim_id": claim["claim_id"],
                "outcome": "remove",
                "reason": "claim absent from trusted answer key",
            }

        required = set(expected.get("required_evidence_refs", []))
        if not required or not required.issubset(set(evidence_by_ref)):
            return {
                "claim_id": claim["claim_id"],
                "outcome": "remove",
                "reason": "answer-key evidence unavailable",
            }

        return {
            "claim_id": claim["claim_id"],
            "outcome": expected["outcome"],
            "reason": "trusted planted-scenario answer key",
        }

    result = run_wbr(
        calls,
        analyst,
        verifier=verifier,
        expected_tool_names=expected_tools,
        label=label,
    )

    output = {
        "fixture": str(Path(args.fixture)),
        "label": label,
        "status": result.status,
        "renderer_input": result.renderer_input,
    }
    print(json.dumps(output, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
