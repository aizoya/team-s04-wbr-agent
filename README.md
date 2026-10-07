# Team S04 — Weekly Business Review Agent

AWS Community Day Bay Area Hackathon 2026

## Goal
Build a trustworthy agent that turns Olist e-commerce data into a completed weekly business review for an operations analyst.

## Project narrative
Analysts spend hours each week pulling metrics, comparing the latest complete week with the prior week, investigating what changed, and writing the commentary by hand.

Our system uses two reasoning agents:

1. **Analyst agent** — uses read-only query tools to investigate the metrics and draft an evidence-linked weekly review.
2. **Verifier agent** — checks each claim against the available evidence and keeps, downgrades, flags, or removes unsupported material.

The output layer then renders the verified result while preserving evidence, warnings, caveats, unavailable metrics, review flags, and uncertainty.

**One-line pitch:** Analysts spend hours each week explaining what changed. Our agents investigate the metrics, draft the review, show their evidence, check their own claims, and clearly identify what they still cannot explain.

The system does not assume that observed correlations prove causation. When evidence cannot support an explanation, the report must say so.

## V1
Compare two complete weeks across:
- Revenue
- Order count
- Average review score
- Category breakdown
- Customer-state breakdown

The final report must include supporting evidence, caveats, and actionable questions.

## Trust principles
1. Every number and conclusion is traceable to evidence, query, period, and filters.
2. Observations are separated from causes; correlation is not presented as causation.
3. Bad data or tool failure produces an honest partial report, never fabricated completion.

## Working ownership
- Franklyn Rosario, MBA-ITM — product scope, acceptance testing, demo story, AWS architecture, runner, Bedrock integration, verifier
- Lakshmi Bharathy Kumar — Olist exploration, metric definitions, Athena queries, weekly_metrics, planted scenarios, S3/Athena data setup, tool functions, analyst loop, final submission
- Maxime Gillot — final report/output layer, output tests, integration-test support, README support

## Development workflow
- One branch per task
- Pull requests into `main`
- Another teammate reviews before merge
- Squash merge preferred
- No raw Olist data, AWS credentials, API keys, `.env` files, or secrets in Git

## AWS foundation
Region: `us-east-2`
- Source bucket: `aizoya-s04-wbr-source-704554708405`
- Athena results bucket: `aizoya-s04-wbr-athena-results-704554708405`
- Glue database: `s04_wbr`
- Athena workgroup: `S04-WBR`

## Franklyn runner/verifier branch
`build/franklyn-runner-verifier-v2`

The branch provides:
- strict completion rules;
- tool-envelope and claim validation;
- one-retry failure behavior;
- evidence-aware verifier outcomes;
- explicit internal/external metric adapters;
- a renderer input boundary;
- synthetic complete/partial demos;
- local verification tooling.

Real-data acceptance remains pending Lakshmi's final tool outputs and Maxime's renderer implementation.

## License
MIT

## Status
Private development repository. Public release and final submission are separate approval gates.
