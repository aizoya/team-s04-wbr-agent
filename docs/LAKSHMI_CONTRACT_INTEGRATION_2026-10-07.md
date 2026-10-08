# Lakshmi contract integration — local acceptance only

The existing PR #4 adapter now accepts the actual Stage 3 contract:
`run_analyst(week)` returns nested `report_draft.claims`, a request-ID-keyed
`evidence_log`, and optional run/calls/transcript metadata. The legacy flat
claim-list adapter path remains supported.

## Mappings

- Nested claims keep their original request-ID citations. The verifier index
  resolves each ID to a deep-copied original captured envelope. Failed calls
  are never available evidence, even if a custom verifier attempts to keep
  the claim. Unknown IDs likewise cannot be kept.
- Structured evidence metadata receives a capture-local lookup key for the
  older runner boundary. Query/backend/table/count/time metadata is preserved
  unchanged inside `source_envelope`; no query authentication is fabricated.
- Structured warnings receive a JSON string for the older renderer boundary,
  preserving codes, messages and details. The verifier's request-ID lookup
  still sees the original warning objects.
- Multiple calls to one tool stay distinct, even when query metadata repeats.
  Request-ID aliases colliding with legacy reference keys are rejected.
- Model failures with a null draft return partial results and retain logged
  captures. A partial draft, unavailable items or precheck issues cannot
  produce overall complete status solely because a verifier returned keep.
- Renderer context includes explicitly unverified `analyst_draft`, plus
  `analyst_run`, `analyst_transcript`, and `analyst_calls`. Only the existing
  top-level claims carry verifier outcomes. A renderer must not treat raw
  analyst questions/draft claims as verified conclusions.

Configure the actual tool names at integration:
`get_weekly_metric`, `get_breakdown`, `get_delivery_signals`.

The agent sees concise views, not necessarily the complete raw envelopes.
The raw captures and model transcript remain separate evidence. This adapter
does not prove every tool call was captured or implement Lakshmi's loop.

## Source inspection

Inspected `work/Lakshmi-data-tools` source blobs:

- agent/analyst.py: 58fed18663883f56d524d9ca503ee09907889794
- agent/run_context.py: 036bcf6888aebc7bdc24a05dfe7539a8eb790e87
- agent/postchecks.py: 009fe2c5cdc8a989c1edb1aefcfee54cce64f9f1
- tools/envelope.py: 80ca80da9c190a3007b478052e5d6e8de2321a25

No teammate source was changed or merged. The 13 new tests use synthetic
fixtures matching these inspected contracts, not actual Olist query results.

## Verification and remaining gates

`python3 scripts/verify.py`: 80/80 local tests PASS, including all earlier
runner/adapter/answer-key tests and 13 new handoff tests. Synthetic complete
and partial demos PASS. This is not independent review, hosted CI evidence,
real Strands execution, semantic acceptance of arbitrary prose, or live AWS.

## Negative-claim replay and safety correction

The four authored claim strings from Lakshmi's answer-key blob
`0dfe5a8094d58383eed7f1cc063dd8b7c1b46efa` are replayed through the adapter
and default verifier with synthetic captures. V1 and V4 flag unsupported causal
language; V3 removes a claim citing a failed call. V2 flags with "semantic
verification unavailable" rather than the required remove: this remains an
acceptance gap, not a passed numeric-verification requirement. Real query
payloads and numeric semantic verification are still required. The tests
deliberately record fallback behavior; they do not implement an answer-key
oracle or prove real Olist parity.

Removed blanket causal-guard exemptions for a trailing question mark or a
disclaimer anywhere in the text, and added "drove" to the blocked patterns.
Four adversarial regression tests pass. Ambiguous causal questions/negations
may now require review rather than silently bypassing the guard. This lexical
check is conservative, not a complete semantic causal-language detector; a
trusted custom verifier remains responsible for its own review policy.

Remaining: actual tool/golden outputs and V2 numeric semantic acceptance, confidence
policy reconciliation, Maxime renderer binding, real Olist/Athena parity and
Bedrock tests, teammate review, merge decision, final demo/submission handoff.

Access update: console login exists with required first-sign-in password reset;
the narrow permission repair was applied and verified. Credential delivery and
team status/checklist messages were sent separately. Successful sign-in and
runtime SDK/service access remain unconfirmed. No credentials are stored here.
