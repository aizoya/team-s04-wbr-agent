import unittest

from src.wbr_contract import (
    ContractError,
    Metric,
    assert_unique_order_ids,
    guard_noncausal,
    mean_review,
    pct_change,
    reconcile_total,
    report_status,
    unavailable_metric,
)


class WBRContractTests(unittest.TestCase):
    def test_known_totals(self):
        self.assertAlmostEqual(pct_change(1000, 800), -20.0)
        self.assertAlmostEqual(pct_change(4, 4), 0.0)
        self.assertAlmostEqual(mean_review([5, 4, 4, 3]), 4.0)
        self.assertAlmostEqual(mean_review([4, 3, 3, 2]), 3.0)

    def test_missing_reviews_ignored(self):
        self.assertAlmostEqual(mean_review([5, None, 3]), 4.0)
        self.assertIsNone(mean_review([None, None]))

    def test_multi_item_join_safety(self):
        with self.assertRaises(ContractError):
            assert_unique_order_ids([{"order_id": "o1"}, {"order_id": "o1"}])

    def test_reconciliation(self):
        reconcile_total(800.0, [300.0, 250.0, 200.0, 50.0], "category_revenue")
        with self.assertRaises(ContractError):
            reconcile_total(800.0, [300.0, 250.0, 200.0], "category_revenue")

    def test_causal_claim_blocked(self):
        with self.assertRaises(ContractError):
            guard_noncausal("Revenue fell because of lower reviews.")
        guard_noncausal("Revenue and review score both declined.")

    def test_failure_produces_partial(self):
        ok = Metric("revenue", 800.0, evidence_ref="athena:q-123")
        bad = unavailable_metric("review_score", "timeout")
        self.assertEqual(report_status([ok, bad]), "PARTIAL")


if __name__ == "__main__":
    unittest.main()
