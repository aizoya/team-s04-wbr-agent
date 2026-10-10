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

## Approved same-device temporary login enablement — October 8, 4:54 PM Pacific

Franklyn approved ("A") adding the proposed two sign-in actions and sending
Lakshmi the instructions. Target account/user verified; previously absent inline
policy S04-WBR-Lakshmi-LocalLogin-20261008 applied with exact actions
signin:AuthorizeOAuth2Access and signin:CreateOAuth2Token, resource
arn:aws:signin:us-east-2:704554708405:oauth2/public-client/localhost,
StringEquals aws:RequestedRegion us-east-2. PutUserPolicy succeeded and readback
matched. Principal simulations allow both same-device Ohio actions; deny remote
public client and us-west-2. Existing service policies preserved; no permanent
key created, no SSO/role/infrastructure setup or live invocation.

Authorized instructions sent as a reply to Lakshmi's authentication DM:
https://awsusers.slack.com/archives/D0C78HS1Z50/p1791503705107929?thread_ts=1791503449.478859&cid=D0C78HS1Z50
Instructions include CLI >=2.32.0, s04-login profile in Ohio, own-user/account
identity verification, older-SDK credential_process compatibility, private cache/
credential handling and logout. CLI/SDK version and actual login remain unverified.
No root/admin credentials to be used. Remote login or different region would
require reconciliation, not silent policy expansion. Rollback if authorized:
remove only this dedicated inline policy.

Authentication approval does not authorize paid tool-parity or Bedrock batches.
Requested finite Athena cases/query-attempt counts including retries and a
separate six-scenario model plan with token/tool-call limits before approval.
Lambda/EventBridge deferred. This supersedes the earlier unauthorised proposal
status for these exact login actions only.

## Approved Athena tool-parity batch — October 8, 5:57 PM Pacific

Lakshmi confirms AWS CLI 2.37.11 login and Python boto3 s04-sdk compatibility
profile both identify account 704554708405 and aws-hackathon-s04-lakshmi.
This is teammate-reported laptop/SDK authentication acceptance, not independently
executed on her laptop. No project dependencies changed, per her report.

Franklyn approved ("A") one execution of the exact 13-case parity batch today,
October 8 Pacific, with a USD0.02 total incremental exposure ceiling, including
Athena and associated S3 requests/result handling. Scope: us-east-2, S04-WBR,
s04_wbr, existing real and golden tables, get_weekly_metric/get_breakdown/
get_delivery_signals compared with DuckDB. Three real cases use 2018-03-12;
golden S1/S2/S3/S4/S6/S7/S8/S10 each send one query; S5 simulated failure and
S9 invalid input send zero queries. Eleven planned queries, hard maximum
22 StartQueryExecution attempts including retries, no extra batches or reruns.
S5/S9 must not reach Athena. Script cap enforcement is Lakshmi-reported, not
independently inspected code enforcement.

Existing 100 MiB per-query workgroup cutoff remains. Total ceiling is founder
authorization, not a verified AWS hard-dollar enforcement control. Her ~$0.001
projection assumes minimum billing per query and is not a maximum-cost proof.
Stop before exceeding the attempt/spending cap, on access denial, uncertain
execution status or unplanned scope; no ad hoc retry or permission expansion.
Expire after the single batch or October 8, 11:59 PM Pacific, whichever first.

No Bedrock calls, DDL/write operations, deployment or new permissions authorized.
Required receipt: reviewed branch/commit and command, case-level DuckDB/Athena
comparison, all query IDs/attempts including failures/retries, bytes scanned,
engine/total/elapsed times, errors, cap behavior and priced-vs-unknown costs.
Bedrock six-scenario plan remains separately gated. Assistant did not execute
the batch; completion and parity are not yet verified.


## October 9, 2026 — parity evidence reconciliation and bounded Bedrock approval

Independent read-only verification: runs/athena_parity_20261009_103840.json
on work/Lakshmi-data-tools, blob 6f8f085c31acf0472cbd035d67d6c29896af9fc9,
contains 13 cases; all stored DuckDB/Athena normalized envelopes compare equal.
AWS GetQueryExecution independently confirms the 11 recorded execution IDs
SUCCEEDED with matching bytes/engine times: 636,489 bytes and 5,175 engine ms.
File reports 98.3 s local elapsed and USD0.000525 estimated Athena cost, not
invoiced cost. Local DuckDB was not independently replayed.

