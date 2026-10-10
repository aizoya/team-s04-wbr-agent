# Three-Minute Demo Script

## 0:00–0:20 — Problem
An e-commerce operations analyst should not spend Monday assembling metrics, investigating movements, and writing the weekly review by hand.

The agent should return a finished, evidence-linked Weekly Business Review and clearly separate what changed, what the evidence supports, and what remains unexplained.

## 0:20–0:50 — Real Olist report with planted scenario
Use real Olist weeks inside the approved analysis window, with one planted scenario whose expected answer is known in advance.

Preferred scenario: Lakshmi's S1 category drop, using the final answer key's
week (currently 2018-08-13), where health_beauty revenue falls and SP accounts
for the leading contribution. Use only the actual captured query values and
approved output. Do not force the older illustrative 20% decline or flat-order
story onto this scenario; orders, items and other values were scaled together.
Label it a synthetic scenario planted on real Olist summaries, not an actual
business incident or an order-level reconstruction.

Show the finished WBR briefly:
- headline revenue movement;
- order movement;
- average order value / supporting metric;
- leading state/category contribution;
- one actionable question.

Do not use the 4-order synthetic fixture as the primary judging demo. Keep it only for deterministic unit/contract tests.

## 0:50–1:20 — Agent investigation trace
Show the analyst agent deciding what to inspect next rather than jumping directly to prose.

Illustrative trace:
1. Revenue changed materially.
2. Check order count.
3. If orders are relatively flat, inspect average order value.
4. Break the change down by state.
5. Follow the largest material state contribution.
6. Break that state down by category.
7. Draft only claims supported by returned evidence.

The purpose of this segment is to demonstrate planning and tool use, not a prompt-wrapper workflow.

## 1:20–1:45 — Evidence inspection
Open one supported claim and show the evidence behind it:
- comparison period;
- filters;
- grain;
- query/tool identifier;
- row/order count;
- evidence reference;
- warnings, including small-sample warnings when applicable.

The verifier must be able to trace the claim back to this evidence.

## 1:45–2:15 — Real incomplete-data failure
Use the real week starting 2018-08-20.

That week is the known incomplete end-of-collection case in Lakshmi's answer
key. Show the actual incomplete warning and captured values; do not invent a
volume ratio that has not been verified in the selected capture.

Expected behavior:
- agent detects the week is incomplete / outside the complete-window policy;
- report does not present the movement as a real business collapse;
- affected findings are marked unavailable, incomplete, or PARTIAL as appropriate;
- no replacement values or causal explanation are invented.

This is the primary failure-path demonstration because it is a real data-quality problem.

## 2:15–2:40 — Independent query failure
Optionally trigger one tool/query failure while leaving the other tool results intact.

Expected:
- the backend applies its bounded retry policy; captured-response replay never
  retries already-recorded calls or spends on another model run;
- failure is preserved;
- unaffected sections survive;
- unsupported claims are removed or flagged;
- final report remains PARTIAL rather than failing closed or fabricating a value.

This demonstrates independent tool failure handling in addition to incomplete-data detection.

## 2:40–3:00 — Trust close
Reject unsupported causal wording such as:
"Revenue fell because reviews fell."

Safe form:
"Revenue and average review score both declined. This is an association only;
no causal conclusion is established."

Close:
The agent investigates with read-only tools and shows its evidence. Demonstrate
which checks actually ran; disclose flagged and unsupported statements. Do not
claim general semantic verification from the bounded numeric gate. Keep the
report PARTIAL when an acceptance requirement has not been met.

