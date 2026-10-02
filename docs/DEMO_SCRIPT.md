# Three-Minute Demo Script

## 0:00–0:25 — Problem
An e-commerce operations analyst should not spend Monday assembling metrics and then writing the review. The agent should return a finished, evidence-linked weekly business review.

## 0:25–1:20 — Completed synthetic report
Show:
- Revenue: 1,000 -> 800 (-20.0%)
- Orders: 4 -> 4 (0.0%)
- Average review score: 4.0 -> 3.0 (-1.0 point)

Then show the narrative and actionable questions.

## 1:20–1:55 — Evidence inspection
Open one metric's evidence:
- period
- filters
- grain
- query/tool ID
- row count
- evidence reference

## 1:55–2:35 — Deliberate failure
Simulate current-week review failure.
Expected:
- revenue valid
- orders valid
- review score unavailable
- report status PARTIAL
- no replacement value invented

## 2:35–3:00 — Trust close
Reject unsupported causal wording such as:
"Revenue fell because reviews fell."

Safe form:
"Revenue and average review score both declined; this report does not establish that one caused the other."
