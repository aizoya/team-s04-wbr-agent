# S04 Well-Architected review — 2026-10-08

Status: **NO-GO for final submission acceptance; GO for offline preparation.**
Submission deadline supplied by Franklyn: October 11, 2026, 11:59 AM Pacific.
Protect the existing project and teammate branches. This is a targeted review, not a replacement architecture or permission to merge/deploy/spend.


## Latest checkpoint — October 8 afternoon

This summary supersedes historical observations below where state has changed.

- All five expected Parquet objects now exist in the agreed S3 layout (uploaded
  3:52–3:55 PM Pacific); contents/parity remain unverified. Glue s04_wbr still has
  zero tables. Do not duplicate Lakshmi's in-flight setup.
- Approved Ohio Athena console read-only policy repair was applied/read back and
  positive/negative IAM simulations passed, as recorded below. Console/runtime
  acceptance is not established.
- Maxime's report/output-layer ownership was confirmed by his October 4 email;
  implementation delivery and expanded coordination acceptance remain unverified.
- Latest offline gate: 123 tests plus both synthetic demos PASS; four additional
  adapter-boundary regression tests, no runtime changes, published and read back
  at c5f996ae922fcf5f6ea9697434e57cf60f49dfe3.
- Approved accountability email and Slack sent once; Slack receipt:
  https://awsusers.slack.com/archives/C0C648P9SV8/p1791497219968399
- Final acceptance remains NO-GO. Data/catalog parity, approved live capture,
  renderer integration, verifier-policy review and final demo evidence are open.
  Credits and total live-run cost remain unknown. No new paid workload, merge or
  deployment occurred during this afternoon checkpoint.

## Initial verified state — historical

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

## 11:28 AM Pacific recheck — October 8

Read-only AWS recheck succeeded: s04_wbr still has zero tables; source bucket still
contains only two zero-byte markers. October 8 sender-filtered Outlook searches
returned no Lakshmi/Maxime replies; S04 channel search returned only our earlier
status post. Branch inventory remains the six existing branches, with no renderer
branch visible. PR #4 is draft/open/unmerged and mergeable; mergeability is not
review approval. Maxime's previously confirmed output ownership is now corrected
in the PR description. Existing 119-test offline evidence remains unchanged; no
new live tests, infrastructure mutation, paid workload or follow-up message.
Submission NO-GO remains. Next dependency: teammate data/renderer receipts and
review, followed by separately approved bounded live testing and acceptance.

## Lakshmi Athena denial — October 8, 12:20 PM Pacific diagnosis

Lakshmi reported inability to use the workgroup; this is now a confirmed active
integration blocker, not merely missing execution evidence. Her current attached
S04 policy contains the requested source/results S3 list/read/write, scoped Glue
table create/read, and five Athena actions. IAM simulation allows those Athena
actions for S04-WBR in us-east-2; simulation is not runtime acceptance.
CloudTrail records aws-hackathon-s04-lakshmi GetWorkGroup AccessDenied at
19:11:10 UTC in us-east-2 (event 6e6432e3-7113-4a81-9133-d2409fd0738c).
Region mismatch is therefore ruled out for that recorded attempt. Request
parameters/resource ARN were absent from the retrieved event, so the exact
workgroup target and root cause remain unknown. Other-region/primary-workgroup
simulations were implicitly denied, but do not prove she requested those targets.
Next: exact selected workgroup/full error or a direct read-only GetWorkGroup test
using her existing configured credentials. No new permissions, credentials or
paid query were created. Proposed source and fixture table-prefix layout is
compatible with the architecture; golden fixtures must remain separately labeled.

## Approved Athena console discovery repair — October 8, 12:51 PM Pacific

Franklyn explicitly approved the five-action read-only addition at 12:50 PM.
Applied a new dedicated inline policy S04-WBR-Lakshmi-ConsoleReadOnly-20261008
to aws-hackathon-s04-lakshmi after verifying account/user and confirming that the
new policy did not already exist. Existing teammate policies were preserved.
PutUserPolicy succeeded; GetUserPolicy readback matched exactly.

- athena:ListWorkGroups and athena:ListDataCatalogs: Resource *, with
  aws:RequestedRegion equal to us-east-2.
- athena:ListDatabases, athena:ListTableMetadata, athena:GetTableMetadata:
  arn:aws:athena:us-east-2:704554708405:datacatalog/AwsDataCatalog, same region condition.

IAM principal simulations: all five intended actions allowed; discovery in
us-west-2 denied, metadata on UnapprovedCatalog denied, Glue DeleteTable on
s04_wbr/weekly_metrics denied. These are IAM simulation results, not live console
acceptance. Ohio discovery can reveal workgroup/catalog names; it does not grant
query access outside the pre-existing S04-WBR policy. Glue database access remains
as previously scoped. No DeleteTable, new keys, paid queries, model invocations,
or data changes. Next: Lakshmi refreshes Athena in Ohio, selects S04-WBR, and
confirms console access. Rollback if approved/needed: remove only this new inline
policy, not existing managed or repair policies.

## Approved Glue catalog console read repair — October 8, 4:10 PM Pacific

Lakshmi reports that the workgroup list now loads and S04-WBR can be selected:
this is teammate-reported confirmation of the earlier Athena discovery repair.
The left panel then denies glue:GetCatalogs on the Ohio account catalog. Her
forwarded message contains an unresolved selectable/not-selectable placeholder;
database dropdown usability is therefore unknown.

