# S04 Well-Architected review — 2026-10-08

Status: **NO-GO for final submission acceptance; GO for offline preparation.**
Submission deadline supplied by Franklyn: October 11, 2026, 11:59 AM Pacific.
Protect the existing project and teammate branches. This is a targeted review, not a replacement architecture or permission to merge/deploy/spend.

## Verified state

Read-only AWS plugin authentication was restored on October 8. STS verified account 704554708405, IAM identity aizoya-admin. Successful API receipts support the following observations:

- Region us-east-2: Athena workgroup S04-WBR ENABLED, engine version 3, enforced workgroup configuration; output results prefix in the existing results bucket; SSE_S3 encryption; 104857600-byte (100 MiB) per-query scan cutoff. CloudWatch query metrics are disabled.
- Glue GetTables for s04_wbr returned **zero tables**.
- Source bucket contains only two zero-byte markers, fixtures/ and source/. No source dataset objects were present at inspection. Results bucket contains four small CSV/metadata objects from October 2; their contents were not read and do not prove Olist acceptance.
- Both S04 buckets are in us-east-2, default AES256 encryption, and all four bucket public-access block settings true. GetBucketPolicyStatus returned NoSuchBucketPolicy for both. This is not proof of public exposure; IAM/ACL/account controls still matter. Explicit bucket-level TLS-only policy was not established.
- Nova Micro inference profile us.amazon.nova-micro-v1:0 ACTIVE; foundation-model availability reports authorization AUTHORIZED, agreement/entitlement/region AVAILABLE. No model was invoked. Other listed profiles are not evidence of teammate invocation permission.
- Lakshmi's existing managed S04 policy and inline October 7 repair were read back. They scope S3 to the two project buckets, Athena to S04-WBR, Glue to s04_wbr, and Nova Micro to the exact profile/destination model ARNs. Groups list empty; IAMUserChangePassword also attached. Effective access is not proven: SCPs, boundaries, session policy and runtime credential selection were not fully tested. Data-engineering permissions are broader than a future read-only runtime role; retain ownership and do not change them during this review.
- AIZOYA Zero Spend Alert: monthly USD1 budget, credits included, reported actual USD0, last billing update October 7. ACTUAL > USD0.01 notification exists with one EMAIL subscriber. VisionProof budget reports USD0.006 excluding credits; it is a different budget, not an S04 allocation.
- **Remaining credits are UNKNOWN.** Budget calculated spend is delayed and its credit treatment cannot establish a credit balance or a spending authorization.

GitHub inspection: PRs #1–#4 open/unmerged; PR #4 draft stacked on #3/#2. PR #4 inspection head 4fd385b3f5d8ec8ca99329907a58e0acce7e4c06; no reviews returned. No renderer branch visible in inspected branch inventory. No S04 issue returned by issue search. No S04 record returned by Linear search; this document prepares the exact canonical tracking update rather than inventing a PCC/Linear receipt.

## Existing architecture and review scope

Lakshmi: Olist preparation → local DuckDB or S3/Glue/Athena → three query tools → Strands/Bedrock analyst → report_draft + request_id-indexed evidence_log.
Franklyn: captured analyst adapter → fail-closed numeric/claim verifier → renderer boundary and acceptance harness.
Maxime: concept and assigned implementation; renderer ownership/availability must be confirmed rather than assumed.

Reviewed Lakshmi source: analyst.py 58fed18663883f56d524d9ca503ee09907889794; config.py aa0ed680dd483614e0d7359e2c6dd797b46363df; backend.py aa562378bd17215d968bd32ccbff9f29626428e0; requirements.txt d5fd59a69ce234808e97d6c611f8a8542da7cd5c.
No teammate source edits. The existing verified-fact policy remains opt-in OFF by default.

## Prioritized findings

