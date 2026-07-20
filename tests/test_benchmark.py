import unittest
import foldcontact

class BenchmarkTest(unittest.TestCase):
    def test_research_method_clears_baseline(self):
        result = foldcontact.run()
        self.assertGreaterEqual(result["contact_gain_pct"], 30)

if __name__ == "__main__":
    unittest.main()
