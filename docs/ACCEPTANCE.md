# Acceptance Checklist

## Core correctness
- [ ] Known synthetic totals exactly match expected values.
- [ ] Revenue delta is -20.0%.
- [ ] Order-count delta is 0.0%.
- [ ] Review-score delta is -1.0 point.
- [ ] No divide-by-zero produces fabricated percentages.

## Traceability
- [ ] Every headline metric includes period, filters, grain, query ID, and evidence reference.
- [ ] Report claims reference the evidence used.
- [ ] Missing evidence prevents a COMPLETE report.

## Join safety
- [ ] Multi-item orders do not inflate headline order count.
- [ ] Reviews are canonicalized to at most one row per order before headline joins.
- [ ] State revenue reconciles to headline revenue.
- [ ] Category revenue reconciles to merchandise revenue.
- [ ] Category distinct-order counts are never summed into headline orders.

## Failure handling
- [ ] Tool timeout marks the affected metric unavailable.
- [ ] Malformed output is rejected.
- [ ] Valid sections survive as a PARTIAL report.
- [ ] Missing values are never invented.

## Causal safety
- [ ] Unsupported causal language is blocked.
- [ ] Observations may be stated.
- [ ] Causal explanations remain questions unless separately evidenced.

## Reproduction
- [ ] Tests run without AWS credentials.
- [ ] Synthetic demo is clearly labeled.
- [ ] Source data remains unchanged.
