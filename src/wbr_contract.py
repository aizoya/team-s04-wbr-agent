from __future__ import annotations

import math
import re
from dataclasses import dataclass
from typing import Any, Iterable, Optional


class ContractError(ValueError):
    pass


@dataclass(frozen=True)
class Metric:
    name: str
    value: Optional[float]
    status: str = "OK"
    evidence_ref: Optional[str] = None
    caveat: Optional[str] = None


CAUSAL_PATTERNS = [
    r"\bcaused by\b",
    r"\bbecause of\b",
    r"\bdue to\b",
    r"\bled to\b",
    r"\bresulted in\b",
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


def report_status(metrics: Iterable[Metric]) -> str:
    return "COMPLETE" if all(m.status == "OK" and m.evidence_ref for m in metrics) else "PARTIAL"


def unavailable_metric(name: str, caveat: str) -> Metric:
    return Metric(name=name, value=None, status="UNAVAILABLE", caveat=caveat)
