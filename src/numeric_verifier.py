"""Conservative contradiction check for an explicitly bounded claim grammar.

Never accepts arbitrary prose, and never promotes a claim solely because a
number appears somewhere in a capture. Unknown forms retain fallback review.
"""
import math
import re
from collections.abc import Mapping
from decimal import Decimal

from .wbr_runner import default_verify_claim


CHANGE_CLAIM = re.compile(
    r"(?:(?P<category>[a-z][a-z0-9_]*) )?"
    r"(?P<metric>revenue|orders|items) (?P<direction>fell|rose) "
    r"(?P<amount>\d+(?:\.\d+)?)%"
    r"(?: in (?P<state>[A-Z]{2}|Other))?\.?", re.ASCII)
METRICS = {"revenue": "product_revenue", "orders": "orders", "items": "items"}


def _finite(value):
    return isinstance(value, (int, float)) and not isinstance(value, bool) and math.isfinite(value)


def _series(envelope, metric, state, category, week):
    """Select precisely the stated metric, comparison week and filter slice."""
    params, data = envelope.get("parameters"), envelope.get("data")
    if not isinstance(params, Mapping) or not isinstance(data, Mapping):
        return []
    if params.get("week") != week or params.get("metric") != metric or data.get("metric") != metric:
        return []
    if envelope.get("tool_name") == "get_weekly_metric":
        if params.get("state") == state and params.get("category") == category:
            return [data]
    if envelope.get("tool_name") == "get_breakdown":
        dimension = params.get("dimension")
        if data.get("dimension") != dimension:
            return []
        group = None
        if dimension == "state" and state and params.get("state") is None and params.get("category") == category:
            group = state
        if dimension == "category" and category and params.get("category") is None and params.get("state") == state:
            group = category
        groups = data.get("groups")
        if group and isinstance(groups, list):
            return [g for g in groups if isinstance(g, Mapping) and g.get("group") == group]
    return []


def make_captured_verifier(week):
    """Remove contradictions with scoped, internally consistent numeric evidence.

    Only positive previous values and finite non-negative additive metrics are
    supported. The claimed percentage is rounded at its displayed precision.
    Matching numbers remain subject to the existing semantic/human review;
    this gate never upgrades the fallback outcome to keep.
    """
    def verify(claim, evidence):
        fallback = default_verify_claim(claim, evidence)
        if fallback["outcome"] == "remove" or fallback["reason"] == "unsupported causal language":
            return fallback
        match = CHANGE_CLAIM.fullmatch(claim["statement"])
        if not match or claim["claim_type"] != "fact":
            return fallback
        metric = METRICS[match["metric"]]
        series = []
        for ref in set(claim["supporting_evidence"]):
            envelope = evidence[ref]
            if envelope.get("status") not in {"ok", "partial"}:
                continue
            envelope = envelope.get("source_envelope", envelope)
            series.extend(_series(envelope, metric, match["state"], match["category"], week))
        if not series:
            return fallback
        intervals = []
        for item in series:
            current, previous, change = (item.get(k) for k in ("current", "previous", "change"))
            if (item.get("change_type") != "pct" or item.get("data_issue")
                    or not all(_finite(v) for v in (current, previous, change))
                    or current < 0 or previous <= 0):
                return {**fallback, "reason": "numeric evidence incomplete or malformed"}
            # Lakshmi's builder rounds current, previous and change separately
            # to two decimals. Recomputing rounded inputs with an exact-value
            # tolerance would falsely reject legitimate captures. Intersect
            # the possible arithmetic range with the reported-change range.
            c, p, delta = (Decimal(str(v)) for v in (current, previous, change))
            half = Decimal("0.005")
            if p <= half:
                return {**fallback, "reason": "numeric rounding leaves denominator uncertain"}
            lower = (max(Decimal(0), c - half) / (p + half) - 1) * 100
            upper = ((c + half) / (p - half) - 1) * 100
            lower, upper = max(lower, delta - half), min(upper, delta + half)
            if lower > upper + Decimal("0.000001"):
                return {**fallback, "reason": "numeric evidence is internally inconsistent"}
            intervals.append((lower, upper))
        lower = max(i[0] for i in intervals)
        upper = min(i[1] for i in intervals)
        if lower > upper + Decimal("0.000001"):
            return {**fallback, "reason": "conflicting numeric captures require review"}
        amount = Decimal(match["amount"])
        if amount < 0 or amount > 1000000:
            return fallback
        signed = -amount if match["direction"] == "fell" else amount
        half_unit = Decimal(1).scaleb(amount.as_tuple().exponent) / 2
        # Boundary ties are allowed conservatively; signed direction is checked
        # independently so a tiny rise cannot validate a rounded drop.
        direction_impossible = lower >= 0 if match["direction"] == "fell" else upper <= 0
        epsilon = Decimal("0.000001")
        if (direction_impossible or upper < signed - half_unit - epsilon
                or lower > signed + half_unit + epsilon):
            return {"claim_id": claim["claim_id"], "outcome": "remove",
                    "reason": "claimed percentage contradicts scoped captured evidence"}
        return {**fallback, "reason": "numeric percentage matches; semantic/confidence review remains"}
    return verify
