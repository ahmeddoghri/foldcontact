import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

import foldcontact
import foldcontact_v2
from adversarial import HOLDOUT_SEEDS, TUNING_SEEDS
from eval_v2 import summarize


class AdversarialTest(unittest.TestCase):
    def test_holdout_disjoint_from_tuning(self):
        self.assertTrue(set(TUNING_SEEDS).isdisjoint(HOLDOUT_SEEDS))

    def test_original_benchmark_still_reproduces_exactly(self):
        result = foldcontact.run()
        self.assertEqual(result["naive_contact_satisfaction"], 0.345)
        self.assertEqual(result["guided_contact_satisfaction"], 1.0)
        self.assertEqual(result["contact_gain_pct"], 65.5)

    def test_original_bug_guided_metric_is_a_tautology(self):
        """guided_contact_satisfaction is not an empirical measurement: the
        guided infiller picks max(AA, key=compatible(guided[i], a)), and the
        metric it's scored on is exactly compatible(guided[i], guided[j]).
        Since every GROUP has at least one member, a compatible pick always
        exists, so this metric is mathematically guaranteed to equal 1.0 for
        every seed, with zero variance -- proven directly across 40 seeds."""
        results = [foldcontact.run(seed=seed)["guided_contact_satisfaction"] for seed in TUNING_SEEDS]
        self.assertEqual(set(results), {1.0})

    def test_identity_recovery_is_not_tautological_and_has_real_variance(self):
        results = [foldcontact_v2.run(seed=seed)["guided_identity_recovery"] for seed in TUNING_SEEDS]
        self.assertGreater(len(set(results)), 1)
        self.assertTrue(all(r < 1.0 for r in results))

    def test_v2_shows_genuine_signal_on_tuning_seeds(self):
        result = summarize(TUNING_SEEDS)
        self.assertGreater(result["guided_identity_mean"], result["naive_identity_mean"] * 2)
        self.assertLess(result["guided_identity_mean"], 0.9)

    def test_v2_shows_genuine_signal_on_frozen_holdout_seeds(self):
        result = summarize(HOLDOUT_SEEDS)
        self.assertGreater(result["guided_identity_mean"], result["naive_identity_mean"] * 2)
        self.assertLess(result["guided_identity_mean"], 0.9)

    def test_v2_does_not_regress_the_original_published_seed(self):
        result = foldcontact_v2.run(seed=11)
        self.assertGreater(result["guided_identity_recovery"], result["naive_identity_recovery"])

    def test_original_module_untouched(self):
        import inspect

        source = inspect.getsource(foldcontact.run)
        self.assertIn('guided_ok += compatible(guided[i], guided[j])', source)

    def test_report_is_reproducible(self):
        a = summarize(TUNING_SEEDS[:5])
        b = summarize(TUNING_SEEDS[:5])
        self.assertEqual(a, b)


if __name__ == "__main__":
    unittest.main()
