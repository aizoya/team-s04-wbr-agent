# Team Integration Checklist

Internal finish: October 8, 2026, 11:59 a.m. Pacific

Franklyn's runner/verifier work is intended to be integration-ready before team inputs arrive.

## Franklyn — local implementation ready; final acceptance still open

Latest draft: PR #4, `build/s04-analyst-loop-adapter-20261007`, stacked on PR #3
and the original PR #2 runner branch. No merge or approval is implied.

Latest local gate: 95 tests and both synthetic demos PASS. The nested analyst
adapter, structured evidence/warnings, request-ID citations, causal-check repair,
bounded numeric-contradiction gate and offline capture replay are implemented.
See `docs/LAKSHMI_CONTRACT_INTEGRATION_2026-10-07.md` for limits and source blobs.
Correct numeric matches and unknown prose remain reviewed, not automatically
kept. Real-data semantic verification is NOT complete.

Ready:
- strict complete/partial rules;
- fail-closed fallback verifier and bounded numeric contradiction check;
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

Still owed by Franklyn: real capture replay, a reviewed semantic verifier that can
justify keep outcomes, confidence-policy reconciliation, renderer binding,
integrated failure/partial tests and final reproducible demo acceptance.

## Lakshmi — integration handoff needed

Already inspected: `work/Lakshmi-data-tools` source and authored golden answer
keys. Tool names are `get_weekly_metric`, `get_breakdown`, `get_delivery_signals`;
structured refs/warnings and nested analyst shape are supported locally. Her
reported 18 real-data checks and 9 offline tests are not our independently
replayed AWS acceptance.

Still provide:
- representative successful tool envelopes;
- representative partial/error envelopes;
- real Olist/Athena outputs for acceptance.

AWS console profile and narrow permission repair were completed; successful
teammate sign-in/reset, SDK authentication and service smoke tests remain
unconfirmed. No credentials belong in fixtures, Git or group messages.

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
2. Bind Maxime's renderer callback to `run_analyst_week(..., renderer=...)` for
   captured analyst-loop runs; keep `run_wbr` for the original tool orchestration.
3. Run `python3 scripts/verify.py`.
4. Run synthetic complete and partial integration.
5. Replay saved nested responses with `demo/run_captured_analyst.py`; numeric
   contradictions must be removed, and unknown semantics must remain reviewed.
   Use `demo/run_real_olist_acceptance.py` only with independently trusted exact
   answer-key statements, never answer keys generated from claims under test.
6. Run the real 2018-08-20 incomplete-week case and independent-tool-failure case.
7. Run real-data/Athena parity acceptance.
8. Record mocked/local evidence separately from real AWS evidence.
9. Request teammate review.
10. Do not merge solely because tests pass.

## Human/team decisions still open

Do not silently freeze:
- final review of the already-inspected structured evidence contract;
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

