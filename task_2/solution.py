import numpy as np

def generate_random_data(mean, variance, num_samples):
    return np.random.randint(max(mean - variance, 0), min(mean + variance + 1, 90), num_samples)


def calculate_department_mean(threat_scores):
    return np.mean(threat_scores)

def calculate_aggregated_threat_score(department_scores, importance_weights):
    # Calculate weighted mean of department scores
    weighted_sum = sum(score * weight for score, weight in zip(department_scores, importance_weights))
    total_weight = sum(importance_weights)
    return min(max(weighted_sum / total_weight, 0), 90) 