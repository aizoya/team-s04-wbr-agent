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
- zero-dependency local quality gate.

No additional Franklyn-side feature work should be needed before team integration unless a teammate exposes an interface mismatch.

## Lakshmi — integration handoff needed

Provide:
- final tool names if different from the temporary runner configuration;
- final tool-specific `data` payload shapes;
- final `evidence_refs` structure;
- representative successful tool envelopes;
- representative partial/error envelopes;
- real Olist/Athena outputs for acceptance;
- final decisions for weeks/timezone, revenue/qualifying-order rules, and review coverage when ready.

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
5. Run real-data acceptance against Lakshmi's outputs.
6. Record mocked/local evidence separately from real AWS evidence.
7. Request teammate review.
8. Do not merge solely because tests pass.

## Human/team decisions still open

Do not silently freeze:
- exact comparison weeks/timezone;
- revenue and qualifying-order rules;
- review coverage policy;
- confidence policy.

## Gates

Still require explicit approval for:
- spending;
- new credentials or permissions;
- production changes;
- public repository publication;
- submission;
- merge if team review requirements are not met.
