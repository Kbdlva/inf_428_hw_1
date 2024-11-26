import unittest
import numpy as np
from solution import (
    generate_random_data,
    calculate_aggregated_threat_score
)

class TestAggregatedThreatScore(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        np.random.seed(42)

    def test_equal_department_scores(self):
        scores = [generate_random_data(30, 0, 5) for _ in range(5)]
        result = calculate_aggregated_threat_score(scores)
        self.assertAlmostEqual(result, 30, delta=2)

    def test_one_high_score_others_low(self):
        scores = [
            generate_random_data(30, 0, 4) + generate_random_data(80, 0, 1)  # One high outlier
            for _ in range(5)
        ]
        result = calculate_aggregated_threat_score(scores)
        self.assertTrue(result > 40)

    def test_outlier_in_finance(self):
        scores = [
            generate_random_data(30, 10, 5),  # HR
            generate_random_data(20, 10, 5),  # IT
            generate_random_data(30, 10, 5),  # Operations
            np.concatenate((generate_random_data(30, 10, 4), generate_random_data(80, 5, 1))),
            generate_random_data(30, 10, 5),  # Legal
        ]

        result = calculate_aggregated_threat_score(scores)
        print(result)
        self.assertTrue(35 <= result <= 50)


    def test_different_user_counts_per_department(self):
        scores = [
            generate_random_data(30, 10, 5),  # HR
            generate_random_data(40, 15, 10),  # IT
            generate_random_data(20, 5, 3),  # Operations
            generate_random_data(50, 15, 8),  # Finance
            generate_random_data(35, 10, 7),  # Legal
        ]
        result = calculate_aggregated_threat_score(scores)
        self.assertTrue(30 <= result <= 70)

    def test_uniform_high_scores(self):
        scores = [generate_random_data(80, 2, 5) for _ in range(5)]
        result = calculate_aggregated_threat_score(scores)
        self.assertAlmostEqual(result, 80, delta=2)

    def test_uniform_low_scores(self):
        scores = [generate_random_data(5, 2, 5) for _ in range(5)]
        result = calculate_aggregated_threat_score(scores)
        self.assertAlmostEqual(result, 5, delta=2)

    def test_high_variance_with_extreme_outliers(self):
        scores = [
            np.concatenate((generate_random_data(30, 2, 4), generate_random_data(90, 5, 10)))
            for _ in range(5)
        ]
        result = calculate_aggregated_threat_score(scores)
        print(f"Aggregated Score: {result}")
        self.assertTrue(result > 50)


    def test_large_number_users_different_variance(self):
        scores = [generate_random_data(40, 10, 150) for _ in range(5)]
        result = calculate_aggregated_threat_score(scores)
        self.assertTrue(30 <= result <= 90)

    def test_outlier_impact(self):
        """
        Case: One department has an outlier value, and the result should reflect its higher weight.
        Example: [30, 30, 30, 30, 80]
        """
        scores = [
            generate_random_data(30, 0, 4) + generate_random_data(80, 0, 1)  # One department with an outlier
            for _ in range(5)
        ]
        result = calculate_aggregated_threat_score(scores)
        self.assertTrue(result > 50)

if __name__ == "__main__":
    unittest.main(argv=['first-arg-is-ignored'], exit=False)
