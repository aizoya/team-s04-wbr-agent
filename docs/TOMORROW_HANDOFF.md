# S04: execution handoff for October 8

Internal finish target: October 8, 2026, 11:59 a.m. Pacific. Franklyn intends to
drive while teammates execute; use this handoff to minimize founder technical work. It is not
an assertion that the project is done, a merge authorization, or permission
to spend beyond existing approvals. Proposed ownership does not prove teammate
acceptance.

## What is prepared

Existing draft PR #4 contains the runner adapter, captured-evidence mapping,
causal-language protection, numeric contradiction rejection, replay CLI and
tests. It is stacked on PR #3 and PR #2. Do not copy only one branch's files or
discard the lower-stack answer-key statement-binding fix. Follow normal team
review and merge decisions; do not merge merely because tests pass.

Latest local gate: 123 tests plus both synthetic demos PASS. Offline configuration
diagnostics and runner initialization recovery are implemented. See
`docs/WELL_ARCHITECTED_REVIEW_2026-10-08.md` for priorities and current AWS receipts. No real Olist,
Strands, Athena or Bedrock runtime acceptance is established. No paid service
call or deployment was performed for this handoff.

## Lakshmi: own the data/agent acceptance handoff

1. Confirm console reset, local SDK authentication, exact source/results bucket,
   s04_wbr catalog and S04-WBR workgroup. Do not share credentials in Git/chat.
2. Complete the source upload/catalog and Athena parity checks under the existing
   approved scope. Use us-east-2 and us.amazon.nova-micro-v1:0; no silent model
   fallback or expanded permissions.
3. Save representative analyst responses with their request-ID evidence logs:
   planted complete scenario, incomplete 2018-08-20, failed review query,
   unsupported causal wording and the V2 unsupported percentage. Keep actual
   results separate from synthetic fixtures; do not derive expected answers
   from claims being tested.
4. Provide branch/commit, run command, actual outcomes, blockers and ETA.

## Maxime: own report binding and integration coordination

1. Provide renderer branch/commit and callable interface. Bind it through
   run_analyst_week(..., renderer=...) on the reviewed integration branch.
2. Render top-level claim outcomes, removed claims, unavailable results and
   warnings. Raw analyst_draft/transcript is unverified; never display its
   rejected claims as approved conclusions.
3. Run local quality checks, real capture replay and complete/partial/failure
   report tests. Preserve unaffected results on one-tool failure.
4. Assemble the final demo, run instructions and evidence packet with Lakshmi.

## Reviewed numeric-fact policy: proposed, off by default

The existing default rejects scoped numeric contradictions but flags numeric
matches for review. The optional callback below is implemented and tested as a
candidate, not approved for live acceptance:

```python
from src.numeric_verifier import make_captured_verifier
from src.analyst_adapter import run_analyst_week

verifier = make_captured_verifier(week, allow_verified_facts=True)
result = run_analyst_week(
    week, run_analyst,
    expected_tool_names=("get_weekly_metric", "get_breakdown", "get_delivery_signals"),
    verifier=verifier, renderer=render_report,
)
```

Only enable after team review and real-output validation. This verifies an exact
bounded additive-metric percentage sentence, never arbitrary narrative.
Every cited capture must match the slice; its comparison week must be the
preceding Monday; all rounded numeric possibilities must fit the assertion;
status must be ok with no envelope/group warnings; bases must be at least 30;
baseline must have eight weeks and a finite scoped z-score. Human-review flags
and causal permissions cannot be waived. Proposed confidence is high for the
strongest matched signal at |z| >= 3, medium otherwise; inconsistent labels
remain reviewed. Do not borrow strength from another slice or a top group
unrelated to the claim. This deliberately narrows Lakshmi's preliminary rule
and requires reconciliation, not silent adoption.

Observed patterns, unexplained claims, arbitrary prose, rate/point statements,
weak or unknown quality, uncertain rounding and missing semantics stay flagged.
The callback assumes trusted wrapper captures; it does not authenticate database
provenance or prove real AWS access. If a complete report cannot be justified,
keep PARTIAL and disclose the limitations instead of forcing keep outcomes.

