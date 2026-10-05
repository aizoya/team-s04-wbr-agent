# Runner / Verifier Integration Boundary

Owner: Franklyn Rosario, MBA-ITM

## Scope

This branch implements the mockable runner/verifier path only. It does not
implement Lakshmi's Olist profiling, Athena SQL, weekly_metrics table, three
data tools, analyst loop, or final tool payload shapes. It also does not
implement Maxime's final renderer.

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

The output is explicitly labeled `SYNTHETIC`. The category/state payloads in
the demo are placeholders only; they do not freeze Lakshmi's final data shapes.

## Still unresolved / owned by the data workstream or team

Do not freeze these in runner code:

- exact comparison weeks and timezone;
- revenue definition and qualifying-order rules;
- review canonicalization/coverage details;
- tool-specific `data` payloads;
- final `evidence_refs` structure;
- confidence policy.

## Real AWS boundary

The tests and demo on this branch are local/mocked and require no AWS
credentials. Real-data acceptance remains pending Lakshmi's tool outputs.