Timing exception: AWS submissions occurred October 9, 10:37–10:38 AM Pacific,
after the October 8, 11:59 PM approval expiry. No renewal is established in
the reviewed records. Preserve test evidence; do not retroactively describe
the run as within the approval window. Reconciliation remains open.

Franklyn explicitly approved ("Approve", October 9 at 11:23:46 AM Pacific)
the revised one-time USD0.75 total incremental ceiling for six live scenarios:
S1, S2, S3, S4, S5, S7, one trial each. Lakshmi owns execution. S1 runs first;
stop the entire batch on any unexpected failure. Backend Athena golden tables;
account 704554708405; source endpoint us-east-2; S04-WBR/s04_wbr; model/profile
us.amazon.nova-micro-v1:0. US cross-region routing is within this scope.

Pre-execution condition: identify branch/commit/command and verify deterministic
guards for model attempts including SDK retries, cumulative input/output tokens,
tool calls, Athena attempts, timeouts, and next-call cost reservation. A
documented limit is not verified enforcement. Confirm the exact finite model
attempt ceiling before execution. Per run: 25 tool calls, 300,000 cumulative
input+output tokens, max 2,000 output tokens per response. Do not start a call
that can exceed the reserved run/batch budget. Batch: max 300 Athena start
attempts including all retries; preserve existing 100 MiB/query cutoff.
USD0.75 includes Bedrock, Athena, associated S3 requests/results and retries;
this is founder authorization, not an AWS hard-dollar service cap.

The proposed USD0.014 Athena worst case was minimum-billing based, not a maximum:
300 x 100 MiB at approximately USD5/TB is approximately USD0.16 before S3.
Lakshmi's USD0.47 Bedrock estimate remains a projection, not independently
verified runtime enforcement or invoice.

Read-only GetInferenceProfile confirms ACTIVE US Nova Micro and destination
models in us-east-1/us-east-2/us-west-2. IAM simulation for Lakshmi allows
InvokeModel and InvokeModelWithResponseStream on the exact Ohio account profile
and all three destination model ARNs, using requested-region Ohio context.
Simulation does not prove successful live invocation or override organization/
session controls. No permission expansion or model invocation performed.

Approval expires after the single batch or October 9, 11:59 PM Pacific,
whichever first. No extra trials/reruns, model substitution, DDL/data writes,
new permissions or deployment. Stop on access denial, uncertain execution,
missing cost accounting or cap risk; request renewed approval for changed scope.
Save scenario-level expected/actual verdicts, raw request_id evidence envelopes,
model request counts/IDs and token usage, query IDs/attempts/bytes, engine/total/
elapsed times, errors and estimated-vs-unknown costs. Full submission acceptance
remains pending live agent/verifier/renderer integration and final demonstration.


## October 9 — model-free published-code preflight review

MUST FIX BEFORE LIVE BATCH: reviewed published Lakshmi branch files without
changing teammate source or executing the agent:
- agent/steering.py blob 757b76b24d7bc5affd51cf7a2be18f3cf692856a checks
  accumulated usage rather than reserving the next call; explicitly permits
  a final call past token cap. No next-call reservation proven here.
- agent/analyst.py blob 33003da7b74671e6f2aad8a29a193f0acb286b20 configures
  40 turns and an additional five-turn finalization invocation. This is not
  proof of a global model-attempt cap including SDK-level retries.
- scripts/evaluate_agent.py blob 839abfca66b4a12eed29e2eda6889e52d89e843a
  stops on run.status error only; a graded scenario failure can continue.
  Saved evaluation runs omit evidence_log and individual Athena query receipts.
  Its plan still computes minimum billing and calls that worst-case Athena cost.
- Exact scenario assertion is recommended. Prefix matching can select extra
  future IDs; current GRADERS (agent/evaluation.py blob
  11e7a67a681742aa9b259fe1914d0ebe9b0de91b) contains only the six proposed
  scenario IDs and does NOT register S10. No current S10 selection defect
  established. Use full registered IDs or assert the selected six explicitly.

Lakshmi owns corrections and model-free guard tests. The conditional paid batch
must not start until the approved guard requirements are verified. Local/in-flight
fixes may already differ from these published versions; request updated immutable
commit and exact command before judging the final run. No new tests claimed here.

Sent targeted preflight findings in existing approval thread:
https://awsusers.slack.com/archives/D0C78HS1Z50/p1791570422540469
No new permission, paid execution, teammate-branch mutation or merge.
At this checkpoint no new Maxime handoff appeared in the latest S04 channel.


