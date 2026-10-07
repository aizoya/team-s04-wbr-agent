# Real Olist Demo Acceptance

This is the acceptance path for the judge-facing demonstration. It is deliberately separate from the deterministic synthetic unit/demo path.

## Required scenarios

### 1. Planted real-Olist scenario

Label: `PLANTED_REAL_OLIST`.

Use actual Olist-derived weekly rows plus an explicitly disclosed planted change with a trusted answer key. The fixture must come from Lakshmi's final tools/outputs; do not invent judge-facing numbers in the runner workstream.

The demo should show roughly 30 seconds of investigation:
1. headline revenue change;
2. order-count check;
3. order-value check when appropriate;
4. state breakdown;
5. category breakdown;
6. evidence-backed claim draft and verifier result.

### 2. Real incomplete week

Label: `REAL_OLIST_INCOMPLETE`.

Use the week starting 2018-08-20. The expected behavior is not to present the drop as a normal business collapse. The report must remain partial / incomplete according to the final tool policy and must not invent a replacement value or causal explanation.

### 3. Independent tool failure

One query/tool may fail while unaffected tool envelopes survive. The failure must retry once, preserve the final valid error envelope, and keep the overall report partial rather than fabricated or all-or-nothing.

## Runner

Once Lakshmi's final envelopes and answer keys are committed or supplied for integration:

```bash
python3 demo/run_real_olist_acceptance.py --fixture <fixture.json>
```

The fixture must contain:
- `label`
- `expected_tool_names`
- `tool_results`
- `claims`
- `answer_key`

Each answer-key claim supplies an expected verifier `outcome` and non-empty `required_evidence_refs`.

## Evidence rule

A revised script or fixture template is not evidence of a successful real-data run. Record separately:
- local deterministic/synthetic test results;
- real DuckDB/Olist acceptance;
- Athena parity;
- Lakshmi service-level AWS access;
- teammate acceptance.

Until Lakshmi's final tools, planted scenario, answer key, and representative envelopes are available, the real-Olist run remains BLOCKED, not passed.
