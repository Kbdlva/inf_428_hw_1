import numpy as np

def generate_random_data(mean, variance, num_samples):
    lower_bound = max(mean - variance, 0)
    upper_bound = min(mean + variance + 1, 90)

    if lower_bound >= upper_bound:
        raise ValueError(f"Invalid range: lower_bound >= upper_bound. Lower bound: {lower_bound}, Upper bound: {upper_bound}")
    
    return np.random.randint(lower_bound, upper_bound, num_samples)


def calculate_department_mean(threat_scores):
    return np.mean(threat_scores)


def calculate_department_variance(threat_scores):
    return np.var(threat_scores)


def calculate_aggregated_threat_score(department_scores):
    """
    Calculate aggregated threat score. Departments with higher variance are weighted more
    to account for potential outliers.
    """
    means = [np.mean(scores) for scores in department_scores]
    variances = [np.var(scores) for scores in department_scores]
    
    # Normalize variances to use as weights (avoid division by zero)
    max_variance = max(variances)
    weights = [(var / max_variance) if max_variance > 0 else 1 for var in variances]
    
    # Weighted average
    weighted_sum = sum(mean * weight for mean, weight in zip(means, weights))
    total_weight = sum(weights)
    
    aggregated_score = weighted_sum / total_weight if total_weight > 0 else np.mean(means)
    return min(max(aggregated_score, 0), 90)
