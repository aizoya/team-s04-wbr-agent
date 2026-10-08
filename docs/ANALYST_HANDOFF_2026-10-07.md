# Analyst loop handoff — 2026-10-07 PT

## Answer to Lakshmi (prepared; not sent)

Your proposed `run_analyst(week) -> {report_draft, evidence_log}` works with the new runner adapter. `report_draft` is the nested report with a `claims` list (the legacy flat list is also accepted); `evidence_log` is a request-ID-keyed mapping containing the full, unchanged external tool envelopes. Tool wrappers must collect the log outside model-generated text. Include every attempt, including partial/error results, and allocate a unique request ID per call. Structured query metadata may repeat across distinct requests; the adapter does not collapse these calls. Nested claims cite `supporting_evidence` request IDs; the verifier resolves these to the exact original captured envelope. Structured evidence references and warning objects are adapted without losing their original fields. Repeated calls to the same tool are supported. No tools are replayed by this adapter.

The adapter runs the existing verifier and renderer boundary. The fallback verifier remains fail-closed; reference existence alone never establishes semantic correctness. Only an explicit trusted verifier can keep a claim. The log's completeness and authenticity still require instrumentation in your tool wrappers; the adapter cannot prove an omitted call happened.

Account checks in us-east-2 show Nova Micro, Nova Lite, Nova Pro and Claude Sonnet 4.6 each have AVAILABLE agreement/entitlement/region and AUTHORIZED account status. These are account metadata checks, not successful model invocations or proof of your user's permissions. Haiku 4.5 is region/entitlement available but its agreement is NOT_AVAILABLE, so it is not a ready fallback.

Your user currently has only Nova Micro invoke permission. Keep the candidate configuration `WBR_MODEL_ID=us.amazon.nova-micro-v1:0` and `AWS_REGION=us-east-2` while completing model-free integration. Nova models support tool use; no comparative multi-step reliability benchmark has been run here. Switching to Lite, Pro or Sonnet requires model-specific permission review and a bounded real tool-calling acceptance run. Do not silently choose a paid model when the setting is absent.

I checked your console sign-in: user `aws-hackathon-s04-lakshmi` exists, but GetLoginProfile returns NoSuchEntity. Console sign-in is therefore still blocked. Also, the existing Nova Micro policy includes only the us-east-2 foundation-model ARN, while its US inference profile lists us-east-1, us-east-2 and us-west-2. The destination permission gap was corrected after Franklyn explicitly authorized it on October 7. Runtime invocation is still untested.

## Runner use

```python
from src.analyst_adapter import run_analyst_week

result = run_analyst_week(
    week,
    run_analyst,  # Lakshmi-owned Strands loop; returns wrapper-captured evidence
    expected_tool_names=approved_v1_tool_names,
    verifier=trusted_verifier,
    renderer=render_report,
    label="REAL_OLIST",  # only after actual Olist tools are connected
)
```

The latest mappings and source inspection are recorded in
`docs/LAKSHMI_CONTRACT_INTEGRATION_2026-10-07.md`.

Claim fields: claim_id, question_id, statement, claim_type, confidence,
supporting_evidence, causal_language_allowed, requires_human_review.

Every envelope includes: tool_name, request_id, status, generated_at,
parameters, data, evidence_refs, warnings, error. Status values are
ok/partial/error. The adapter preserves tool-specific data as opaque.

The expected tool names remain a caller setting owned by team integration;
this change does not freeze Lakshmi's final names or payload semantics.
Logged failed attempts conservatively make the overall result partial even
if later attempts recover. Malformed logs and ambiguous evidence refs fail
before verification or rendering. Claim-level malformations remain governed
by the existing runner's partial/rejection behavior.

## AWS evidence and next action

Read-only APIs completed: STS GetCallerIdentity; Bedrock ListFoundationModels,
ListInferenceProfiles, GetInferenceProfile, GetFoundationModelAvailability;
IAM GetUser, GetLoginProfile, ListAttachedUserPolicies, ListUserPolicies,
ListGroupsForUser, ListMFADevices, GetPolicy, GetPolicyVersion.

Checked account: 704554708405. User has one attached customer-managed policy,
one new inline access-repair policy after founder authorization, no groups,
no permissions boundary returned, and no MFA device returned. No model
inference, credential creation, subscription or message transmission occurred.

The policy simulator returned a templated resource ARN rather than the
requested concrete ARNs. Its implicitDeny output is therefore inconclusive
and is not accepted as per-resource authorization evidence. The destination
gap above is based on the actual policy document and profile membership.

Franklyn authorized the prepared supplemental permissions on October 7.
They were applied as inline policy `S04-WBR-Lakshmi-AccessRepair-20261007`
and verified using GetUserPolicy. The change matches
`S04_ACCESS_REPAIR_PROPOSAL.json`:
Nova Micro invoke permissions for its exact profile and all listed foundation
model destinations, plus this user's own ChangePassword/GetAccountPasswordPolicy
permissions. It adds no alternative model, IAM admin or billing permissions.
Non-sensitive API receipts are in `S04_ACCESS_REPAIR_RECEIPT_2026-10-07.json`.
Rollback, if separately requested: DeleteUserPolicy for this user and this
exact inline policy name; preserve the original attached policy.

Founder console bootstrap is now completed: GetLoginProfile confirmed
console access with PasswordResetRequired=true on October 7. Franklyn's
requested credential email and team checklist messages were sent. No
credentials are stored in this handoff. Lakshmi's successful sign-in and
service-level S3, Athena, Glue and Bedrock acceptance remain unconfirmed.

## Verification

Local model-free quality gate: 72 tests PASS (including 9 original adapter
and 13 new Lakshmi handoff tests),
plus complete and partial synthetic demos PASS. Existing runner behavior is
preserved through a shared verification/rendering function. Real Strands,
Bedrock, Olist, console and renderer acceptance remain untested.

## Primary references

- https://docs.aws.amazon.com/bedrock/latest/userguide/geographic-cross-region-inference.html
- https://docs.aws.amazon.com/bedrock/latest/userguide/model-parameters-nova.html
