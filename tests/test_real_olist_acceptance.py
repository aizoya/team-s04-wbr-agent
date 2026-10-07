import unittest

from demo.run_real_olist_acceptance import (
    index_tool_results,
    make_answer_key_verifier,
    require_expected_status,
)


class RealOlistAcceptanceTests(unittest.TestCase):
    def test_duplicate_tool_results_are_rejected_before_indexing(self):
        results = [
            {"tool_name": "weekly_revenue"},
            {"tool_name": "weekly_revenue"},
        ]
        with self.assertRaisesRegex(ValueError, "duplicate tool result"):
            index_tool_results(results)

    def test_answer_key_evidence_must_be_cited_by_claim(self):
        verifier = make_answer_key_verifier(
            {
                "c1": {
                    "outcome": "keep",
                    "required_evidence_refs": ["athena:weekly_revenue"],
                }
            }
        )
        claim = {
            "claim_id": "c1",
            "supporting_evidence": ["athena:weekly_orders"],
        }
        evidence_by_ref = {
            "athena:weekly_revenue": {"tool_name": "weekly_revenue"},
            "athena:weekly_orders": {"tool_name": "weekly_orders"},
        }

        outcome = verifier(claim, evidence_by_ref)

        self.assertEqual(outcome["outcome"], "remove")
        self.assertEqual(
            outcome["reason"],
            "claim does not cite required answer-key evidence",
        )

    def test_answer_key_evidence_must_also_be_available(self):
        verifier = make_answer_key_verifier(
            {
                "c1": {
                    "outcome": "keep",
                    "required_evidence_refs": ["athena:weekly_revenue"],
                }
            }
        )
        claim = {
            "claim_id": "c1",
            "supporting_evidence": ["athena:weekly_revenue"],
        }

        outcome = verifier(claim, {})

        self.assertEqual(outcome["outcome"], "remove")
        self.assertEqual(outcome["reason"], "answer-key evidence unavailable")

    def test_planted_real_olist_requires_complete(self):
        require_expected_status("PLANTED_REAL_OLIST", "complete")
        with self.assertRaisesRegex(ValueError, "expected complete, got partial"):
            require_expected_status("PLANTED_REAL_OLIST", "partial")

    def test_incomplete_real_olist_requires_partial(self):
        require_expected_status("REAL_OLIST_INCOMPLETE", "partial")
        with self.assertRaisesRegex(ValueError, "expected partial, got complete"):
            require_expected_status("REAL_OLIST_INCOMPLETE", "complete")


if __name__ == "__main__":
    unittest.main()
