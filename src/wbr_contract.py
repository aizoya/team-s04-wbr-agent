from __future__ import annotations

import math
import re
from dataclasses import dataclass
from typing import Any, Iterable, Mapping, Optional, Sequence


class ContractError(ValueError):
    pass


@dataclass(frozen=True)
class Metric:
    """Internal metric model.

    Internal status intentionally uses uppercase values and a singular evidence_ref.
    External tool envelopes use lowercase ok/partial/error and plural evidence_refs.
    Conversion must be explicit through the adapter functions below.
    """

    name: str
    value: Optional[float]
    status: str = "OK"
    evidence_ref: Optional[str] = None
    caveat: Optional[str] = None


EXPECTED_HEADLINE_METRICS = ("revenue", "orders", "review_score")

CAUSAL_PATTERNS = [
    r"\bcaused by\b",
    r"\bcaused\b",
    r"\bbecause(?:\s+of)?\b",
    r"\bdue to\b",
    r"\bled to\b",
    r"\bresulted in\b",
    r"\bresulted from\b",
    r"\bas a result of\b",
    r"\bdriven by\b",
    r"\battribut(?:ed|able) to\b",
    r"\bstemming from\b",
]


def validate_number(value: Any, field: str) -> float:
    if isinstance(value, bool) or not isinstance(value, (int, float)):
        raise ContractError(f"{field} must be numeric")
    value = float(value)
    if not math.isfinite(value):
        raise ContractError(f"{field} must be finite")
    return value


def pct_change(prior: float, current: float) -> Optional[float]:
    prior = validate_number(prior, "prior")
    current = validate_number(current, "current")
    if prior == 0:
        return None
    return ((current - prior) / prior) * 100.0


def mean_review(scores: Iterable[Any]) -> Optional[float]:
    clean = [validate_number(v, "review_score") for v in scores if v is not None]
    return None if not clean else sum(clean) / len(clean)


def assert_unique_order_ids(rows: list[dict]) -> None:
    ids = [row["order_id"] for row in rows]
    if len(ids) != len(set(ids)):
        raise ContractError("order-grain rows contain duplicate order_id values")


def reconcile_total(headline: float, parts: Iterable[Any], label: str, tolerance: float = 1e-9) -> None:
    headline = validate_number(headline, f"{label}.headline")
    values = [validate_number(v, f"{label}.part") for v in parts]
    if abs(sum(values) - headline) > tolerance:
        raise ContractError(f"{label} parts do not reconcile to headline")


def guard_noncausal(text: str) -> None:
    lowered = text.lower()
    for pattern in CAUSAL_PATTERNS:
        if re.search(pattern, lowered):
            raise ContractError("unsupported causal language detected")


def report_status(
    metrics: Iterable[Metric],
    expected_names: Sequence[str] = EXPECTED_HEADLINE_METRICS,
) -> str:
    """Return COMPLETE only for a non-empty, exact expected set with valid values/evidence."""

    items = list(metrics)
    if not items:
        return "PARTIAL"

    names = [metric.name for metric in items]
    if len(names) != len(set(names)):
        return "PARTIAL"

    by_name = {metric.name: metric for metric in items}
    if set(by_name) != set(expected_names):
        return "PARTIAL"

    for name in expected_names:
        metric = by_name[name]
        if metric.status != "OK" or not metric.evidence_ref or metric.value is None:
            return "PARTIAL"
        validate_number(metric.value, f"metric.{name}.value")

    return "COMPLETE"


def unavailable_metric(name: str, caveat: str) -> Metric:
    return Metric(name=name, value=None, status="UNAVAILABLE", caveat=caveat)


def metric_to_external(metric: Metric) -> dict[str, Any]:
    """Explicit internal -> external adapter; never equate status/evidence fields implicitly."""

    status_map = {"OK": "ok", "PARTIAL": "partial", "UNAVAILABLE": "error"}
    if metric.status not in status_map:
        raise ContractError(f"unsupported internal metric status: {metric.status}")
    return {
        "name": metric.name,
        "value": metric.value,
        "status": status_map[metric.status],
        "evidence_refs": [metric.evidence_ref] if metric.evidence_ref else [],
        "warnings": [metric.caveat] if metric.caveat else [],
    }


def external_to_metric(payload: Mapping[str, Any]) -> Metric:
    """Explicit external -> internal adapter for simple metric-shaped payloads."""

    status_map = {"ok": "OK", "partial": "PARTIAL", "error": "UNAVAILABLE"}
    status = payload.get("status")
    if status not in status_map:
        raise ContractError("external metric status must be ok, partial, or error")

    refs = payload.get("evidence_refs", [])
    if not isinstance(refs, list) or any(not isinstance(ref, str) or not ref for ref in refs):
        raise ContractError("evidence_refs must be a list of non-empty strings")

    value = payload.get("value")
    internal_status = status_map[status]
    if internal_status == "OK":
        value = validate_number(value, "external_metric.value")
    elif value is not None:
        value = validate_number(value, "external_metric.value")

    warnings = payload.get("warnings", [])
    if warnings is None:
        warnings = []
    if not isinstance(warnings, list) or any(not isinstance(w, str) for w in warnings):
        raise ContractError("warnings must be a list of strings")

    return Metric(
        name=str(payload.get("name") or ""),
        value=value,
        status=internal_status,
        evidence_ref=refs[0] if refs else None,
        caveat="; ".join(warnings) if warnings else None,
    )