## October 9, 1:33 PM Pacific — review of Lakshmi guard update

Reviewed immutable commit d23cb42bab0683e420a4792b8fd321c6e2097f15 on
work/Lakshmi-data-tools. Exact scenario selection/order, stop on graded failure,
model retry disabling, 30 per-run model attempt limit and saved raw evidence/
query receipts now exist in code. Proposed execution remains the same six
one-trial scenarios; USD0.70 internal ledger is below USD0.75 authorization.
26/26 model-free tests (17 guard tests) are teammate-reported only: current
review runtime has pytest but lacks Strands, DuckDB and boto3, so full suite
was not independently executed and no dependencies were installed.

MUST FIX before conditional live batch:
1. agent/steering.py uses JSON characters/2.5 and projected input estimates;
   neither establishes a model-specific upper bound for the actual request.
   Post-call over-reservation halt cannot prevent a paid/token-cap overshoot.
   Require supported exact counting or defensible request upper bounds,
   including all relevant schemas; fallback is full-context reservation.
2. tools/backend.py FAILED/CANCELLED branch substitutes zero for missing scan
   stats, settles the minimum and may retry. Missing/invalid terminal accounting
   must retain the full reservation and halt; over-reservation stats also need
   fail-closed accounting. Request targeted missing-stat and underestimate tests.

Independent isolated reproduction executed only the published pure-Python
tools/budget.py Ledger: reserve USD0.001 under a USD0.70 ceiling, then settle
USD0.701. Ledger committed amount exceeds ceiling and halted remains None.
This confirms settlement itself does not enforce the ceiling when a reservation
underestimates actual cost; it does not simulate or incur an AWS charge.

Additional limitation: 900-second timer triggers wrap-up and can allow another
model call, so it is a soft investigation threshold, not a hard wall-clock
deadline. Separate client request timeouts are configured.

Sent precise review to Lakshmi in existing approval thread:
https://awsusers.slack.com/archives/D0C78HS1Z50/p1791578016312989
No authorization expansion, paid execution, full-suite pass claim, merge,
dependency installation or teammate-source mutation. Conditional gate remains
open for corrected immutable commit and targeted test evidence.


## October 9, 3:44 PM Pacific — conditional batch preflight cleared

Reviewed immutable fc40b9f925c33d03e9f817ac3e38773fdc97c944.
Both outstanding guards corrected in published code: full 128,000 context +
2,000 output reservation before each model call; missing/invalid/over-bound
Athena scan accounting retains full reservation, halts, and cannot retry.
Sequential tool executor added; evidence checkpointed after every run.
900 s limit explicitly soft, with separate per-request timeouts. AWS official
Nova Micro card confirms 128K context:
https://docs.aws.amazon.com/bedrock/latest/userguide/model-card-amazon-nova-micro.html

Independent 8/8 isolated checks passed on published production functions with
fake dependencies: full-context reservation ignoring low projected estimate;
refusal before sending when next full reservation cannot fit; missing stats in
FAILED/CANCELLED/SUCCEEDED; negative and bool stats; scan over 100 MiB. Each
Athena unsafe case retains full reservation and a subsequent start is blocked.
AST import stripping/fake dependencies were used because SDK/Strands/DuckDB
are unavailable; this is not a full service/SDK integration test or full-suite
pass. Lakshmi reports 36/36 laptop model-free tests, 27 guard tests.

Confirmed go-ahead to Lakshmi within EXISTING October 9 USD0.75 authorization,
not new spend/permission authority. Exact commit above; one six-scenario,
one-trial batch; USD0.70 internal ledger; S1 first; preserve all current caps,
region/model/workgroup/database/golden settings and no reducing context/prices.
Stop on unexpected failure/uncertain execution/missing accounting/cap risk;
no automatic rerun. Expiry remains October 9, 11:59 PM Pacific or single-batch
completion, whichever first. No separate gate between successful S1 and remaining
five was added. Request S1 verdict/usage and final committed raw evidence JSON.
Slack persisted receipt:
https://awsusers.slack.com/archives/D0C78HS1Z50/p1791585841846909

Lakshmi acknowledged the parity run exceeded yesterday's expiry and that no
separate renewal existed (October 9, 1:25:56 PM DM). Record exception separately;
do not rewrite prior authorization or discard valid technical evidence.

Live execution, full agent/verifier/renderer acceptance and submission remain
unverified. Assistant did not invoke models, start queries, change permissions,
merge, or alter teammate source.
