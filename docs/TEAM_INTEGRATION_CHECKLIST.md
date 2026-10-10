# Team Integration Checklist

## Current status — October 9, 2026, 11:28 AM Pacific

- Data foundation: five uploaded Parquet objects and five Glue tables verified.
  Console access confirmed by Lakshmi; temporary CLI/boto3 sign-in is teammate-
  reported successful. No permanent access keys were created for this work.
- Athena tool parity: published evidence contains 13/13 equal normalized
  DuckDB/Athena comparisons. AWS independently confirms the 11 recorded queries
  succeeded: 636,489 scanned bytes and 5,175 engine ms. Local elapsed 98.3 s
  and USD0.000525 query cost are reported/estimated, not an invoice or local
  independent replay. Preserve the existing file; no parity rerun is needed.
- Approval timing exception: parity query timestamps are October 9 morning,
  outside the prior October 8 expiry. No renewal is established; reconcile
  separately without invalidating the technical evidence or claiming approval.
- Bedrock: one six-scenario batch (S1/S2/S3/S4/S5/S7, one trial each) approved
  with USD0.75 total incremental ceiling, ending after one batch or October 9,
  11:59 PM Pacific. S1 first; stop on unexpected failure. This is conditional
  on verified code guards before execution, not a service-enforced dollar cap.
- MUST FIX before live batch: next-call token/cost reservation, global finite
  model attempt accounting including retries, stop on graded failures, and
  per-run raw evidence_log plus individual query receipts in saved JSON.
  Existing published evaluator does not yet prove these conditions.
  Lakshmi owns her corrections; no source changes made on her branch.
- Nova Micro US profile is ACTIVE; scoped IAM simulation permits the requested
  invocation actions and all three destination models. Live invocation is
  untested; do not expand permissions without an actual scoped denial/approval.
- Maxime: renderer callable, immutable handoff commit, report tests and final
  instructions still need receipt/review. Existing output-layer ownership is
  confirmed; do not duplicate or override in-flight implementation.
- Franklyn: review guards/real captures, reconcile verifier/confidence policy,
  bind reviewed renderer, accept complete/partial/error demonstrations, and
  follow team review/merge/submission gates. Full submission remains NO-GO.

Authoritative details and source blobs:
docs/WELL_ARCHITECTED_REVIEW_2026-10-08.md.
Previous dated checkpoints are historical, not current-state assertions.

Original internal finish target (missed): October 8, 2026, 11:59 a.m. Pacific
Working submission cutoff: October 11, 2026, 11:59 a.m. Pacific

Franklyn's runner/verifier work is intended to be integration-ready before team inputs arrive.

## Franklyn — local implementation ready; final acceptance still open

Latest draft: PR #4, `build/s04-analyst-loop-adapter-20261007`, stacked on PR #3
and the original PR #2 runner branch. No merge or approval is implied.

Latest local gate: 123 tests and both synthetic demos PASS. Offline settings diagnostics
and privacy-safe analyst initialization recovery are also implemented.
See `docs/WELL_ARCHITECTED_REVIEW_2026-10-08.md` for the six-pillar assessment,
read-only AWS evidence, costs, owner actions and submission NO-GO conditions. The nested analyst
adapter, structured evidence/warnings, request-ID citations, causal-check repair,
bounded numeric-contradiction gate and offline capture replay are implemented.
See `docs/LAKSHMI_CONTRACT_INTEGRATION_2026-10-07.md` for limits and source blobs.
Correct numeric matches and unknown prose remain reviewed by default. An
explicit opt-in policy candidate can keep only narrowly verified numeric facts
after team review; see `docs/TOMORROW_HANDOFF.md`. Real-data semantic acceptance
is NOT complete. The teammate execution handoff proposes Lakshmi owning actual
data/agent receipts and Maxime coordinating renderer/integration while Franklyn
is driving. Lakshmi's data ownership and Maxime's output-layer ownership are
confirmed; expanded integration coordination acceptance remains unconfirmed.

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

AWS console/profile repairs and temporary local-login permissions were completed.
Lakshmi confirmed console and CLI/boto3 access; Athena parity is independently
cross-checked against published captures and AWS execution metadata. Bedrock
live acceptance remains pending conditional guard verification. No credentials belong in fixtures, Git or group messages.

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


## October 8 morning AWS checkpoint — historical

AWS plugin access restored; STS account/identity verified. S04 buckets have default
encryption/public-access blocking; Athena enforces a 100 MiB scan cutoff. Source
bucket currently contains only two zero-byte markers; Glue s04_wbr has zero tables.
Nova Micro metadata reports available/authorized; runtime invocation remains
untested. A budget email notification exists; remaining eligible credits are
unknown. No new teammate emails or S04 channel messages were returned by the
October 8 morning searches; this does not establish their current availability.
Do not duplicate teammate uploads or infer completion. Final submission remains
NO-GO until data/catalog parity, approved live evidence, renderer integration,
reviewed verifier policy and reproducible demo acceptance are recorded.

## Team communication and ownership reconciliation — October 8

Authorized status email sent from franklyn@aizoya.com to Lakshmi Bharathy Kumar
and Maxime Gillot; Outlook send action returned success (Sent Items search may
lag and did not yet return the new message). Slack update posted successfully:
https://awsusers.slack.com/archives/C0C648P9SV8/p1791478412697219
No credentials included. Requested branch/commit, completed items, blockers and
ETA; preserved separate spending, permissions, merge and submission gates.

Recipient-history verification found Maxime's October 4 email explicitly
accepting final report/output-layer ownership, tests, integration support and
README. This corrects any earlier wording that his renderer ownership itself
was unconfirmed. His current renderer implementation/delivery remains unverified;
acceptance of the newer expanded coordination proposal is not assumed. Lakshmi's
October 7 report confirms her data/agent work and pending AWS integration.
No new teammate acknowledgement of today's handoff is established.

## October 8 afternoon checkpoint — historical

Five Parquet objects are verified present in the agreed source/fixtures prefixes;
this supersedes the earlier empty-bucket observation. Glue s04_wbr still returns
zero tables. Object existence does not establish schema or golden-output parity.
Preserve Lakshmi's in-flight catalog work.

The approved five-action Ohio Athena console discovery policy was applied and
read back; IAM simulations passed positive and negative boundaries. No live
teammate console acceptance is established. No DeleteTable was added.

Latest offline gate: 123 tests and both synthetic demos PASS. Four adapter-path
failure/completion regression tests were published at
c5f996ae922fcf5f6ea9697434e57cf60f49dfe3 and read back. No runtime changes.

The approved accountability email and Slack message were sent once. Slack receipt:
https://awsusers.slack.com/archives/C0C648P9SV8/p1791497219968399
Current evidence does not establish full integration or submission readiness.
See docs/TOMORROW_HANDOFF.md for the latest acceptance sequence and remaining
owners. Historical checkpoints below/above are not current-state assertions.