## Commands and acceptance receipts

```sh
python3 scripts/verify.py
python3 demo/run_captured_analyst.py --week 2018-08-13 --response /path/to/response.json
```

The replay command uses the safe default and never calls tools or models.
Record the reviewed code commit, data version, model ID, backend, requested
week, captured evidence, outcomes, renderer output and actual service test
results. Keep secrets and private transcripts out of committed receipts.

Show real planted Olist evidence in the judge demo; use synthetic fixtures only
for testing. Pick the scenario/week from Lakshmi's final answer key, not the
older illustrative 20% example. Capture association versus causation honestly.

## What genuinely needs Franklyn

Escalate only a real permission/credential authority change, incremental spending,
contract/publication/submission decision, material scope/policy exception or
explicit merge decision not already delegated. Do not imply sign-in success,
review approval, live acceptance, submitted status or completed integration
without evidence. Reply with one concise decision and exact options if founder
action is needed; otherwise keep routine technical execution with the two
teammates. No founder action is currently needed merely to read this handoff.

## October 8 verified AWS checkpoint

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

## October 8 afternoon reconciliation — approximately 4:03 PM Pacific

This checkpoint supersedes the earlier empty-source-bucket observation, not
the historical receipt. Read-only STS, S3 ListObjectsV2 and Glue GetTables
succeeded in account 704554708405, us-east-2.

Five Parquet objects now exist in the agreed layout:
- source/order_facts/order_facts.parquet: 4,815,182 bytes
- source/weekly_category_metrics/weekly_category_metrics.parquet: 198,659 bytes
- source/weekly_metrics/weekly_metrics.parquet: 30,376 bytes
- fixtures/weekly_category_metrics/weekly_category_metrics.parquet: 198,899 bytes
- fixtures/weekly_metrics/weekly_metrics.parquet: 30,289 bytes

Source uploads are timestamped October 8, 22:52:18–19 UTC; fixture uploads
22:55:06 UTC (3:52–3:55 PM Pacific). Object existence does not verify Parquet
contents, schema, parity or uploader identity. Glue s04_wbr still returns zero
tables. Preserve Lakshmi's in-flight setup; do not duplicate uploads or create
catalog tables in her place.

PR #4 remains draft, open and unmerged; inspected head before this documentation
update: 2aa02ef8239a50692d3569e1a12173c574839d2e. Local scripts/verify.py rerun
returned exit 0 / QUALITY GATE PASS: 119 tests and both synthetic demos.
This is offline evidence, not real-data/AWS/renderer acceptance.

Approved accountability email sent to Lakshmi and Maxime from
franklyn@aizoya.com: Outlook action acknowledged success, with Sent Items
requested. Approved Slack message sent once and subsequently found in channel
search: https://awsusers.slack.com/archives/C0C648P9SV8/p1791497219968399
No new teammate reply was returned by today's scoped email searches or S04
public-channel search. This does not prove absence of private messages or
teammate work.

Remaining owners: Lakshmi catalog and data/tool parity plus live captures;
Maxime renderer integration and report/demo evidence; Franklyn acceptance,
review/merge decisions, confidence-policy reconciliation and bounded spending
approval where needed. No new paid Athena query, Bedrock invocation, permission
change, merge, deployment or additional team communication was performed in
this checkpoint. Final acceptance remains NO-GO until those gates are evidenced.

## Offline acceptance hardening — October 8 afternoon

Four adapter-path regression tests were added on the existing PR #4 branch,
without runtime changes or edits to teammate components:
empty drafts remain partial; error captures retaining stale references cannot
support a keep outcome; verifier exceptions remove the claim and render once
without replaying the analyst; duplicate expected-tool configuration cannot
produce a complete report.

Test commit: c5f996ae922fcf5f6ea9697434e57cf60f49dfe3; published file readback
verified. python3 -m unittest discover -s tests: 123 tests, OK, exit 0.
python3 scripts/verify.py: exit 0, QUALITY GATE PASS, including both synthetic
complete/partial demos. These tests strengthen offline acceptance evidence only;
real-data parity, live invocation, renderer integration and final approval
remain outstanding. No paid workloads, permissions, merge or deployment.
