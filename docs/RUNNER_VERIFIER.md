# Runner / Verifier Integration Boundary

Owner: Franklyn Rosario, MBA-ITM

## Scope

This branch implements the mockable runner/verifier path only. It does not
implement Lakshmi's Olist profiling, Athena SQL, weekly tables, three
data tools, analyst loop, or final tool payload shapes. It also does not
implement Maxime's final renderer.

Metric semantics are finalized separately in `docs/METRIC_CONTRACT.md`.
The runner intentionally treats tool-specific `data` payloads as opaque.

## Current orchestration

1. Call each configured tool through the approved external envelope.
2. Retry an exception, malformed result, or explicit error exactly once.
3. After retry exhaustion, preserve an error envelope and continue honestly.
4. Validate analyst claims against the approved claim contract.
5. Verify evidence availability and unsupported causal language.
6. Apply keep / downgrade / flag / remove outcomes.
7. Pass structured verified results to the renderer callback when available.
8. Without a renderer, expose the same payload through `renderer_input`.

## Status / evidence adapter

Internal metric helpers intentionally use:

- `OK | PARTIAL | UNAVAILABLE`
- singular `evidence_ref`

External tools intentionally use:

- `ok | partial | error`
- plural `evidence_refs`

Use `metric_to_external` and `external_to_metric`; do not treat the two
representations as identical.

## Completion rule

A mocked run is `complete` only when all configured V1 tool boundaries are
present, each expected tool returns `ok` with evidence, and every valid claim
is verified as `keep`. Empty, incomplete, malformed, unavailable, missing-
evidence, flagged, or removed results remain `partial`.

## Synthetic demo

Run:

```bash
python3 demo/run_synthetic_demo.py --scenario complete
python3 demo/run_synthetic_demo.py --scenario partial
```

The synthetic fixture remains for deterministic contract/unit tests. The
judge-facing demo should use real Olist weeks plus a planted scenario and the
real incomplete week starting 2018-08-20.

## Still unresolved / owned by the data workstream or team

Do not freeze these in runner code:

- tool-specific `data` payloads;
- final `evidence_refs` structure;
- confidence policy.

## Finalized metric contract

The runner does not conflict with the final V1 metric contract:

- revenue orders exclude canceled, unavailable, and unpaid orders;
- product revenue excludes freight;
- reviews are averaged to one score per order;
- review coverage is `review_count / orders`;
- weeks start Monday;
- complete analysis window is 2017-01-30 through 2018-08-13;
- category/state groupings are owned by the data layer;
- totals come from `weekly_metrics`, while category comparisons come from
  `weekly_category_metrics`.

## Real AWS boundary

The tests and demo on this branch are local/mocked and require no AWS
credentials. Real-data acceptance remains pending Lakshmi's tool outputs and
AWS parity checks.
