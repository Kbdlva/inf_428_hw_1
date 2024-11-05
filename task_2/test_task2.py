import unittest

from solution import generate_random_data, calculate_department_mean, calculate_aggregated_threat_score 

class TestAggregatedThreatScore(unittest.TestCase):
    
    def test_calculate_department_mean(self):
        data = [10, 20, 30, 40, 50]  #give values to department thread score 
        self.assertAlmostEqual(calculate_department_mean(data), 30, places=2) # check value of the function with actual value
    
    def test_calculate_aggregated_threat_score(self):
        department_scores = [50, 60, 70]
        importance_weights = [1, 1, 1]
        self.assertAlmostEqual(calculate_aggregated_threat_score(department_scores, importance_weights), 60, places=2)

        # Aggregated Score= (50*1 + 60 *1 + 70 *1)/1+1+1 = 60 --> check that function esstimates this way


        # different variations of combinations 

# - all departments has the same importance
# - all departments has the different importance
# - different number of users.
# - each department has no outliers (no really high threat scores) and vice versa
# - each department mean threat score are NOT far from each other and vice versa


    def test_equal_mean_scores_equal_importance(self):
        scores = [generate_random_data(50, 5, 50) for _ in range(5)]
        department_means = [calculate_department_mean(score) for score in scores]
        importance = [3, 3, 3, 3, 3]
        result = calculate_aggregated_threat_score(department_means, importance)
        self.assertTrue(0 <= result <= 90)

    def test_high_variance_in_threat_scores(self):
        scores = [
            generate_random_data(10, 5, 50),  # Low threat department
            generate_random_data(80, 5, 50),  # High threat department
            generate_random_data(40, 10, 50),
            generate_random_data(30, 20, 50),
            generate_random_data(70, 5, 50)
        ]
        department_means = [calculate_department_mean(score) for score in scores]
        importance = [3, 3, 3, 3, 3]
        result = calculate_aggregated_threat_score(department_means, importance)
        self.assertTrue(0 <= result <= 90)

    def test_different_importance_weights(self):
        scores = [
            generate_random_data(50, 5, 50),
            generate_random_data(60, 10, 50),
            generate_random_data(70, 5, 50),
            generate_random_data(30, 10, 50),
            generate_random_data(20, 5, 50)
        ]
        department_means = [calculate_department_mean(score) for score in scores]
        importance = [1, 2, 5, 3, 4]
        result = calculate_aggregated_threat_score(department_means, importance)
        self.assertTrue(0 <= result <= 90)

    def test_large_differences_in_user_count(self):
        scores = [
            generate_random_data(50, 5, 200),
            generate_random_data(30, 10, 10),
            generate_random_data(40, 5, 20),
            generate_random_data(70, 15, 100),
            generate_random_data(60, 10, 150)
        ]
        department_means = [calculate_department_mean(score) for score in scores]
        importance = [3, 2, 1, 4, 5]
        result = calculate_aggregated_threat_score(department_means, importance)
        self.assertTrue(0 <= result <= 90)

    def test_extreme_outliers(self):
        scores = [
            generate_random_data(10, 2, 50),  # Very low threat
            generate_random_data(85, 2, 50),  # Very high threat
            generate_random_data(45, 5, 50),
            generate_random_data(60, 3, 50),
            generate_random_data(30, 1, 50)
        ]
        department_means = [calculate_department_mean(score) for score in scores]
        importance = [1, 5, 3, 2, 4]
        result = calculate_aggregated_threat_score(department_means, importance)
        self.assertTrue(0 <= result <= 90)

if __name__ == "__main__":
    unittest.main(argv=['first-arg-is-ignored'], exit=False)

