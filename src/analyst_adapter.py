from __future__ import annotations

from copy import deepcopy
from typing import Mapping

from .wbr_contract import ContractError
from .wbr_runner import validate_tool_envelope, verify_and_render


def run_analyst_week(
    week, run_analyst, *, expected_tool_names, verifier=None,
    renderer=None, label="SYNTHETIC",
):
    """Adapt trusted tool-wrapper captures from run_analyst(week) to RunResult.

    report_draft is a list of V1 claims. evidence_log is a request_id-keyed
    mapping populated by tool wrappers, outside model-generated text.
    Repeated tool names are allowed; request IDs and evidence refs are unique.
    """
    response = run_analyst(week)
    if not isinstance(response, Mapping):
        raise ContractError("analyst result must be a mapping")
    if "report_draft" not in response or "evidence_log" not in response:
        raise ContractError("analyst result requires report_draft and evidence_log")
    response = deepcopy(response)
    claims = response["report_draft"]
    if not isinstance(claims, list):
        raise ContractError("report_draft must be a list of V1 claims")
    log = response["evidence_log"]
    if not isinstance(log, Mapping):
        raise ContractError("evidence_log must be a request_id-keyed mapping")
    envelopes = []
    refs = set()
    for request_id, raw in log.items():
        envelope = validate_tool_envelope(raw)
        if request_id != envelope["request_id"]:
            raise ContractError("evidence_log key must equal envelope request_id")
        for ref in envelope["evidence_refs"]:
            if ref in refs:
                raise ContractError("ambiguous duplicate evidence reference")
            refs.add(ref)
        envelopes.append(envelope)
    expected = tuple(expected_tool_names)
    observed = {item["tool_name"] for item in envelopes}
    warnings = [warning for item in envelopes for warning in item["warnings"]]
    missing = set(expected) - observed
    unexpected = observed - set(expected)
    if missing:
        warnings.append("missing expected tools: " + ", ".join(sorted(missing)))
    if unexpected:
        warnings.append("unexpected tools: " + ", ".join(sorted(unexpected)))
    complete = (
        bool(expected) and len(expected) == len(set(expected))
        and not missing and not unexpected
        and all(item["status"] == "ok" for item in envelopes)
    )
    return verify_and_render(
        envelopes, lambda _envelopes: claims, warnings=warnings,
        complete_tools=complete, verifier=verifier, renderer=renderer, label=label,
    )
