import numpy as np

def generate_random_data(mean, variance, num_samples):
    return np.random.randint(max(mean - variance, 0), min(mean + variance + 1, 90), num_samples)


def calculate_department_mean(threat_scores):
    return np.mean(threat_scores) #function to calulate mean of 5 deparment threat_scores

def calculate_aggregated_threat_score(department_scores, importance_weights):
    # Calculate weighted mean of department scores
    weighted_sum = sum(score * weight for score, weight in zip(department_scores, importance_weights)) #zip(department_scores, importance_weights): This combines department_scores and importance_weights into pairs, where each score is matched with its corresponding weight.
    total_weight = sum(importance_weights)
    return min(max(weighted_sum / total_weight, 0), 90) #weighted average of the department scores between 0-90

# department_scores is a list of mean threat scores for different departments.
# importance_weights is indicating how critical the threat levels in each department are relative to others.
