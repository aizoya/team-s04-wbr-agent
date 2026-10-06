# Three-Minute Demo Script

## 0:00–0:20 — Problem
An e-commerce operations analyst should not spend Monday assembling metrics, investigating movements, and writing the weekly review by hand.

The agent should return a finished, evidence-linked Weekly Business Review and clearly separate what changed, what the evidence supports, and what remains unexplained.

## 0:20–0:50 — Real Olist report with planted scenario
Use real Olist weeks inside the approved analysis window, with one planted scenario whose expected answer is known in advance.

Preferred scenario:
- a realistic week-over-week revenue decline (target about 20%);
- order count approximately flat or materially smaller than the revenue move;
- the investigation should identify the state/category contribution through the query tools;
- exact values come from Lakshmi's planted scenario and answer key.

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

That week is outside the approved complete analysis window because order volume falls to roughly half the preceding normal range as data collection winds down.

Expected behavior:
- agent detects the week is incomplete / outside the complete-window policy;
- report does not present the movement as a real business collapse;
- affected findings are marked unavailable, incomplete, or PARTIAL as appropriate;
- no replacement values or causal explanation are invented.

This is the primary failure-path demonstration because it is a real data-quality problem.

## 2:15–2:40 — Independent query failure
Optionally trigger one tool/query failure while leaving the other tool results intact.

Expected:
- failed tool retries once;
- failure is preserved;
- unaffected sections survive;
- unsupported claims are removed or flagged;
- final report remains PARTIAL rather than failing closed or fabricating a value.

This demonstrates independent tool failure handling in addition to incomplete-data detection.

## 2:40–3:00 — Trust close
Reject unsupported causal wording such as:
"Revenue fell because reviews fell."

Safe form:
"Revenue and average review score both declined; this report does not establish that one caused the other."

Close:
The agent does not just write commentary. It investigates with read-only tools, shows its evidence, independently checks its claims, and says when the data is not strong enough to support an explanation.
