"""Dependency-free regressions for S2 assessment, not report certification."""
import copy
import unittest

from agent.evaluation import grade_run, grade_s2


KEY = {"id": "S2_delivery_and_reviews", "expected": {"state_with_review_drop": "RJ"}}


def fixture():
    return {
        "run": {"status": "ok", "tool_calls": 2, "budget": 25, "blocked_calls": []},
        "calls": [{"tool": "get_weekly_metric"}, {"tool": "get_delivery_signals"}],
        "report_draft": {
            "claims": [
                {"claim_id": "review", "question_id": "Q2", "statement": "Reviews fell in RJ.", "claim_type": "fact"},
                {"claim_id": "pattern", "question_id": "Q2", "statement": "In RJ reviews fell while late deliveries rose.", "claim_type": "observed_pattern"},
            ],
            "precheck_issues": [],
        },
    }


class S2GraderBoundary(unittest.TestCase):
    def test_valid_q2_pattern_still_passes(self):
        self.assertTrue(grade_run(fixture(), KEY)["passed"])

    def test_pattern_in_wrong_section_cannot_complete_q2(self):
        out = fixture()
        out["report_draft"]["claims"][1]["question_id"] = "Q1"
        self.assertFalse(grade_run(out, KEY)["passed"])

    def test_foreign_state_pattern_cannot_complete_rj(self):
        out = fixture()
        out["report_draft"]["claims"][1]["statement"] = "In SP reviews fell while deliveries slowed."
        self.assertFalse(grade_run(out, KEY)["passed"])

    def test_wrong_period_pattern_is_not_accepted(self):
        out = fixture()
        out["report_draft"]["precheck_issues"] = [{"claim_id": "pattern", "issue": "evidence_week_mismatch"}]
        self.assertFalse(grade_run(out, KEY)["passed"])

    def test_invalid_q2_review_is_not_hidden_by_valid_pattern(self):
        out = fixture()
        out["report_draft"]["precheck_issues"] = [{"claim_id": "review", "issue": "evidence_week_mismatch"}]
        self.assertFalse(grade_run(out, KEY)["passed"])

    def test_unnamed_state_q2_issue_is_not_hidden_by_valid_pattern(self):
        for statement in ["Reviews in that state fell.", "Reviews fell in Rio."]:
            with self.subTest(statement=statement):
                out = fixture()
                out["report_draft"]["claims"][0]["statement"] = statement
                out["report_draft"]["precheck_issues"] = [{"claim_id": "review", "issue": "evidence_week_mismatch"}]
                self.assertFalse(grade_run(out, KEY)["passed"])

    def test_unrelated_section_issue_does_not_replace_q2_evaluation(self):
        out = fixture()
        out["report_draft"]["precheck_issues"] = [{"claim_id": "other-section", "issue": "evidence_week_mismatch"}]
        self.assertTrue(grade_run(out, KEY)["passed"])

    def test_wrong_period_named_pattern_is_not_masked_by_valid_replacement(self):
        out = fixture()
        replacement = copy.deepcopy(out["report_draft"]["claims"][1])
        replacement["claim_id"] = "replacement"
        out["report_draft"]["claims"].append(replacement)
        out["report_draft"]["precheck_issues"] = [{"claim_id": "pattern", "issue": "evidence_week_mismatch"}]
        self.assertFalse(grade_run(out, KEY)["passed"])

    def test_invalid_evidence_variants_are_rejected(self):
        for issue in ["unknown_evidence", "no_valid_evidence", "cites_failed_call", "evidence_wrong_week", "causal_language"]:
            with self.subTest(issue=issue):
                out = fixture()
                out["report_draft"]["precheck_issues"] = [{"claim_id": "pattern", "issue": issue}]
                self.assertFalse(grade_s2(out, KEY)["passed"])

    def test_no_pattern_stays_failure(self):
        out = fixture()
        out["report_draft"]["claims"].pop()
        self.assertFalse(grade_run(out, KEY)["passed"])

    def test_q1_review_cannot_substitute_for_q2(self):
        out = fixture()
        for claim in out["report_draft"]["claims"]:
            claim["question_id"] = "Q1"
        self.assertFalse(grade_run(out, KEY)["passed"])

    def test_run_error_and_process_counts_preserved(self):
        out = fixture()
        self.assertEqual(grade_run(out, KEY)["process"]["tool_calls"], 2)
        out["run"]["status"] = "error"
        self.assertFalse(grade_run(out, KEY)["passed"])

    def test_q2_pattern_can_be_the_review_claim_without_literal_tool_sequence(self):
        out = fixture()
        out["report_draft"]["claims"].pop(0)
        out["calls"] = [{"tool": "alternative_analytical_path"}]
        self.assertTrue(grade_run(out, KEY)["passed"])


if __name__ == "__main__":
    unittest.main()
