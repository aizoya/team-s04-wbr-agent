# Metric Contract — V1 (final)

Agreed definitions for the WBR agent. Details and rationale: `docs/stage1_data_foundation.md`.

## Time
- Week: Monday of the purchase week (`date_trunc('week', order_purchase_timestamp)`).
- Analysis window: weeks starting 2017-01-30 through 2018-08-13 (81 weeks).

## Revenue (`product_revenue`)
- `SUM(order_items.price)` for revenue orders. Shipping (freight) is excluded and reported separately.
- Revenue order: status not `canceled` or `unavailable`, and payment approved (`order_approved_at` not null).

## Order count
- `COUNT(DISTINCT order_id)` of revenue orders, at order grain.

## Average review score
- One score per order: multiple reviews for the same order are averaged.
- Orders without a review are excluded from the mean.
- Review coverage is reported as `review_count ÷ orders`.

## Delivery
- Delivered: status `delivered` with an actual delivery date.
- Late: delivered, and the delivery date is after the estimated delivery date (dates compared, not timestamps).
- Delivery days: purchase date to delivery date.

## Category
- Revenue is attributed at item grain; category revenue reconciles to total revenue.
- Category order counts are distinct within a category and are never summed into headline orders.
- Groups: 14 categories with a median of at least 30 orders per week (bed_bath_table, sports_leisure, health_beauty, furniture_decor, computers_accessories, housewares, watches_gifts, telephony, cool_stuff, toys, garden_tools, auto, perfumery, baby), plus `Other`.
- Products without a category are labeled `unknown` and grouped into `Other`.

## Customer state
- The customer state on the order.
- Groups: SP, RJ, MG, RS, PR, BA, SC, plus `Other` (states with a median below 30 orders per week).
- Missing or invalid states: none found (checked: 0 null, 0 blank, 27 valid codes). Any unexpected value would fall into `Other`.

## Join safety
- Items and reviews are pre-aggregated to one row per order before joining.
- Totals come from `weekly_metrics`; category comparisons come from `weekly_category_metrics`.