Franklyn approved the proposed two-action addition at 4:10 PM Pacific ("A").
Account/target IAM user verified; a dedicated previously absent inline policy
S04-WBR-Lakshmi-GlueCatalogReadOnly-20261008 was applied to
aws-hackathon-s04-lakshmi. Existing policies preserved. Exact grant:
glue:GetCatalogs and glue:GetCatalog, resource
arn:aws:glue:us-east-2:704554708405:catalog, with aws:RequestedRegion us-east-2.
PutUserPolicy succeeded and GetUserPolicy matched the proposed JSON.

IAM principal simulations allow both actions on the Ohio account catalog;
deny both on us-west-2 and another account; Glue DeleteTable remains denied.
Simulation is not live console acceptance. No query/write/delete permissions,
keys, paid query/model call or data/catalog mutation were added/performed.
Next: Lakshmi refreshes Athena in Ohio with S04-WBR selected and confirms whether
the left panel and s04_wbr dropdown now load. Stop and reconcile any new denied
action before expanding permissions. Rollback if authorized: remove only the
new dedicated inline policy.

## Five-table catalog verification — October 8, approximately 4:19 PM Pacific

Lakshmi confirmed that the Ohio Athena left panel now loads with S04-WBR selected,
s04_wbr is selectable and five created tables appear. Read-only Glue GetTables
independently verifies exactly weekly_metrics, weekly_category_metrics,
order_facts, golden_weekly_metrics and golden_weekly_category_metrics, each an
EXTERNAL_TABLE pointing to its agreed source/fixture S3 prefix. This supersedes
the earlier zero-table observation. Schema/content/parity are not yet accepted.

Athena GetWorkGroup verifies S04-WBR ENABLED, enforced results configuration,
SSE_S3 and the existing 104857600-byte per-query scan cutoff. No query was run
during verification. Lakshmi requests one reconciliation SELECT for counts,
revenue totals and date ranges across these five tables; her scan/cost estimate
is not independently measured. New spending approval remains pending. Do not
infer authorization for retries, additional queries or Bedrock runs.

## Founder-approved single reconciliation query — October 8, 4:20 PM Pacific

Franklyn approved ("A") the concrete one-query proposal and communicating it
to Lakshmi. Authorization: Lakshmi may execute exactly one read-only reconciliation
SELECT today, October 8 Pacific, in account 704554708405, us-east-2, S04-WBR,
database s04_wbr, covering row counts, revenue totals and date ranges for
weekly_metrics, weekly_category_metrics, order_facts, golden_weekly_metrics and
golden_weekly_category_metrics against DuckDB. Total exposure ceiling USD0.01.
No retries, additional queries, Bedrock invocation or write/DDL are authorized.
Stop on failure, unexpected scope/cost or uncertain execution status; reconcile
before another attempt. Existing enforced 100 MiB per-query scan cutoff is
verified; it is not a verified total-dollar cap.

Expires October 8, 2026, 11:59 PM Pacific or after the single execution, whichever
occurs first. Requested receipt: exact SQL, query ID, final status, data scanned,
runtime, output totals/date ranges and DuckDB comparison, excluding credentials
and raw private rows. Lakshmi's USD0.00005 estimate is unverified; measured cost
and query acceptance are not established. This record is approval, not an
execution receipt. Assistant has not executed the query.

## Reconciliation receipt and laptop authentication proposal — October 8 afternoon

Approved single SELECT executed once in S04-WBR, s04_wbr; query ID
b3083bf1-2b61-43e2-8d32-fdfba4c8ff3a, SUCCEEDED, submitted 23:26:12.773 UTC,
completed 23:26:13.721 UTC. Read-only GetQueryExecution and GetQueryResults verify
1,161,647 bytes scanned, 817 ms engine time, 948 ms total time, and five aggregate
rows. Correctly distinguish engine time from total latency. This consumes the
one-execution authorization; it does not authorize subsequent paid calls.
Billed dollar cost is not independently verified.

Athena results (row count / rounded revenue):
weekly_metrics 730 / 13492730.31;
weekly_category_metrics 9467 / 13492730.31;
order_facts 99441 / 13591643.70;
golden_weekly_metrics 729 / 13460585.94;
golden_weekly_category_metrics 9467 / 13470166.86.
Revenue sums differ across raw/aggregate/golden tables; these are different
semantics and planted fixtures, not an assertion they should equal each other.
Lakshmi reports exact per-table DuckDB parity and correct timestamps; her
local DuckDB counterpart is not independently replayed in this checkpoint.
Whole-table ranges extend outside the canonical analysis window: tool validation
must separately demonstrate correct requested-window filtering.

Programmatic-access inspection: Lakshmi has zero access keys; no S04 assumable
developer role is present in the returned six-role inventory; IAM Identity Center
ListInstances in Ohio returns none. Attached policies do not include the AWS
local-development sign-in policy. Never reuse VisionProof roles or admin keys.

AWS official CLI documentation supports console-based aws login (CLI >=2.32.0)
for IAM users, with temporary auto-refreshing credentials and an older-SDK
credential_process compatibility route. Official managed-policy reference lists
signin:AuthorizeOAuth2Access and signin:CreateOAuth2Token. Proposed narrow
same-device grant targets arn:aws:signin:us-east-2:704554708405:oauth2/public-client/localhost.
This is a PROPOSAL, not applied or authorized; actual CLI/SDK versions and local
login acceptance remain unknown. Sources:
https://docs.aws.amazon.com/cli/latest/userguide/cli-configure-sign-in.html
https://docs.aws.amazon.com/aws-managed-policy/latest/reference/SignInLocalDevelopmentAccess.html

Next paid steps remain proposals: three-tool Athena parity on real/golden data
requires a finite query/attempt plan and separate total ceiling approval; six
Nova Micro scenarios require the exact bounded plan and separate approval.
Keep Lambda/EventBridge deployment as post-submission work, not an in-flight
architecture change.