| Priority | Finding / acceptance action | Owner |
|---|---|---|
| MUST FIX BEFORE SUBMISSION | Load validated data and create expected Athena tables; compare all three tools with golden outputs. Existing source bucket/Glue are empty. | Lakshmi |
| MUST FIX BEFORE SUBMISSION | Capture one reviewed-model analyst run with actual SDK credentials, exact model/settings, tool envelopes, token usage, query bytes, elapsed time, and complete/partial verification outputs. Console login alone is not SDK authentication. Paid invocation/query requires spending approval. | Lakshmi; Franklyn acceptance |
| MUST FIX BEFORE SUBMISSION | Agree final evidence refs and confidence policy; validate real captures through runner/verifier; confirm renderer integration, review stacked PRs through established process, and record complete demo + failure segment. | Franklyn + Lakshmi; Maxime assigned integration |
| MUST FIX BEFORE SUBMISSION | Establish remaining eligible credits and an explicit small live-test spending ceiling before new paid runs. Budget alerts are not a verified hard spending cap. | Franklyn |
| OPTIONAL LOW-RISK IMPROVEMENT | Offline configuration preflight added in this PR; rejects accidental DuckDB live mode, unknown backend, unreviewed model/region/data boundary, and failure simulation. No environment values or credentials printed. Invoke explicitly; it does not alter the analyst. | Franklyn — implemented |
| OPTIONAL LOW-RISK IMPROVEMENT | Handle initialization/model construction errors at the analyst boundary: model/Agent construction currently precedes its try block. Define privacy-safe error codes and test with injected failure. Avoid unsynchronized edits on teammate branch. | Lakshmi; Franklyn adapter coordination |
| OPTIONAL LOW-RISK IMPROVEMENT | Review explicit SDK connect/read timeouts, bounded retries and query cancellation after transport errors. Current 30-second polling deadline is not an end-to-end wall-clock guarantee. Outer retry may start another query after an ambiguous transport failure. | Lakshmi |
| OPTIONAL LOW-RISK IMPROVEMENT | Record existing Athena Statistics.DataScannedInBytes/engine time and model token usage from authorized captures; use summary-only diagnostics, keep prompts/rows/transcripts private. | Lakshmi; Franklyn evidence |
| DEFER UNTIL AFTER SUBMISSION | Separate read-only runtime role from data deployment permissions, scoped temporary credentials, TLS-only bucket policy, result lifecycle, monitoring enablement, lockfile/version pinning after recording a working environment, service-level dashboards. Any infrastructure/permission change needs approval. | Franklyn architecture + Lakshmi |
| DEFER UNTIL AFTER SUBMISSION | Broader refactor, more models, caching/reuse changes, new telemetry vendors, automated background workloads. | Team |

## Six-pillar assessment

Operational excellence: local repeatable gate and replay exist; added no-network settings diagnostics. Preserve exact commit, command, scenario, output label and raw private capture for submission evidence. No new telemetry service.
Security: existing bucket encryption/public blocking and scoped project policies verified; no new credentials or grants. Diagnostic output is allowlisted booleans/status/codes. Secrets and private data must not enter GitHub or public demo receipts.
Reliability: complete/partial synthetic paths pass. Real AWS failure recovery unverified; analyst initialization errors and SDK timeout scope need owner review. Use deterministic synthetic fallback, visibly labeled SYNTHETIC; no claim that it is a live cloud run.
Performance: local gate runtime is not Bedrock/Athena latency. Actual scan volume, model turns/tokens and end-to-end latency UNKNOWN until an authorized capture. Reviewed tools target preaggregated weekly data; hosted query plan and scan efficiency remain unproven.
Cost: 25-tool-call configured analyst budget, MAX_RETRIES=1 in tool backend, 40 main turns plus a five-turn finalization path in analyst source. These are not USD caps or proof of SDK enforcement. At most two logical backend attempts per executed tool under this code path; AWS API/internal model retries, token sizes, failures and polling can add exposure. Athena's 100 MiB cutoff is per query, not a total project cap. Cost formula: model input/output tokens × current regional rates + billed Athena bytes + S3 storage/requests/other services. No numeric credit balance or whole-run price asserted.
Sustainability: replay captured evidence and synthetic fixtures offline; avoid repeated paid calls during presentation, polling loops outside bounded runs, or extra compute merely for polish.

## Repeatable runbook (zero AWS/model calls)

