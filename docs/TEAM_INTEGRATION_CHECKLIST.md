# Team Integration Checklist

Internal finish: October 8, 2026, 11:59 a.m. Pacific

Franklyn's runner/verifier work is intended to be integration-ready before team inputs arrive.

## Franklyn — complete on branch

Branch: `build/franklyn-runner-verifier-v2`

Ready:
- strict complete/partial rules;
- evidence-aware verifier;
- unsupported-causal-language guard;
- one-retry failure handling;
- explicit internal/external metric adapter;
- mockable tool -> analyst -> verifier -> renderer orchestration;
- renderer input fixture;
- complete/partial synthetic demo;
- zero-dependency local quality gate;
- final metric contract aligned to Lakshmi's data foundation;
- explicit zero-denominator KPI policy (`null`/unavailable, never infinity or fabricated zero);
- founder-only AWS bootstrap packet in `docs/AWS_LAKSHMI_BOOTSTRAP.md`;
- real-Olist acceptance harness in `demo/run_real_olist_acceptance.py`.

No additional Franklyn-side feature work should be needed before team integration unless a teammate exposes an interface mismatch.

## Lakshmi — integration handoff needed

Provide:
- final tool names if different from the temporary runner configuration;
- final tool-specific `data` payload shapes;
- final `evidence_refs` structure;
- representative successful tool envelopes;
- representative partial/error envelopes;
- planted scenarios and answer keys;
- real Olist/Athena outputs for acceptance.

Finalized metric semantics are now canonical in `docs/METRIC_CONTRACT.md`.

The runner treats `data` as opaque and should not require Lakshmi to conform to a runner-invented data schema.

## Maxime — integration handoff needed

Provide:
- renderer callable/module boundary;
- expected renderer input requirements if they differ from `renderer_input`;
- output-layer tests;
- behavior for complete, partial, warning, flagged, downgraded, and unavailable material;
- README/run instructions for final report generation.

The current deterministic example is `fixtures/renderer_input_complete.json`.

## Integration sequence

1. Validate Lakshmi envelopes without changing their data payload semantics.
2. Bind Maxime's renderer callback to `run_wbr(..., renderer=...)`.
3. Run `python3 scripts/verify.py`.
4. Run synthetic complete and partial integration.
5. Run planted-scenario acceptance on real Olist weeks with `demo/run_real_olist_acceptance.py`.
6. Run the real 2018-08-20 incomplete-week case and independent-tool-failure case.
7. Run real-data/Athena parity acceptance.
8. Record mocked/local evidence separately from real AWS evidence.
9. Request teammate review.
10. Do not merge solely because tests pass.

## Human/team decisions still open

Do not silently freeze:
- final `evidence_refs` structure;
- confidence policy;
- any future tool-specific payload fields not covered by the metric contract.

## Gates

Still require explicit approval for:
- spending;
- new credentials or permissions;
- production changes;
- public repository publication;
- submission;
- merge if team review requirements are not met.