From repository root:
```sh
python3 scripts/verify.py
python3 scripts/check_health.py
```

Before an approved live test, set nonsecret reviewed settings in the teammate's runtime:
```sh
export WBR_BACKEND=athena
export WBR_AWS_REGION=us-east-2
export WBR_ATHENA_WORKGROUP=S04-WBR
export WBR_ATHENA_DATABASE=s04_wbr
export WBR_MODEL_ID=us.amazon.nova-micro-v1:0
unset WBR_SIMULATE_FAILURE
python3 scripts/check_health.py --live
```
A PASS checks settings only. It does not authenticate, query, invoke, authorize spending, or attest deployment. Actual code reads WBR_AWS_REGION; setting AWS_REGION alone does not select its region.

Fallback:
```sh
python3 demo/run_synthetic_demo.py --scenario complete
python3 demo/run_synthetic_demo.py --scenario partial
```
Use recorded, previously validated captures only with provenance and the appropriate replay label; raw agent narratives are not verified facts. Never rerun paid workloads simply to regenerate screenshots.

Recovery: stop on access denied, empty tables, model initialization failure, deadline or cost uncertainty. Preserve private evidence; do not add permissions or loop retries ad hoc. Revert optional diagnostic files if necessary; existing runner/model/data behavior is unchanged.

## Test evidence and change record

Baseline: 107 tests + both synthetic demos PASS.
After change: **116 tests + both synthetic demos PASS**, python3 scripts/verify.py exit 0.
Nine diagnostic tests include secret-canary non-disclosure, unchanged input, region-key correctness, accidental local mode, unknown backend/model/data boundary and live-only failure simulation.
python3 scripts/check_health.py: exit 0; OFFLINE_CONFIGURATION_ONLY, cloud/credits/spending booleans false.
No real Olist/Strands/Athena/Bedrock run or paid workload performed. New helper/CLI is opt-in; no existing runtime behavior changed. Published on existing Franklyn PR #4; no merge/deployment.

## Exact tracking update

S04 — Well-Architected review completed October 8. AWS read-only access restored; account and existing secured buckets/workgroup verified. Source bucket only empty markers; Glue s04_wbr zero tables. Nova Micro metadata available; runtime untested. Budget alert/subscriber verified; remaining credits unknown. Offline gate improves 107→116 tests, synthetic complete/partial PASS. Franklyn diagnostics/review added to PR #4; teammate branches preserved. Lakshmi owns data upload/catalog/tool parity and live capture; Maxime assigned integration/renderer status needs confirmation; Franklyn owns review, budget approval, acceptance and submission. NO-GO final acceptance pending real-data integration, approved live test, renderer/demo evidence and PR review. No spend, permissions expansion, merge, deployment or external messages authorized/performed by this review.

## Primary references

- AWS Well-Architected framework: https://docs.aws.amazon.com/wellarchitected/latest/framework/welcome.html
- Athena workgroup configuration: https://docs.aws.amazon.com/athena/latest/APIReference/API_WorkGroupConfiguration.html
- Athena scan limits: https://docs.aws.amazon.com/athena/latest/ug/workgroups-setting-control-limits-cloudwatch.html
- Nova Micro model card: https://docs.aws.amazon.com/bedrock/latest/userguide/model-card-amazon-nova-micro.html

Resource observations above come from successful read-only API receipts, not documentation assumptions.

## Follow-up runner reliability fix — October 8

Franklyn-owned adapter now catches ordinary exceptions raised by the single analyst call (including model initialization before the analyst's own try block) and returns a partial report with empty evidence and the fixed code ANALYST_CALL_FAILED. It does not retry or copy exception text. Malformed returned contracts still fail validation; KeyboardInterrupt remains interruptible. Lakshmi's agent source is unchanged. Three added tests exercise these boundaries and renderer invocation; final local gate: **119 tests + both synthetic demos PASS**, scripts/verify.py exit 0. The earlier 116-test observation is the diagnostics-only checkpoint. AWS data, paid live run, credits, renderer and review blockers remain unchanged. Canonical tracking update: runner initialization recovery implemented and tested on PR #4; no paid calls, merge or deployment.
